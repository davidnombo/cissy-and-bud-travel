#!/usr/bin/env python3
"""Build all V3 HTML from local content. Python standard library only."""
from pathlib import Path
import json, re, html
from launch_build import odyssey_explainer
ROOT=Path(__file__).resolve().parents[1]
GOOGLE_TAG=(ROOT/'content/google-tag.html').read_text().rstrip()
def load(name): return json.loads((ROOT/'content'/f'{name}.json').read_text())
def esc(s): return html.escape(str(s),quote=True)
trips=load('expeditions'); images=load('images'); odyssey=load('odyssey'); field_photos=load('field-note-photos')
NAV=[('Home',''),('Transcontinental Odyssey','odyssey/'),('Field Notes','field-notes/'),('Gallery','gallery/'),('FAQs','faqs/'),('About Us','about/'),('Thank You','support/')]
def photo(src,alt,prefix='',eager=False,cls=''):
 src=str(Path(src));src=src if src in images else str(Path(src).with_suffix('.webp'));meta=images[src]
 return f'<img class="{cls}" src="{prefix}assets/photos/{src}" alt="{esc(alt)}" width="{meta["width"]}" height="{meta["height"]}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async">'
def link(url,label,cls='text-link'):return f'<a class="{cls}" href="{url}">{label} <span aria-hidden="true">↗</span></a>'
def page(path,title,body,desc,current,article=False,launch=False):
 depth=len(Path(path).parts)-1;p='../'*depth
 nav=''.join(f'<a href="{p}{url or "index.html"}"'+(' aria-current="page"' if key==current else '')+f'>{key}</a>' for key,url in NAV)
 out=f'''<!doctype html>
<html lang="en"><head>{GOOGLE_TAG}<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} — PourHouseLife</title><meta name="description" content="{esc(desc)}"><link rel="icon" href="{p}assets/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;500;600;650&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}css/site.css?v=17">{f'<link rel="stylesheet" href="{p}css/field-notes.css?v=5">' if article else ''}<script src="{p}js/site.js?v=3" defer></script>{f'<script src="{p}js/field-notes.js?v=3" defer></script>' if article else ''}</head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="{p}index.html"><img src="{p}assets/pourhouse-life-logo.webp" alt="" width="62" height="62"><strong>PourHouseLife</strong></a><button class="menu" aria-expanded="false" aria-controls="navigation" hidden>Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation">{nav}</nav></header><main id="main">{body}</main><footer><div class="shell footer-inner"><div><a class="footer-brand" href="{p}index.html">PourHouseLife</a><p>Cassie and David take the long way.</p></div><div>{'' if current in ('Transcontinental Odyssey','Thank You') else link(p+'odyssey/','Follow the Odyssey')}<p>© 2026 PourHouseLife · Go small. Go now.</p></div></div></footer></body></html>'''
 if launch:out=out.replace('</head>',f'<link rel="stylesheet" href="{p}css/launch-build.css?v=2"></head>')
 target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(out+'\n')
def intro(kicker,title,description,cls=''):return f'<header class="page-intro shell {cls}"><p class="kicker">{kicker}</p><h1>{title}</h1><p class="intro">{description}</p></header>'
def facts(t):return '<dl class="facts">'+''.join(f'<div><dt>{k}</dt><dd>{esc(v)}</dd></div>' for k,v in t['facts'].items())+'</dl>'
def panel(kicker,title,text,image,alt,url,cta,reverse=False,caption=''):
 caption_html=f'<span class="photo-credit panel-caption">{esc(caption)}</span>' if caption else ''
 return f'<section class="feature-panel {"reverse" if reverse else ""}"><div class="panel-photo">{photo(image,alt)}{caption_html}</div><div class="panel-copy"><p class="kicker">{kicker}</p><h2>{title}</h2><p>{text}</p>{link(url,cta)}</div></section>'
hero=f'''<div class="shell home"><div class="edition"><span>A travel journal by Cassie &amp; David</span><span>On the road since 2019</span></div><section class="home-hero"><div class="hero-copy"><p class="eyebrow">The road ahead · October 18, 2026</p><h1>{odyssey['heading']}</h1><p class="hero-title">Transcontinental Odyssey</p><p>Key West to Deadhorse</p><div class="hero-links">{link('odyssey/','Follow the Odyssey')}<a class="text-link" href="mailto:PourHouseLife@gmail.com?subject=Follow%20the%20Odyssey">Contact Us <span aria-hidden="true">↗</span></a></div></div><div class="hero-photo">{photo('death-valley-van.jpg','PourHouse beneath the desert mountains',eager=True)}<span class="photo-credit">PourHouse, Death Valley National Park</span></div></section><div class="opening"><p>Two people. A home on wheels.<br>A little more room for the unexpected.</p><p>We’re Cassie and David. From our Prius V to our Sprintervan called PourHouse, our trips have grown into a way of life. Next up: Key West to Deadhorse, part of 50,000 miles and a year on the road...</p></div><div class="panel-stack">'''
hero+=panel('01 / The archive','Field Notes','Six journeys. Each vehicle made a different kind of adventure possible.','utah-2019/bryce-overlook.jpg','Cassie and David looking over Bryce Canyon','field-notes/','Explore the Field Notes',caption='Spencer and Cassie, Bryce Canyon National Park')
hero+=panel('02 / The visual record','Gallery','Places we pulled over. Views we stayed for. Photographs from our travels, collected along the way.','redington-pass.jpg','PourHouse at sunset on Redington Pass','gallery/','Browse the photographs',True,'PourHouse at sunset, Redington Pass')
questions = ''.join(f'<span class="faq-question{ " active" if i < 3 else ""}" aria-hidden="{ "false" if i < 3 else "true"}">{esc(q["question"])}</span>' for i, q in enumerate(load('faqs')))
hero+='<section class="faq-teaser faq-photo-card"><div class="faq-teaser-photo">'+photo('pourhouse-faq-question-marks.jpg','PourHouse surrounded by green and black question marks')+'</div><div class="faq-teaser-copy"><p class="kicker">03 / Life on the road</p><h2>Frequently Asked Questions</h2><p class="faq-questions" aria-live="off">'+questions+'</p><button class="faq-rotation" type="button" hidden>Pause questions</button>'+link('faqs/','A few honest answers')+'</div></section>'
hero+=panel('04 / The people behind PourHouse','About Us','We began with a Prius, upgraded to a minivan, and now we\'re touring North America in a sprinter van called PourHouse.  We preserve the trips, practical lessons, and experiences from the road.','cassie-pacific.jpg','Cassie looking out toward the Pacific','about/','Meet Cassie and David')
hero+='</div></div>'
page('index.html','Taking the Long Way',hero,'Cassie and David, six past expeditions, and the road ahead from Key West to Deadhorse.','Home')
body=intro('The archive / 2019 onward','Field Notes','Each rig changed the size of our map. Follow six previous expeditions, and watch the progression.')+'<div class="shell expedition-stack">'
for i,t in reversed(list(enumerate(trips))):
 image=t['image'];alt=t['alt']
 card=dict(t);card['facts']={("Distance" if key=="Mileage" else key):value for key,value in t['facts'].items()}
 if t['slug'] in ('great-western-loop','pch-ex'):card['facts']['Vehicle']='Ivan the minivanRV'
 summary='We traveled with Cassie\'s parents to discover the Pacific Northwest.' if t['slug']=='northwest-hot-lap' else t['summary']
 if t['slug']=='prius-utah-2019':summary='Spencer proposed a national-park trip from Denver to Las Vegas. We discovered that the drive itself could become the adventure.'
 if t['slug']=='northwest-hot-lap':image='gallery/47-577b8119.jpg';alt='Snow-covered mountain above evergreen trees'
 if t['slug']=='pch-ex':image='field-notes/pch-ex/44-0fa91611.jpg';alt='Waves crashing against rocks along the Pacific Coast'
 if t['slug']=='socoex':image='field-notes/socoex/79-a7de4831.jpg';alt='PourHouse overlooking the Southern Colorado high country'
 body+=f'<article class="expedition"><a class="expedition-photo" href="{t["slug"]}.html" aria-label="Read {esc(t["title"])}">{photo(image,alt,"../",i==0)}</a><div class="expedition-copy"><p class="kicker">Field Note / 0{i+1}</p><h2><a href="{t["slug"]}.html">{t["title"]}</a></h2>{facts(card)}<h3>{t["heading"]}</h3><p>{summary}</p>{link(t["slug"]+".html","Read the complete Field Note")}</div></article>'
body+='</div>'
page('field-notes/index.html','Field Notes',body,'Six historical expeditions, from California Expedition back to Mighty V Passage.','Field Notes')
for i,t in enumerate(trips):
 src=t['image'];alt=t['alt']
 if t['slug']=='northwest-hot-lap':src='northwest-hotlap/seaside-bubbles.webp';alt='Bubbles at sunset on the Oregon coast'
 prose=(ROOT/'content/stories'/f'{t["slug"]}.html').read_text()
 # Each page owns one expedition pool; the Gallery never reads this data.
 pool=field_photos[t['slug']]
 assert len(pool)>1, 'Rotating frames need multiple expedition photographs'
 def frame(number,hero=False):
  staggered_starts={
   'california-expedition':{1:0,2:99,3:199},
   # SoCoEx has one authored figure; generated frames 3, 1, and 2 appear
   # from top to bottom after the two additional players are inserted.
   'socoex':{3:0,1:24,2:49},
   # PCH-Ex appears in visual order 3, 1, 4, 2 after the selected-break
   # player and one evenly distributed player are added.
   'pch-ex':{3:0,1:2,4:4,2:6},
   # Great Western Loop's two authored figures surround its generated player.
   'great-western-loop':{1:0,3:5,2:10},
  }
  start=staggered_starts.get(t['slug'],{}).get(number,number) % len(pool)
  selected=pool[start]
  image_url='../assets/photos/'+selected['src']
  return f'<figure class="photo-frame {"shell story-photo" if hero else ""}" data-photo-frame data-start="{start}" aria-label="{esc(t["title"])} photographs, frame {number+1}"><div class="frame-image" style="--frame-bg:url(\'{esc(image_url)}\')">{photo(selected["src"],selected["alt"],"../",hero)}</div><figcaption><span class="frame-caption">{esc(selected["caption"])}</span><div class="frame-controls" hidden><span class="frame-count">{start+1} / {len(pool)}</span><button type="button" data-previous aria-label="Previous photograph">←</button><button type="button" data-next aria-label="Next photograph">→</button><button type="button" data-pause>Pause photos</button></div></figcaption></figure>'
 frame_number=[0]
 def replace_figure(match):
  frame_number[0]+=1
  return frame(frame_number[0])
 prose=re.sub(r'<figure>.*?</figure>',replace_figure,prose,flags=re.S)
 if t['slug']=='pch-ex':
  selected_break='<p>Death Valley felt massive and astonishingly empty.'
  assert selected_break in prose
  frame_number[0]+=1
  prose=prose.replace(selected_break,frame(frame_number[0])+selected_break,1)
 # Preserve the original prose and existing image positions; add enough breaks
 # to give every story three inline frames, except PCH-Ex's requested fourth.
 target_frames=4 if t['slug']=='pch-ex' else 3
 missing=target_frames-frame_number[0]
 if missing>0:
  headings=list(re.finditer(r'<h2>',prose))
  positions=[headings[min(len(headings)-1, max(1,round((k+1)*len(headings)/(missing+1))))].start() for k in range(missing)]
  for pos in sorted(positions,reverse=True):
   frame_number[0]+=1
   prose=prose[:pos]+frame(frame_number[0])+prose[pos:]
 photo_data=json.dumps(pool,ensure_ascii=False).replace('<','\\u003c')
 photo_script=f'<script type="application/json" id="expedition-photos">{photo_data}</script>'
 next_trip=trips[(i+1)%len(trips)]
 opening_media=''
 body=f'<div class="shell article-top"><a href="./">← All Field Notes</a><span>From the archive / 0{i+1}</span></div><header class="story-header shell"><p class="kicker">Field Notes · {t["facts"]["When"]}</p><h1>{t["title"]}</h1><p class="intro">{t["dek"]}</p></header>{opening_media}<article class="article shell {t["slug"]}"><aside aria-label="Expedition facts">{facts(t)}</aside><div class="prose">{prose}<nav class="story-next" aria-label="More Field Notes"><p class="kicker">{"Start again" if i==5 else "The next chapter"}</p>{link(next_trip["slug"]+".html",next_trip["title"])}<p><a href="./">All Field Notes</a></p></nav></div></article>'
 page('field-notes/'+t['slug']+'.html',t['title'],body+photo_script,t['summary'],'Field Notes',True)
page('odyssey/what-the-hell-is-the-odyssey.html','What the Hell Is the Odyssey?',odyssey_explainer(load('odyssey-explainer')['paragraphs']),'How Alaska became a year-long Transcontinental Odyssey. Go Small. Go Now.','Transcontinental Odyssey',article=True,launch=True)
body=intro('The road ahead / Departing October 18, 2026','Transcontinental Odyssey','Our current chapter: A one-year, 50,000 mile loop around the US and Canada','odyssey-intro')
body+='<div class="shell"><section class="odyssey-overview"><div class="odyssey-overview-copy"><p class="kicker">'+esc(odyssey['status'])+'</p><h2>Room to change<br>our minds.</h2><p class="intro">A much larger year-long journey, with Key West and Deadhorse as two of its defining destinations.</p><p>Our next chapter is the Transcontinental Odyssey: a roaming, slow-travel journey built around public land, overlooked towns, family, friends, and the freedom to change our minds.</p><dl class="route-facts"><div><dt>Southern marker</dt><dd>Key West, Florida</dd></div><div><dt>Northern marker</dt><dd>Deadhorse, Alaska</dd></div><div><dt>Planned departure</dt><dd>October 18, 2026</dd></div><div><dt>Home on the road</dt><dd>PourHouse</dd></div></dl><p class="odyssey-explainer-link">'+link('what-the-hell-is-the-odyssey.html','What the Hell Is the Odyssey?')+'</p></div><figure class="odyssey-overview-photo">'+photo('death-valley-wide.jpg','PourHouse crossing the vast landscape of Death Valley','../',True)+'<figcaption>From the archive · Death Valley</figcaption></figure></section><section id="dispatches" class="dispatches"><p class="kicker">The journey journal</p><h2>Dispatches from the road</h2>'
if not odyssey['updates']:body+='<div class="dispatch-follow"><h2>Want to hear from us when there’s something new from the Transcontinental Odyssey?</h2><a class="button" href="mailto:PourHouseLife@gmail.com?subject=Follow%20the%20Odyssey">Send Us a Note <span aria-hidden="true">↗</span></a><p>Say hello and we’ll add you to our road-dispatch list.</p></div>'
for update in odyssey['updates']:
 body+=f'<article class="dispatch"><p class="kicker"><time datetime="{esc(update["date"])}">{esc(update["date"])}</time> · {esc(update["location"])}</p><h3>{esc(update["title"])}</h3>'
 for img in update.get('images',[]):body+='<figure>'+photo(img['src'],img['alt'],'../')+(f'<figcaption>{esc(img["caption"])}</figcaption>' if img.get('caption') else '')+'</figure>'
 body+=''.join('<p>'+esc(p)+'</p>' for p in update['paragraphs'])
 for key,label in [('social_url','Watch the reel'),('map_url','See the location')]:
  if update.get(key):
   if not update[key].startswith('https://'):raise ValueError('Optional update links must use HTTPS')
   body+=link(esc(update[key]),label)
 body+='</article>'
body+='</section><section class="simple-callout"><h2>The roads that brought us here.</h2>'+link('../field-notes/','Read the historical Field Notes')+'</section></div>'
page('odyssey/index.html',odyssey['title'],body,'The upcoming Transcontinental Odyssey: Key West to Deadhorse, departing October 18, 2026.','Transcontinental Odyssey')
# Gallery is David's explicit selection. Never populate it from photo imports.
body=intro('The visual record','Gallery',"We've taken tens of thousands of photos.  These are the best.")+'<div class="shell gallery-wrap"><div class="gallery">'
for i,item in enumerate(load('gallery')):
 s,c,e=item['src'],item['caption'],item['expedition'];url='../assets/photos/'+(s if s in images else str(Path(s).with_suffix('.webp')))
 body+=f'<figure data-expedition="{esc(e)}"><a href="{url}" aria-label="View photograph: {esc(c)}">{photo(s,c,"../",i==0)}</a></figure>'
body+='</div></div>'
page('gallery/index.html','Gallery',body,'Photographs from Cassie and David’s travels.','Gallery')
body=intro('Life on the road','A few honest answers.','The practical questions behind the photographs.')+'<div class="shell faq-page"><section class="faq-contact dispatch-follow"><h2>Have a question we didn’t answer? Send us a note.</h2><a class="button" href="mailto:PourHouseLife@gmail.com?subject=Question%20for%20PourHouseLife">Send Us a Note <span aria-hidden="true">↗</span></a></section><div class="faq-list">'
for q in load('faqs'):body+=f'<details><summary>{esc(q["question"])}</summary><p>{esc(q["answer"])}</p></details>'
body+='</div></div>'
page('faqs/index.html','FAQs',body,'Practical answers about sleeping and daily life on the road.','FAQs')
about_file=ROOT/'content/about.html'
if not about_file.exists():
 source=(ROOT.parent/'about.html').read_text();copy=re.search(r'<h2 class="title">We are real people building freedom as we see it.</h2>(.*?)</div></div></section>',source,re.S)[1];about_file.write_text(copy)
body=intro('The people behind PourHouse','We are Cassie<br>and David.','PourHouseLife is what happens when the route becomes the story.')+'<div class="shell about-layout"><div><figure>'+photo('cassie-pacific.jpg','Cassie looking across the Pacific Ocean','../',True)+'<figcaption>Traveling at human speed.</figcaption></figure><figure>'+photo('utah-2019/bryce-overlook.jpg','Cassie and David overlooking Bryce Canyon','../')+'</figure></div><div class="about-prose"><h2>We are real people building freedom as we see it.</h2>'+about_file.read_text()+link('../field-notes/','Start with our first expedition')+'</div></div>'
page('about/index.html','About Us',body,'Meet Cassie and David and the story behind PourHouseLife.','About Us')
gallery_photos=[{'src':item['src'] if item['src'] in images else str(Path(item['src']).with_suffix('.webp')),'alt':item['caption'],'caption':item['caption']} for item in load('gallery')]
selected=gallery_photos[0]
support_photo='../assets/photos/'+str(Path(selected['src']).with_suffix('.webp'))
support_player=f'<figure class="photo-frame thank-you-player" data-photo-frame data-start="0" aria-label="Photographs from the PourHouseLife gallery"><div class="frame-image" style="--frame-bg:url(\'{esc(support_photo)}\')">{photo(selected["src"],selected["alt"],"../",True)}</div><figcaption><span class="frame-caption">{esc(selected["caption"])}</span><div class="frame-controls" hidden><span class="frame-count">1 / {len(gallery_photos)}</span><button type="button" data-previous aria-label="Previous photograph">←</button><button type="button" data-next aria-label="Next photograph">→</button><button type="button" data-pause>Pause photos</button></div></figcaption></figure>'
photo_data=json.dumps(gallery_photos,ensure_ascii=False).replace('<','\\u003c')
body='<header class="page-intro shell thank-you-intro"><h1>Thank You.</h1><p class="intro">Thank you for visiting PourHouseLife, to our friends and family who encourage every chapter, and especially to the generous people who lend a hand, share their knowledge, and help us along the road.</p></header><div class="shell thank-you-content">'+support_player+'</div><script type="application/json" id="expedition-photos">'+photo_data+'</script>'
page('support/index.html','Thank You',body,'Thank you to everyone who follows and supports PourHouseLife.','Thank You',article=True)
print('Built 14 static pages in',ROOT)
