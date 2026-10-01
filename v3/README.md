# PourHouseLife V3

Launch Build 1 adds the GWL featured Reel player/library, expands its photo pool to 14, and adds the evergreen Odyssey explainer. See [the completion report](LAUNCH-BUILD-1-REPORT.md) for scope, acceptance results, source tabs, and the Facebook embed restriction. The generator now emits 15 pages; run `python3 v3/scripts/check_launch.py` alongside the existing check.

A self-contained static preview. No framework, database, deployment, runtime content fetches, or iCloud dependencies. All 13 generated pages are checked in as editable output; edit the sources below and rebuild rather than editing generated HTML.

## Preview

From the repository root:

```sh
python3 -m http.server 8033 --bind 127.0.0.1
```

Open http://127.0.0.1:8033/v3/ . This preview was also opened in the Codex browser. On this Mac, the system Python/Git shims require unavailable Xcode tools; the working bundled Python is `/Users/davidbrown/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

## Editing and rebuilding

```sh
python3 v3/scripts/build.py
python3 v3/scripts/check.py
```

Both scripts use only Python's standard library. The build operates only inside V3. Pages work without JavaScript; JS adds the mobile disclosure menu and gallery filter. Without JS, navigation and all gallery photographs remain visible.

- `content/expeditions.json`: one source for expedition titles, quick facts, summaries, and hero images. Order is the actual V2 order: Mighty V Passage (2019), Northwest Hot-lap (2021), Great Western Loop (2023), Pacific Coast Highway (2024), Southern Colorado (August 2025), California (Winter 2025).
- `content/stories/*.html`: the six original V2 prose fragments, including every heading, paragraph, image reference, and caption. Keep individual editorial structures. Legacy photo references in these fragments are rewritten by the build to V3 assets.
- `content/about.html`: existing repository About prose.
- `content/faqs.json`: existing V2 FAQ questions and answers.
- `content/gallery.json`: ordered photos, captions, and expedition association. Add more entries here. Photography is presented at its native aspect ratio; selecting a photo opens the local optimized image.
- `content/odyssey.json`: editable headline, status, departure date and updates. This starts with **no updates**. Set status and narrative appropriately when departure actually happens; there is no automatic claim that travel has begun.
- `scripts/build.py`: shared page shell, navigation, footer, landing-page copy, and page templates. Header/footer edits propagate everywhere on rebuild.
- `css/site.css`: layout, colors, fonts, and contour wallpaper settings. Adjust `--topo-opacity`, `--topo-scale`, and `--topo-density` globally. `assets/public-domain-contours.svg` is abstract CC0 artwork rather than a map of real geography. Its nested lines do not cross.
- `css/field-notes.css`: long-form articles and quick facts.
- `assets/photos/`: optimized WebP copies, maximum 1600 pixels on the long edge. Original aspect ratios retained. `content/images.json` records dimensions and repository provenance. When adding a photo, add dimensions here too. The logo is copied byte-for-byte, unchanged.

## Adding an Odyssey dispatch

Append an object to `updates` in `content/odyssey.json`, then rebuild. Replace all example text with a real published update; this example is documentation only:

```json
{
  "date": "2026-10-18",
  "location": "Actual location",
  "title": "Actual dispatch title",
  "images": [{"src": "your-photo.webp", "alt": "Describe the photograph", "caption": "Optional caption"}],
  "paragraphs": ["First paragraph of the actual update.", "Optional second paragraph."],
  "social_url": "https://example.com/replace-with-real-reel",
  "map_url": "https://example.com/replace-with-real-map"
}
```

Image paths are relative to `assets/photos/` and must be registered in `content/images.json`. Omit optional links until real URLs exist. The builder requires HTTPS for them and escapes narrative text. Updates remain separate from the historical Field Notes. Their order follows the array; put the newest first if desired. Date, location, photos, paragraphs and optional links are rendered as static HTML.

## Photography and rotating Field Notes

All six authoritative public iCloud albums were verified in the browser. The original legacy endpoint returned zero items, but browser asset downloads succeeded. The saved selection currently contains **44 verified photographs**, not a complete import of every album: Mighty V 4, Northwest 7, Great Western Loop 8, Pacific Coast Highway 8, Southern Colorado 4, California 13. Videos are not included.

`content/photo-sources.json` preserves the authoritative album links. `content/images.json` records the original image filenames and expedition provenance. Imported, optimized WebP copies live in `assets/photos/field-notes/<slug>/`. Browser download URLs expire and are not used by the site.

`content/field-note-photos.json` is the separate, editable pool for each Field Note. It records the image path, useful alt text, and caption. Each story has four frames (one opening frame and three inline frames), with different starting photos. Existing prose is preserved, and additional frames are inserted at section breaks where needed. Original source captions remain in the archived story fragments; displayed captions follow the rotating photos.

`js/field-notes.js` rotates visible frames every three seconds. It preloads/decodes the next image before swapping, updates the caption and alt text together, skips hidden tabs/offscreen frames, and keeps the current photo if an image fails to load. Each frame has previous, next and pause/resume controls at the bottom. Manual stepping pauses that frame. Reduced-motion preferences start frames paused; Resume enables them. No-JavaScript readers see the initial images and captions. Fixed frames preserve aspect ratios using contain, so the prose does not move when portrait and landscape photos alternate.

### Gallery ownership

**David personally proofs and adds Gallery photos through explicit prompts.** Never add, replace, reorder or remove Gallery photos as a side effect of Field Note work or album imports. `content/gallery.json` is the sole explicit Gallery selection; a missing file is an error, not permission to seed a new Gallery. Existing Gallery HTML and content were verified unchanged by this implementation. See `AGENTS.md` for the persistent editorial rule.

## Deferred intentionally

Email signup/CRM and newsletter delivery, Patreon memberships, Printful/store, social account links and supported embeds, live maps, and a publishing UI. There are no fake forms, payment links, accounts, travel updates, or fabricated social URLs. The Odyssey dispatch list is the publishing extension point; the Support page has separate future membership and merchandise sections. Add email collection only after choosing and connecting a real service. A verified social account can be added to the shared footer and Odyssey template.

## Verification

- All 13 pages checked at 1440px desktop, 820px tablet, and 390px mobile; no horizontal overflow or broken image elements.
- Local links, assets and anchors resolve entirely within V3.
- All six source story fragments match the current V2 HTML exactly.
- Mobile menu opens/closes and closes with Escape; Gallery filters correctly.
- Original V2/root files and logo verified by SHA-256; no changes outside V3.
- Work stays on `v3`, uncommitted. No merge, push, deployment or live-site changes.
