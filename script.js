const HERO_IMAGE_URL = 'https://nombo-api.fly.dev/attachments/d281f6b7-2b00-497c-b3a1-151f13e14e81/raw?token=1819392529746.a8f9145023bd1fda5b0723fc9c67e624ff1d5273ed8ff4b5222fe9b9718d9c1a';
const heroImage = document.querySelector('.hero-image');
if (heroImage) heroImage.style.backgroundImage = `url("${HERO_IMAGE_URL}")`;

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
