-- Ejecutar en SQL Editor de Supabase. No contiene credenciales.
create table if not exists public.products (id text primary key, data jsonb not null, check (data->>'id'=id));
create table if not exists public.shop_settings (id text primary key, data jsonb not null);
alter table public.products enable row level security;
alter table public.shop_settings enable row level security;
revoke all on public.products, public.shop_settings from anon, authenticated;
grant select, insert, update, delete on public.products, public.shop_settings to service_role;
insert into storage.buckets (id,name,public,file_size_limit,allowed_mime_types) values ('product-images','product-images',true,2500000,array['image/jpeg','image/png','image/webp','image/avif']) on conflict (id) do update set public=true,file_size_limit=2500000,allowed_mime_types=excluded.allowed_mime_types;
-- Sin políticas de escritura para anon/authenticated: solo el backend autorizado escribe.
