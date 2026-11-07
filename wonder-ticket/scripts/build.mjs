import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
const root=path.resolve(import.meta.dirname,'..');
const out=path.join(root,'dist');
await fs.rm(out,{recursive:true,force:true});
await fs.cp(path.join(root,'web'),out,{recursive:true});
// Original ticket icon, rasterized with Node alone. No font files or external assets.
function crc32(buf){let crc=0xffffffff;for(const b of buf){crc^=b;for(let k=0;k<8;k++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}return(crc^0xffffffff)>>>0;}
function chunk(type,data){const name=Buffer.from(type),len=Buffer.alloc(4),crc=Buffer.alloc(4);len.writeUInt32BE(data.length);crc.writeUInt32BE(crc32(Buffer.concat([name,data])));return Buffer.concat([len,name,data,crc]);}
function png(size,maskable=false){const stride=size*3+1,raw=Buffer.alloc(stride*size),bg=[16,39,36],gold=[232,189,112];
for(let y=0;y<size;y++){raw[y*stride]=0;for(let x=0;x<size;x++){let a=x/size*512,b=y/size*512;if(maskable){a=(a-256)/.86+256;b=(b-256)/.86+256;}const ticket=a>=104&&a<=408&&b>=142&&b<=370&&!((a-104)**2+(b-256)**2<38**2)&&!((a-408)**2+(b-256)**2<38**2);const star=Math.abs(a-256)+Math.abs(b-256)<74&&Math.abs(a-256)*Math.abs(b-256)<1100;const dash=(Math.abs(a-147)<3.5||Math.abs(a-365)<3.5)&&((b>=168&&b<=195)||(b>=317&&b<=344));const color=ticket&&!star&&!dash?gold:bg;const p=y*stride+x*3+1;raw[p]=color[0];raw[p+1]=color[1];raw[p+2]=color[2];}}
const head=Buffer.alloc(13);head.writeUInt32BE(size,0);head.writeUInt32BE(size,4);head[8]=8;head[9]=2;return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',head),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))]);}
for(const size of[180,192,512])await fs.writeFile(path.join(out,`icon-${size}.png`),png(size));
await fs.writeFile(path.join(out,'icon-maskable.png'),png(512,true));
const digest=crypto.createHash('sha256');for(const name of(await fs.readdir(out)).sort()){digest.update(name);digest.update(await fs.readFile(path.join(out,name)));}const id=digest.digest('hex').slice(0,12);
const sw=await fs.readFile(path.join(out,'sw.js'),'utf8');await fs.writeFile(path.join(out,'sw.js'),sw.replaceAll('__BUILD_ID__',id));
console.log(`Built dist/ (${id}); no dependencies or API keys required.`);
if(process.argv.includes('--ios')){
const web=path.join(root,'ios/WonderTicket/Web');await fs.rm(web,{recursive:true,force:true});await fs.cp(out,web,{recursive:true});
const assets=path.join(root,'ios/WonderTicket/Assets.xcassets/AppIcon.appiconset');await fs.mkdir(assets,{recursive:true});
const specs=[['iphone',20,2],['iphone',20,3],['iphone',29,2],['iphone',29,3],['iphone',40,2],['iphone',40,3],['iphone',60,2],['iphone',60,3],['ipad',20,1],['ipad',20,2],['ipad',29,1],['ipad',29,2],['ipad',40,1],['ipad',40,2],['ipad',76,1],['ipad',76,2],['ipad',83.5,2],['ios-marketing',1024,1]];
const images=[];for(const[idiom,points,scale]of specs){const size=points*scale,filename=`icon-${size}.png`;await fs.writeFile(path.join(assets,filename),png(size));images.push({idiom,size:`${points}x${points}`,scale:`${scale}x`,filename});}
await fs.writeFile(path.join(assets,'Contents.json'),JSON.stringify({images,info:{version:1,author:'xcode'}},null,2)+'\n');
console.log('Synced bundled web files and original app icons into ios/. Xcode signing and compilation are still required.');
}
