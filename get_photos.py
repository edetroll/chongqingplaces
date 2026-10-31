#!/usr/bin/env python3
"""Fetch and resize freely licensed Wikimedia Commons photos into this folder.
Run: python3 -m pip install requests pillow
     python3 get_photos.py
The page also works without this step via external, lazy-loaded photo previews.
"""
import io, json, time, re
from html import unescape
from pathlib import Path
import requests
from PIL import Image, ImageOps

HERE=Path(__file__).resolve().parent
items=json.loads((HERE/'photo_sources.json').read_text(encoding='utf-8'))
s=requests.Session();s.headers.update({'User-Agent':'ChongqingPersonalMiniGuide/1.0 (private CC attribution travel site)'})
credits=[];count=0
for key, refs in items.items():
 for i,ref in enumerate(refs,1):
  if ref['type']!='commons':
   credits.append(f'{key}-{i}: Externally displayed photo; please see its source page: {ref["page"]}')
   continue
  dest=HERE/f'{key}-{i}.webp'
  try:
   req=s.get('https://commons.wikimedia.org/w/api.php',params={
    'action':'query','format':'json','prop':'imageinfo','iiprop':'url|extmetadata',
    'iiurlwidth':520,'titles':'File:'+ref['file']}, timeout=30)
   req.raise_for_status()
   pages=req.json()['query']['pages']; page=next(iter(pages.values()))
   data=page['imageinfo'][0]
   meta=data.get('extmetadata',{}); license_name=re.sub('<[^>]+>','',meta.get('LicenseShortName',{}).get('value',''))
   if not any(x in license_name.lower() for x in ('cc by','cc0','public domain','pd-','cc-zero')):
    print('SKIP: Review licensing for',ref['file'],license_name); continue
   url=data.get('thumburl') or data['url']
   imgreq=s.get(url,timeout=45);imgreq.raise_for_status()
   image=Image.open(io.BytesIO(imgreq.content)); image=ImageOps.exif_transpose(image).convert('RGB')
   image.thumbnail((520,390),Image.Resampling.LANCZOS)
   image.save(dest,format='WEBP',quality=57,method=6)
   artist=unescape(re.sub("<[^>]+>", "", meta.get("Artist",{}).get("value","unknown"))).strip()
   license_link=meta.get("LicenseUrl",{}).get("value", "")
   page_link="https://commons.wikimedia.org/wiki/File:"+requests.utils.quote(ref["file"].replace(" ","_"))
   credits.append(f"{dest.name} | Author: {artist} | Licence: {license_name} ({license_link}) | Source: {page_link} | Changes: resized and converted to WebP")
   print(dest.name, f'{dest.stat().st_size/1024:.0f} KB');count+=1
  except Exception as e:print('COULD NOT FETCH',ref['file'],str(e)[:110])
  time.sleep(0.2)
(HERE/'PHOTO_CREDITS.txt').write_text('Wikimedia Commons photo credits and source pages\n\n'+'\n'.join(credits)+'\n',encoding='utf-8')
print(f'Done: {count} tiny photos downloaded. The rest have online fallbacks.')
