const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('#site-nav');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('open', !open);
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('open');
    });
  });
}

const revealItems = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add('visible'));
}

const signup = document.querySelector('#signup-form');
const formNote = document.querySelector('#form-note');
if (signup && formNote) {
  signup.addEventListener('submit', (event) => {
    event.preventDefault();
    formNote.textContent = 'Looks good—this is a prototype, so your address was not stored. We’ll connect the real signup before launch.';
    formNote.setAttribute('role', 'status');
    signup.reset();
  });
}

const play = document.querySelector('.play-button');
if (play) {
  play.addEventListener('click', () => {
    play.innerHTML = '<span aria-hidden="true">✓</span>';
    play.setAttribute('aria-label', 'Video placeholder acknowledged');
    const caption = play.parentElement.querySelector('p');
    if (caption) caption.textContent = 'Your first road reel will play here';
  });
}

const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();
