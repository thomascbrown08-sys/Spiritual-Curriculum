/* Seeing and Believing — Toggle System */
(function () {
  const TOGGLES = [
    { id: 'toggle-facilitator', cls: 'hide-facilitator', key: 'sb-facilitator', def: '0' },
    { id: 'toggle-deepdive',    cls: 'hide-deepdive',    key: 'sb-deepdive',    def: '1' },
    { id: 'toggle-cultural',    cls: 'hide-cultural',    key: 'sb-cultural',    def: '1' },
    { id: 'toggle-nuance',      cls: 'hide-nuance',      key: 'sb-nuance',      def: '1' },
    { id: 'toggle-pilgrim',     cls: 'hide-pilgrim',     key: 'sb-pilgrim',     def: '1' },
    { id: 'toggle-plain',       cls: 'hide-plain',       key: 'sb-plain',       def: '1' },
  ];

  function applyState(t, checked) {
    document.body.classList.toggle(t.cls, !checked);
    try { localStorage.setItem(t.key, checked ? '1' : '0'); } catch(e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    TOGGLES.forEach(function (t) {
      const el = document.getElementById(t.id);
      if (!el) return;
      // Restore saved state, falling back to per-toggle default
      let saved = t.def;
      try { saved = localStorage.getItem(t.key) ?? t.def; } catch(e) {}
      el.checked = saved === '1';
      applyState(t, el.checked);
      el.addEventListener('change', function () { applyState(t, el.checked); });
    });

    // Mark active sidebar link
    const path = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.sidebar a').forEach(function (a) {
      if (a.getAttribute('href') === path) a.classList.add('active');
    });
  });
})();
