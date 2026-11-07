import {spawnSync} from 'node:child_process';
import path from 'node:path';
if(process.platform!=='darwin'){console.error('Opening Xcode requires your Mac. Run npm run ios:sync first, then open ios/WonderTicket.xcodeproj on macOS.');process.exit(1);}
const result=spawnSync('open',[path.resolve(import.meta.dirname,'../ios/WonderTicket.xcodeproj')],{stdio:'inherit'});
process.exit(result.status??1);
