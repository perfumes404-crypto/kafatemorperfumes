import {supa,configured,getProducts,getSettings} from './db.js';
import {validateProduct,validateSettings,validImage} from './model.js';
import defaults from '../data/settings.json' with {type:'json'};
import original from '../data/catalog.json' with {type:'json'};
export async function workspace(init=false){
 if(!configured()){const data={products:original,settings:defaults};return {draft:data,published:data,revision:0,published_revision:0};}
 let rows=await supa('/rest/v1/cms_workspace?id=eq.main&select=*',{service:true});
 if(rows[0]){const w=rows[0];for(const k of ['draft','published'])w[k].settings={...defaults,...w[k].settings};return w;}
 const products=await getProducts(),settings=await getSettings();const data={products:products.length?products:original,settings:{...defaults,...settings}};
 if(!init)return {draft:data,published:data,revision:0,published_revision:0};
 await supa('/rest/v1/cms_workspace?on_conflict=id',{method:'POST',service:true,headers:{Prefer:'resolution=ignore-duplicates,return=minimal'},body:{id:'main',draft:data,published:data}});
 rows=await supa('/rest/v1/cms_workspace?id=eq.main&select=*',{service:true});if(!rows[0])throw Error('No se pudo inicializar el CMS');return rows[0];
}
export const pending=w=>JSON.stringify(w.draft)!==JSON.stringify(w.published);
export const details=w=>({revision:w.revision,publishedRevision:w.published_revision,pending:pending(w),changedAt:w.changed_at,changedBy:w.changed_by});
export async function commit(w,operation,user,next=w.draft,restoreId=null){try{return await supa('/rest/v1/rpc/cms_commit',{method:'POST',service:true,body:{expected:w.revision,next_draft:next,operation,actor_email:user.email,restore_id:restoreId}})}catch(e){if(e.status===409)throw Object.assign(Error('Hubo cambios en otro dispositivo. Recargá antes de guardar.'),{status:409});throw e}}
export function checkRevision(w,b){if(!Number.isSafeInteger(b.revision)||b.revision!==w.revision)throw Object.assign(Error('Hay una versión más reciente. Recargá antes de guardar.'),{status:409})}
export async function history(){return await supa('/rest/v1/cms_versions?select=id,revision,actor,created_at,action&order=id.desc&limit=100',{service:true})}
export async function listMedia(){let all=[];for(let i=0;i<10000;i+=500){const r=await supa(`/rest/v1/cms_media?select=id,data,created_at&order=created_at.desc&limit=500&offset=${i}`,{service:true});all.push(...r);if(r.length<500)break}return all}
export async function editMedia(b,w){const rows=await listMedia(),item=rows.find(x=>x.id===b.id);if(!item)throw Error('Imagen no encontrada');if(b.archived===true&&JSON.stringify([w.published,w.draft]).includes(item.data.url))throw Error('La imagen está en uso. Quitala del contenido y publicá antes de archivarla.');const data={...item.data,name:String(b.name??item.data.name).slice(0,180),alt:String(b.alt??item.data.alt).slice(0,250),folder:String(b.folder??item.data.folder).slice(0,100),archived:b.archived===true};await supa('/rest/v1/cms_media?id=eq.'+encodeURIComponent(b.id),{method:'PATCH',service:true,body:{data}});return data;}
