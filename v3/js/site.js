const menu = document.querySelector('.menu');
const nav = document.querySelector('#navigation');
menu.hidden = false;
document.documentElement.classList.add('js');
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
});
nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });
const filter = document.querySelector('#expedition-filter');
if (filter) {
  document.querySelector('.gallery-controls').hidden = false;
  const figures = [...document.querySelectorAll('[data-expedition]')];
  function update() {
    figures.forEach(figure => { figure.hidden = !!filter.value && figure.dataset.expedition !== filter.value; });
    document.querySelector('#gallery-count').textContent = `${figures.filter(f => !f.hidden).length} photographs`;
  }
  filter.addEventListener('change', update);
  update();
}

// Questions come from the same content source as the dedicated FAQ page.
const questionTeaser = document.querySelector('.faq-questions');
if (questionTeaser) {
  const questions = [...questionTeaser.querySelectorAll('.faq-question')];
  const control = document.querySelector('.faq-rotation');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reducedMotion.matches;
  let index = 0;
  let timer;
  const visibleCount = Math.min(3, questions.length);
  function renderQuestions() {
    questions.forEach((question, questionIndex) => {
      const visible = Array.from({ length: visibleCount }, (_, offset) => (index + offset) % questions.length).includes(questionIndex);
      question.classList.toggle('active', visible);
      question.setAttribute('aria-hidden', String(!visible));
    });
  }
  function restart() {
    clearInterval(timer);
    control.textContent = paused ? 'Resume questions' : 'Pause questions';
    if (!paused && !document.hidden) {
      timer = setInterval(() => {
        index = (index + visibleCount) % questions.length;
        renderQuestions();
      }, 3000);
    }
  }
  if (questions.length > 1) {
    control.hidden = false;
    control.addEventListener('click', () => { paused = !paused; restart(); });
    reducedMotion.addEventListener('change', () => { paused = reducedMotion.matches; restart(); });
    document.addEventListener('visibilitychange', restart);
    renderQuestions();
    restart();
  }
}
