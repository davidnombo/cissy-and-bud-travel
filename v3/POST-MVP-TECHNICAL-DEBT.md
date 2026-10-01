# Post-MVP technical debt

## Thank You carousel and Gallery build coupling

The approved frozen MVP Thank You page (`support/index.html`) intentionally contains 12 photos. Preserve this rendered page unchanged for the MVP.

The build script (`scripts/build.py`) generates the Thank You carousel from the current `content/gallery.json`, which contains 55 photos. A full rebuild would therefore change the approved Thank You page.

After the MVP, decouple the Thank You carousel selection from the Gallery selection so a build can reproduce the approved 12-photo carousel. This is recorded technical debt only; no build or rendered-page change is authorized by this note.
