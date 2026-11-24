-- Ejecutar DESPUÉS de schema.sql. Conserva las tablas anteriores y sus datos.
begin;
create table if not exists public.cms_workspace (
 id text primary key check(id='main'), published jsonb not null, draft jsonb not null,
 revision bigint not null default 0, published_revision bigint not null default 0,
 changed_at timestamptz not null default now(), changed_by text not null default 'migration'
);
create table if not exists public.cms_versions (
 id bigint generated always as identity primary key, snapshot jsonb not null,
 revision bigint not null, actor text not null, created_at timestamptz not null default now(), action text not null
);
create table if not exists public.cms_media (
 id text primary key, data jsonb not null, created_at timestamptz not null default now()
);
alter table public.cms_workspace enable row level security;
alter table public.cms_versions enable row level security;
alter table public.cms_media enable row level security;
revoke all on public.cms_workspace, public.cms_versions, public.cms_media from public, anon, authenticated;
grant select,insert,update,delete on public.cms_workspace, public.cms_versions, public.cms_media to service_role;
grant usage,select on sequence public.cms_versions_id_seq to service_role;
-- Inicialización atómica desde los registros existentes (solo si ya fueron importados).
with snapshot as (select jsonb_build_object('products',coalesce((select jsonb_agg(data order by id) from public.products),'[]'::jsonb),'settings',coalesce((select data from public.shop_settings where id='main'),'{}'::jsonb)) as data)
insert into public.cms_workspace(id,published,draft) select 'main',data,data from snapshot where exists(select 1 from public.products) on conflict do nothing;
-- La revisión evita que dos dispositivos sobrescriban silenciosamente sus cambios.
create or replace function public.cms_commit(expected bigint, next_draft jsonb, operation text, actor_email text, restore_id bigint default null)
returns jsonb language plpgsql security invoker set search_path=public as $$
declare w public.cms_workspace%rowtype; restored jsonb; before_id bigint; after_id bigint;
begin
 select * into w from public.cms_workspace where id='main' for update;
 if not found then raise exception 'CMS no inicializado'; end if;
 if w.revision <> expected then raise exception 'CMS_CONFLICT' using errcode='40001'; end if;
 if operation='save' then
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.draft,w.revision,actor_email,'before_save') returning id into before_id;
   w.draft:=next_draft;
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.draft,w.revision+1,actor_email,'save') returning id into after_id;
 elsif operation='discard' then
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.draft,w.revision,actor_email,'before_discard');
   w.draft:=w.published;
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.draft,w.revision+1,actor_email,'discard');
 elsif operation='restore' then
   select snapshot into restored from public.cms_versions where id=restore_id;
   if not found then raise exception 'Versión inexistente'; end if;
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.draft,w.revision,actor_email,'before_restore');
   w.draft:=restored;
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.draft,w.revision+1,actor_email,'restore');
 elsif operation='publish' then
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.published,w.published_revision,actor_email,'before_publish');
   w.published:=w.draft; w.published_revision:=w.revision+1;
   insert into public.cms_versions(snapshot,revision,actor,action) values(w.published,w.published_revision,actor_email,'publish');
 else raise exception 'Operación inválida'; end if;
 w.revision:=w.revision+1;
 update public.cms_workspace set draft=w.draft,published=w.published,revision=w.revision,published_revision=w.published_revision,changed_at=now(),changed_by=actor_email where id='main';
 return jsonb_build_object('revision',w.revision,'publishedRevision',w.published_revision,'pending',w.draft<>w.published,'beforeId',before_id,'afterId',after_id);
end $$;
revoke all on function public.cms_commit(bigint,jsonb,text,text,bigint) from public,anon,authenticated;
grant execute on function public.cms_commit(bigint,jsonb,text,text,bigint) to service_role;
commit;
