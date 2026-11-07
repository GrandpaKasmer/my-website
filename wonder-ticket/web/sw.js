/* The build replaces __BUILD_ID__. A scope-specific name avoids other apps' caches. */
const PREFIX='wonder-ticket:'+self.registration.scope+':';
const CACHE=PREFIX+'__BUILD_ID__';
const FILES=['./','./index.html','./privacy.html','./terms.html','./manifest.webmanifest','./icon.svg','./icon-180.png','./icon-192.png','./icon-512.png','./icon-maskable.png'];
const URLS=new Set(FILES.map(p=>new URL(p,self.registration.scope).href));
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES))));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  const url=new URL(event.request.url); url.search=''; url.hash='';
  if(!URLS.has(url.href))return;
  // Network-first documents, cached fallback. No user data or third-party requests are cached.
  event.respondWith(fetch(event.request).then(response=>{
    if(response.ok&&response.type==='basic'){
      const copy=response.clone();event.waitUntil(caches.open(CACHE).then(c=>c.put(url.href,copy)));
    }
    return response;
  }).catch(async()=> (await caches.match(url.href)) || Response.error()));
});
