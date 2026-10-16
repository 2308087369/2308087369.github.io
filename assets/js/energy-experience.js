/* Subtle reveal effects; all content remains readable without JavaScript. */
(function () {
  const content = document.querySelector('.page__content');
  if (!content || !('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const targets = content.querySelectorAll(':scope > :not(.energy-hero):not(.energy-focus)');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -24px' });
  targets.forEach((target) => observer.observe(target));
}());
