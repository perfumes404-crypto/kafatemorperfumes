-- Conserva las imágenes existentes y habilita el bucket utilizado por el CMS.
insert into storage.buckets (id,name,public,file_size_limit,allowed_mime_types)
values ('product-images','product-images',true,2500000,array['image/jpeg','image/png','image/webp','image/avif'])
on conflict (id) do update set public=true,file_size_limit=2500000,allowed_mime_types=excluded.allowed_mime_types;
-- La API de la tienda valida la sesión y escribe con service_role; no crear políticas públicas de escritura.
