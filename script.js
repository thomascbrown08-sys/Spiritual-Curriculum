/* Seeing and Believing — Toggle System */
(function () {
  const TOGGLES = [
    { id: 'toggle-facilitator', cls: 'hide-facilitator', key: 'sb-facilitator' },
    { id: 'toggle-deepdive',    cls: 'hide-deepdive',    key: 'sb-deepdive'    },
    { id: 'toggle-cultural',    cls: 'hide-cultural',    key: 'sb-cultural'    },
    { id: 'toggle-nuance',      cls: 'hide-nuance',      key: 'sb-nuance'      },
    { id: 'toggle-pilgrim',     cls: 'hide-pilgrim',     key: 'sb-pilgrim'     },
    { id: 'toggle-plain',       cls: 'hide-plain',       key: 'sb-plain'       },
  ];

  function applyState(t, checked) {
    document.body.classList.toggle(t.cls, !checked);
    try { localStorage.setItem(t.key, checked ? '1' : '0'); } catch(e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    TOGGLES.forEach(function (t) {
      const el = document.getElementById(t.id);
      if (!el) return;
      // Restore saved state (default: shown)
      let saved = '1';
      try { saved = localStorage.getItem(t.key) ?? '1'; } catch(e) {}
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
