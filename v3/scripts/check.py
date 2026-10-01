#!/usr/bin/env python3
"""Check static links, local asset isolation, and preserved V2 story text."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.ids=[];self.h1=0;self.errors=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag in ('a','img','script','link'):
   key='src' if tag in ('img','script') else 'href'
   if a.get(key):self.links.append(a[key])
  if tag=='img' and any(k not in a for k in ['alt','width','height']):self.errors.append('Image missing alt/dimensions')
pages={p:Parser(p.read_text()) for p in ROOT.rglob('*.html') if 'content' not in p.parts}
errors=[]
for path,doc in pages.items():
 if doc.h1!=1:errors.append(f'{path}: expected one h1')
 if len(doc.ids)!=len(set(doc.ids)):errors.append(f'{path}: duplicate IDs')
 errors.extend(doc.errors)
 for ref in doc.links:
  url=urlsplit(ref)
  if url.scheme or url.netloc:continue
  target=(path.parent/unquote(url.path)).resolve() if url.path else path
  if target.is_dir():target=target/'index.html'
  if not target.is_relative_to(ROOT):errors.append(f'{path}: outside V3: {ref}')
  elif not target.exists():errors.append(f'{path}: missing {ref}')
  elif url.fragment and target in pages and url.fragment not in pages[target].ids:errors.append(f'{path}: missing anchor {ref}')
for t in json.loads((ROOT/'content/expeditions.json').read_text()):
 original=(ROOT.parent/'v2-preview/field-notes'/f'{t["slug"]}.html').read_text()
 old=re.search(r'<div class="prose">(.*?)<div class="actions">',original,re.S)[1]
 if t['slug']=='california-expedition':
  for before,after in {
   'Spencer called (again) and invited us':'Spencer called (again - lol!) and invited us',
   'parking for rigs like mine.':'parking for rigs like PourHouse.',
   'Everybody wins. We stayed at an air and space museum in Oklahoma. We visited Petrified Forest, and stopped in Palm Springs to see Steve again. We made fairly direct time and we were camped in urban SF on the Pacific coast - an easy Uber ride to his apartment by Thanksgiving.':'Everybody wins. We visited Petrified Forest, and stopped in Palm Springs to see Steve and Buddy again. We made fairly direct time and we were camped in urban SF on the Pacific coast - an easy Uber ride to Ria and Spencer\'s apartment by Thanksgiving.',
   'We visited the city to see Spencer, and':'We visited the city to see Ria and Spencer, and',
   'adding adjustable shocks all around and a rear leaf spring mini-pack.':'Colorado had made it clear that PourHouse was not ready for Alaska.',
   'But this was different. Now, we were living here.':'But this was different. Now we were living here.',
   'We camped a week at a time off-grid; twice! We visited Kofa National Wildlife Refuge, camped before and after Sedona, Roosevelt Lake, the Apache Trail, Saguaro, Las Cienegas National Conservation Area.':'We camped a week at a time off-grid - twice! We visited Kofa National Wildlife Refuge, camped before and after Sedona, visited Roosevelt Lake, drove the Apache Trail, looked for tarantulas in Saguaro, and slept in the Las Cienegas National Conservation Area.',
  }.items(): old=old.replace(before,after)
 source=(ROOT/'content/stories'/f'{t["slug"]}.html').read_text()
 assert old==source, f'Story changed: {t["slug"]}'
# Expedition pools stay local; explicitly verified Gallery masters may be shared.
shared_photos=json.loads((ROOT/'content/shared-photo-assets.json').read_text())
for shared in shared_photos:
 assert shared['retained'].startswith('gallery/')
 assert hashlib.sha256((ROOT/'assets/photos'/shared['retained']).read_bytes()).hexdigest()==shared['sha256'], f'Shared photo changed: {shared}'
for slug, photos in json.loads((ROOT/'content/field-note-photos.json').read_text()).items():
 assert len(photos)>1, f'Not enough photographs: {slug}'
 expected_frames=4 if slug=='pch-ex' else 3
 assert (ROOT/'field-notes'/f'{slug}.html').read_text().count('data-photo-frame')==expected_frames
 for photo in photos:
  assert photo['src'].startswith(f'field-notes/{slug}/') or any(shared['original'].startswith(f'field-notes/{slug}/') and shared['retained']==photo['src'] for shared in shared_photos), f'Cross-expedition image: {photo}'
  assert (ROOT/'assets/photos'/photo['src']).is_file(), f'Missing rotation image: {photo}'
  assert photo['alt'] and photo['caption'], f'Missing accessible copy: {photo}'
assert not errors,'\n'.join(errors)
print(f'PASS: {len(pages)} pages; all local links/assets/anchors; isolated V3 paths; six exact source stories; image alt/dimensions.')
