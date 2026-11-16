'use strict';
document.documentElement.classList.remove('no-js');

// Casual-copying deterrents only: public HTML and assets remain downloadable.
// Keep editable controls and the email fallback usable; do not trap normal navigation.
function allowsTextActions(target) {
  const element = target instanceof Element ? target : target?.parentElement;
  return Boolean(element?.closest('input, textarea, [contenteditable="true"], [data-copy-allowed]'));
}
for (const type of ['contextmenu', 'copy', 'cut', 'selectstart', 'dragstart']) {
  document.addEventListener(type, event => {
    if (!allowsTextActions(event.target)) event.preventDefault();
  });
}
document.addEventListener('keydown', event => {
  const key = event.key.toLowerCase();
  if (key === 'f12') {
    event.preventDefault();
    return;
  }
  if (allowsTextActions(event.target)) return;
  const command = event.ctrlKey || event.metaKey;
  const inspect = command && event.shiftKey && ['i', 'j', 'c'].includes(key);
  const macInspect = event.metaKey && event.altKey && ['i', 'j', 'c', 'u'].includes(key);
  const copySourceOrSave = command && !event.altKey && ['c', 'x', 'u', 's'].includes(key);
  if (inspect || macInspect || copySourceOrSave) event.preventDefault();
});
const emailFallback = document.querySelector('.copy-status');
if (emailFallback) emailFallback.dataset.copyAllowed = '';

const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#site-nav');
function closeMenu(returnFocus = false) {
  navigation?.classList.remove('is-open');
  toggle?.setAttribute('aria-expanded', 'false');
  if (returnFocus) toggle?.focus();
}
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') closeMenu(true);
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});
window.matchMedia('(min-width: 851px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});

const filterButtons = document.querySelectorAll('[data-filter]');
filterButtons.forEach(button => button.addEventListener('click', () => {
  const category = button.dataset.filter;
  filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  let count = 0;
  document.querySelectorAll('[data-category]').forEach(project => {
    project.hidden = category !== 'all' && project.dataset.category !== category;
    if (!project.hidden) count++;
  });
  document.querySelector('#filter-status').textContent = `${count} projects shown.`;
}));

document.querySelector('.copy-email')?.addEventListener('click', async () => {
  const status = document.querySelector('.copy-status');
  try {
    await navigator.clipboard.writeText('gourabmal4@gmail.com');
    status.textContent = 'Email address copied.';
  } catch {
    status.textContent = 'Copy this address: gourabmal4@gmail.com';
  }
});

document.querySelector('.load-video')?.addEventListener('click', () => {
  const container = document.querySelector('[data-video]');
  const iframe = document.createElement('iframe');
  iframe.src = `https://www.youtube-nocookie.com/embed/${container.dataset.video}?autoplay=1`;
  iframe.title = 'CartPilot AI personal project walkthrough';
  iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
  iframe.allowFullscreen = true;
  container.replaceChildren(iframe);
  iframe.focus();
});

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navigation?.querySelectorAll('a[href*="#"]').forEach(link => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, {rootMargin: '-20% 0px -65% 0px'});
  document.querySelectorAll('main section[id]').forEach(section => observer.observe(section));
}
