const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('[data-menu-button]');
const nav = document.querySelector('[data-nav]');

const setHeaderState = () => header.classList.toggle('is-scrolled', window.scrollY > 30);
setHeaderState();
window.addEventListener('scroll', setHeaderState, { passive: true });

const closeMenu = () => {
  nav.classList.remove('is-open');
  menuButton.classList.remove('menu-active');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open menu');
  document.body.classList.remove('menu-open');
};

menuButton.addEventListener('click', () => {
  const isOpen = nav.classList.toggle('is-open');
  menuButton.classList.toggle('menu-active', isOpen);
  menuButton.setAttribute('aria-expanded', String(isOpen));
  menuButton.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
  document.body.classList.toggle('menu-open', isOpen);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));

const filters = document.querySelectorAll('[data-filter]');
const stories = document.querySelectorAll('[data-category]');
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(item => item.classList.toggle('is-active', item === button));
  const category = button.dataset.filter;
  stories.forEach(story => {
    story.hidden = category !== 'all' && story.dataset.category !== category;
  });
}));

const storyCopy = {
  launch: {
    kicker: 'The beginning · Story preview',
    title: 'Why we chose the road—and what we hope to find',
    body: `<p>There is a moment when a travel day becomes something bigger. The map is folded, the house is behind you, and the next several months are more question than plan.</p><p>Our version begins in California in October 2026. From there, we’ll follow warmer weather east—making room for the towns, meals, people, and detours that don’t appear on an itinerary.</p>`
  },
  revel: {
    kicker: 'Van life · Story preview',
    title: 'Making a Revel feel like home',
    body: `<p>A van asks you to be honest about what you need. Every object earns its place, every routine gets smaller, and the view outside becomes part of the living room.</p><p>This section will eventually share the practical details: our setup, the gear that works, the mistakes we make, and the small rituals that turn a parking spot into home.</p>`
  },
  table: {
    kicker: 'Roadside tables · Story preview',
    title: 'The best table might be outside',
    body: `<p>Travel stories often begin with scenery, but the ones we remember tend to end around a table. A local recommendation, an unexpected conversation, or something simple cooked beside the van can define a whole place.</p><p>Here we’ll collect the meals and people that become landmarks of their own.</p>`
  }
};

const dialog = document.querySelector('[data-story-dialog]');
document.querySelectorAll('[data-story]').forEach(button => button.addEventListener('click', () => {
  const story = storyCopy[button.dataset.story];
  dialog.querySelector('[data-dialog-kicker]').textContent = story.kicker;
  dialog.querySelector('[data-dialog-title]').textContent = story.title;
  dialog.querySelector('[data-dialog-body]').innerHTML = story.body;
  dialog.showModal();
}));
dialog.querySelector('[data-dialog-close]').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const box = dialog.getBoundingClientRect();
  const outside = event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
  if (outside) dialog.close();
});

const signupForm = document.querySelector('[data-signup-form]');
signupForm.addEventListener('submit', event => {
  event.preventDefault();
  const note = signupForm.querySelector('[data-form-note]');
  note.textContent = 'Thanks—this demo works. We’ll connect the real email list before launch.';
  note.classList.add('is-success');
  signupForm.reset();
});

document.querySelectorAll('[data-placeholder-link]').forEach(link => link.addEventListener('click', event => {
  event.preventDefault();
  link.textContent = 'Link coming soon';
}));

document.querySelector('[data-year]').textContent = new Date().getFullYear();
