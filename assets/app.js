(function () {
  'use strict';

  /* ---- mobilmeny ---- */
  var nav = document.querySelector('.nav');
  var btn = document.querySelector('.menu-btn');
  if (nav && btn) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('open') && !nav.contains(e.target)) {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  }

  /* ---- blankett ---- */
  document.querySelectorAll('form[data-lead]').forEach(function (f) {
    var msg = f.querySelector('.form-msg');
    f.addEventListener('submit', function (ev) {
      var ok = true;
      f.querySelectorAll('[required]').forEach(function (el) {
        var bad = !el.value || (el.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value));
        if (bad) { el.setAttribute('aria-invalid', 'true'); ok = false; }
        else { el.removeAttribute('aria-invalid'); }
      });
      if (!ok) {
        ev.preventDefault();
        if (msg) {
          msg.className = 'form-msg err';
          msg.textContent = 'Fyll i de markerade fälten så skickar vi din förfrågan.';
        }
        var first = f.querySelector('[aria-invalid="true"]');
        if (first) first.focus();
        return;
      }
      if (msg) {
        msg.className = 'form-msg ok';
        msg.textContent = 'Tack, din förfrågan skickas nu. Vi matchar dig med upp till tre firmor i ditt område.';
      }
    });
  });
})();
