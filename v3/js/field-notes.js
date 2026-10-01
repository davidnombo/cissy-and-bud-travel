// Runs on Field Note photo frames and the read-only Thank You gallery player.
const photoData = document.querySelector('#expedition-photos');
if (photoData) {
  const photos = JSON.parse(photoData.textContent);
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const controllers = new Map();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { controllers.get(entry.target).visible = entry.isIntersecting; });
  }, { threshold: 0.05 });

  document.querySelectorAll('[data-photo-frame]').forEach(frame => {
    const img = frame.querySelector('img');
    const caption = frame.querySelector('.frame-caption');
    const count = frame.querySelector('.frame-count');
    const pause = frame.querySelector('[data-pause]');
    const state = { index: Number(frame.dataset.start), paused: motion.matches, visible: false, busy: false };
    const fitFrame = (width, height, source) => {
      frame.classList.toggle('is-portrait', height > width);
      frame.querySelector('.frame-image').style.setProperty('--frame-bg', `url("${source}")`);
    };
    fitFrame(Number(img.getAttribute('width')), Number(img.getAttribute('height')), img.currentSrc || img.src);
    const updatePause = () => {
      pause.textContent = state.paused ? 'Resume photos' : 'Pause photos';
      pause.setAttribute('aria-label', state.paused ? 'Resume this photo frame' : 'Pause this photo frame');
    };
    async function advance(direction, automatic = false) {
      if (state.busy || (automatic && (state.paused || !state.visible || document.hidden))) return;
      state.busy = true;
      state.index = (state.index + direction + photos.length) % photos.length;
      const next = photos[state.index];
      const preload = new Image();
      preload.src = '../assets/photos/' + next.src;
      try {
        await preload.decode();
        // Keep the current photo if the reader paused or left during loading.
        if (automatic && (state.paused || !state.visible || document.hidden)) return;
        img.src = preload.src;
        img.alt = next.alt;
        img.width = preload.naturalWidth;
        img.height = preload.naturalHeight;
        fitFrame(preload.naturalWidth, preload.naturalHeight, preload.src);
        caption.textContent = next.caption;
        count.textContent = `${state.index + 1} / ${photos.length}`;
      } catch {
        // A failed download never replaces a working photo with a broken one.
      } finally {
        state.busy = false;
      }
    }
    frame.querySelector('.frame-controls').hidden = false;
    pause.addEventListener('click', () => { state.paused = !state.paused; updatePause(); });
    frame.querySelector('[data-previous]').addEventListener('click', () => { state.paused = true; updatePause(); advance(-1); });
    frame.querySelector('[data-next]').addEventListener('click', () => { state.paused = true; updatePause(); advance(1); });
    motion.addEventListener('change', () => { state.paused = motion.matches; updatePause(); });
    updatePause();
    state.advance = advance;
    controllers.set(frame, state);
    observer.observe(frame);
  });
  setInterval(() => { controllers.forEach(state => state.advance(1, true)); }, 3000);
}
