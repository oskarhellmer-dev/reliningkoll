(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- mobilmeny ---- */
  var btn = document.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        var links = document.querySelectorAll('.nav ul a');
        links.forEach(function (a, i) {
          a.style.opacity = '0';
          a.style.transform = 'translateY(24px)';
          a.style.transition = reduce ? 'none' : 'opacity .5s cubic-bezier(0.22,1,0.36,1) ' + (i * 60) + 'ms, transform .5s cubic-bezier(0.22,1,0.36,1) ' + (i * 60) + 'ms';
          requestAnimationFrame(function () { a.style.opacity = '1'; a.style.transform = 'none'; });
        });
      }
    });
  }

  /* ---- scroll-avslöjande ---- */
  var rv = document.querySelectorAll('.rv');
  if (rv.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      rv.forEach(function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      rv.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---- tagline-reveal: ord tänds ett i taget ---- */
  document.querySelectorAll('.reveal-tag').forEach(function (tag) {
    var text = tag.getAttribute('data-text') || tag.textContent;
    tag.textContent = '';
    var words = text.split(' ');
    words.forEach(function (w, i) {
      var s = document.createElement('span');
      s.className = 'w';
      s.textContent = w;
      tag.appendChild(s);
      if (i < words.length - 1) tag.appendChild(document.createTextNode(' '));
    });
    var spans = tag.querySelectorAll('.w');
    if (reduce || !('IntersectionObserver' in window)) {
      spans.forEach(function (s) { s.classList.add('on'); });
      return;
    }
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io2.disconnect();
        spans.forEach(function (s, i) {
          setTimeout(function () { s.classList.add('on'); }, i * 80);
        });
      });
    }, { threshold: 0.3 });
    io2.observe(tag);
  });

  /* ---- formulär ---- */
  document.querySelectorAll('form[data-lead]').forEach(function (f) {
    var msg = f.querySelector('.form-msg');
    f.addEventListener('submit', function (ev) {
      var ok = true;
      f.querySelectorAll('[required]').forEach(function (el) {
        if (!el.value || (el.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value))) {
          el.style.borderColor = '#c0392b'; ok = false;
        } else { el.style.borderColor = ''; }
      });
      if (!ok) {
        ev.preventDefault();
        if (msg) { msg.className = 'form-msg err'; msg.textContent = 'Fyll i de markerade fälten så skickar vi din förfrågan.'; }
        return;
      }
      if (msg) { msg.className = 'form-msg ok'; msg.textContent = 'Tack, din förfrågan skickas nu. Vi matchar dig med upp till 3 firmor i ditt område.'; }
    });
  });
})();
