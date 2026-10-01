# Launch Build 1 completion report

Implemented in the existing V3 generator and page shell. No redesign or replacement of V3. Read the complete **CODEX — Launch Build 1**, **GWL — Reel Manifest**, and **Odyssey — What the Hell Is It?** tabs in the canonical [Travel Website document](https://docs.google.com/document/d/1OMwGhB2TrD_c_27f9swq8rNOOe6qPIHiiAvWXZk-XNg/edit?tab=t.hzzsfkvlpoha) before editing.

## 1. Files, components, and pages

- Updated `scripts/build.py` to integrate the scoped components and emit 15 pages; added reusable renderers in `scripts/launch_build.py`.
- Added canonical content snapshots: `content/gwl-reels.json` (including the complete supplied embed markup) and `content/odyssey-explainer.json` (the complete article draft).
- Added page-scoped `css/launch-build.css` and single-player selector behavior in `js/reels.js`.
- Updated `field-notes/great-western-loop.html`; added `field-notes/great-western-loop-reels.html`.
- Added `odyssey/what-the-hell-is-the-odyssey.html`; added its entry link to `odyssey/index.html`.
- Expanded only the GWL entry in `content/field-note-photos.json`; registered six new optimized images in `content/images.json` and documented import status in `content/photo-sources.json`. New assets are `assets/photos/field-notes/great-western-loop/launch-{00,05,06,09,10,11}.webp`.
- Updated the existing `scripts/check.py` for three GWL in-story frames after hero removal; added `scripts/check_launch.py` for launch acceptance invariants.

## 2. GWL featured player

The title/subtitle and all story copy are preserved. The oversized rotating hero is replaced with one vertical Facebook iframe, using the exact supplied canonical embed source. Grand Prismatic Spring is initially selected. Five title/play-icon selection controls appear in this exact order: Grand Prismatic Spring, Theodore Roosevelt National Park, Two Medicine, Triceratops Dig, Great Western Loop Recap. Selection updates the same iframe, accessible title, visible title, external fallback link, and selected state. No autoplay parameter is added; the full canonical iframe permissions are retained (permission alone does not request autoplay). Keyboard Enter/Space work. Mobile selections scroll horizontally within their own container. “See All Reels” leads to the library.

**External limitation:** Opening the exact Grand Prismatic Spring embed directly returned Facebook's message: “This video can't be embedded because it may contain content owned by someone else.” Embedded playback could not be verified. The canonical URL is preserved, and “Watch on Facebook” is visible above the player. This restriction cannot be resolved by changing the site's selection UI. Do not interpret the local selection tests as proof that all 30 Facebook videos are playable.

## 3. GWL Reels Library

One active player and all 30 public titles in chronological order. Internal IDs remain 01–04 and 06–31 in data; none are displayed to visitors. Exact manifest URLs and iframe sources are retained. The library starts with the first chronological item. Selection changes the single player and brings it into view without animation. Includes a clear return link to the GWL Field Note. No other trip libraries were created.

## 4. Photography

The existing public GWL iCloud album was accessible. Downloaded candidates were visually checked, including comparison with the eight original photos. Added six distinct full-size photographs, yielding **14 total**. Existing eight images, order, captions, and assets remain intact. Several other downloads failed or yielded only small thumbnails; this is a broader selection, not a complete ~60-photo import.

New images retain aspect ratio, are at most 1600 pixels on the long edge, and are saved as metadata-free WebP with meaningful alt text/captions. Existing in-story frame positions, cropping, three-second timing, manual controls, reduced-motion handling, offscreen/hidden-tab pauses, lazy loading, and one-image-ahead decoding remain unchanged. Only three initial story images are represented as image elements; the pool is local data, not 14 eagerly loaded images. Gallery selection and Gallery HTML are untouched.

## 5. Evergreen Odyssey explainer

Full canonical draft, with heading capitalization adapted to V3 typography and the vehicle sequence presented as a simple progression graphic. Includes the planning language “About 52 Weeks,” “Roughly 50,000 Miles,” and “Key West to Deadhorse,” plus “Go Small. Go Now.” and “Positioning the Van for Launch.” Preserves the brief cancer reference, Alaska objective, and Deadhorse caveat. Linked from the current Odyssey page and ends at its existing dispatches anchor. No Week 0, weekly system, current-location card, GPS, or precise live location was added.

The geographic map is **deferred under the brief's permitted fallback**. A three-chapter route-plan panel presents the canonical broad itinerary without asserting unverified geography or drawing over water.

## 6. Deviations and assumptions

- Facebook's default Reel embed restriction prevents full playback acceptance; selection and fallback links work.
- The larger album is partially imported: 14 reviewed photos, not the complete album.
- Accurate geographic vector map deferred; route-plan panel used instead.
- The manifest supplies no thumbnail images. Used accessible title/play-icon selection cards, as allowed by the brief's “thumbnail/selection control” wording; no unrelated photos or fabricated video stills.
- Preserved the current GWL subtitle's exact sentence case/punctuation rather than changing it to the brief's title-case rendering.
- Existing dispatches are the return destination because the weekly architecture is explicitly out of scope.

## 7. Acceptance results

| Check | Result |
| --- | --- |
| GWL title/subtitle preserved | Pass |
| Oversized opening rotating photo removed | Pass; three in-story frames retained |
| Grand Prismatic default; no autoplay | Correct default/source and no autoplay request; actual playback remains unverified |
| Five featured selections in exact order switch one player | Pass; all five tested in browser, with one selected state and one iframe |
| See All Reels navigation | Pass |
| All 30 manifest entries chronological; no 05 or renumbering | Pass |
| Library has one active iframe | Pass |
| Existing GWL story preserved below videos | Pass; source comparison passes |
| In-story photo controls | Pass; Next changes image/count and pauses automatic rotation |
| Broader source used if accessible | Pass with partial-import limitation; 8 → 14 |
| Canonical Odyssey explainer and links | Pass; entire draft checked |
| Desktop/mobile layouts | Pass at 1280px desktop and 390px embedded document width; no horizontal document overflow on all three new/changed experiences |
| Mobile featured strip | Pass; 324px container with 1233px scrollable contents, page width stays 390px |
| Mobile library selection | Pass; Theodore Roosevelt selection updates active title |
| No precise live location exposed | Pass |
| No unrelated pages/content redesigned | Pass; SHA-256 comparison with pre-edit snapshot confirms all existing HTML except GWL and Odyssey landing unchanged |

The browser viewport override did not take effect, so mobile checks used a temporary same-origin 390px iframe document. The temporary harness was removed after testing. This verifies responsive layout in Chromium, not physical iPhone/Safari playback.

Automated checks passed:

```sh
python3 v3/scripts/check.py
python3 v3/scripts/check_launch.py
```

All 15 pages have valid local links/assets/anchors and image alt text/dimensions. All six archived source stories remain byte-for-byte identical to their existing V2 sources. Baseline hashes also confirm unchanged shared styling, photo-rotation JavaScript, logo, Gallery, homepage, Field Notes listing, and five other trip pages.

## 8. Preview locally

From the repository root:

```sh
python3 v3/scripts/build.py
python3 -m http.server 8033 --bind 127.0.0.1
```

On this Mac use `/Users/davidbrown/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` if the system Python shim is unavailable. The preview server is already running.

- [GWL Field Note](http://127.0.0.1:8033/v3/field-notes/great-western-loop.html)
- [GWL Reels Library](http://127.0.0.1:8033/v3/field-notes/great-western-loop-reels.html)
- [What the Hell Is the Odyssey?](http://127.0.0.1:8033/v3/odyssey/what-the-hell-is-the-odyssey.html)

Try all five featured controls, use See All Reels, select early/middle/late library entries, and test the three story photo frames. Use Watch on Facebook when the embed is restricted. Follow the Odyssey entry and return links. Changes are local and uncommitted; no deployment was performed.

## Playback follow-up — incomplete

The first implementation kept only the canonical src and reconstructed the iframe, omitting Facebook’s autoplay/clipboard permissions, inline style, and frameborder. The player now renders the complete canonical embed (adding only an accessible title), and selections mount a fresh iframe with that Reel’s exact attributes. The interface and styling are unchanged. The launch checker now compares the complete attribute set and canonical markup instead of incorrectly requiring removal of autoplay permission.

Retested Grand Prismatic Spring, Theodore Roosevelt National Park, and Two Medicine in the local player. All three selections mount one iframe with the right canonical source, but none provided playable controls in the in-app browser. Separate minimal local pages containing the unmodified manifest embeds also remained blank. Opening each exact Facebook plugin URL directly returned “This video can't be embedded because it may contain content owned by someone else.” This is evidence of the response in the current browser session, not proof of a permanent restriction or the cause of the earlier working/now failing difference.

Actual playback acceptance remains **FAILED / NOT COMPLETE**. The earlier working embed/browser has not yet been identified for comparison. Temporary diagnostic pages were removed. No unrelated page or styling changes were made in this follow-up.
