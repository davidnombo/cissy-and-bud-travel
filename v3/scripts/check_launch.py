#!/usr/bin/env python3
"""Check the remaining Launch Build content and removal invariants."""
from pathlib import Path
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    return json.loads((ROOT / 'content' / (name + '.json')).read_text())

gwl = (ROOT / 'field-notes/great-western-loop.html').read_text()
trip = next(t for t in load('expeditions') if t['slug'] == 'great-western-loop')
assert f'<h1>{trip["title"]}</h1>' in gwl and trip['dek'] in gwl
assert 'shell story-photo' not in gwl
assert gwl.count('data-photo-frame') == 3
assert '<iframe' not in gwl and 'facebook.com/reel' not in gwl and 'data-reels' not in gwl
assert not (ROOT / 'field-notes/great-western-loop-reels.html').exists()
assert len(load('field-note-photos')['great-western-loop']) == 146

explainer = (ROOT / 'odyssey/what-the-hell-is-the-odyssey.html').read_text()
normalized = ' '.join(html.unescape(re.sub('<[^>]+>', ' ', explainer)).lower().split())
for paragraph in load('odyssey-explainer')['paragraphs']:
    if paragraph.startswith('PRIUS V →'): continue
    assert ' '.join(paragraph.lower().split()) in normalized, paragraph
for vehicle in ['Prius V', 'Town &amp; Country', 'Sprinter 4x4', 'Alaska']:
    assert f'<li>{vehicle}</li>' in explainer
assert 'href="./#dispatches"' in explainer
assert 'href="what-the-hell-is-the-odyssey.html"' in (ROOT / 'odyssey/index.html').read_text()
assert '<iframe' not in explainer
print('PASS: GWL player, video links, and opening carousel removed; three photo frames, 146 photos, full Odyssey draft, and navigation.')
