// Demo-only behaviour for the static copy of financialfixationllc.com.
// The original contact forms post to WordPress, which doesn't exist here, so
// submissions are intercepted and a notice is shown instead.
(function () {
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || !form.classList || !form.classList.contains('elementor-form')) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    var note = form.querySelector('.demo-form-note');
    if (!note) {
      note = document.createElement('p');
      note.className = 'demo-form-note';
      note.setAttribute('role', 'status');
      note.style.cssText = 'margin:12px 0 0;padding:10px 14px;border-radius:6px;background:#fff4d6;color:#5a4300;font-size:14px;width:100%';
      form.appendChild(note);
    }
    note.textContent = 'Demo site: form submissions are turned off on this preview.';
  }, true);
})();
