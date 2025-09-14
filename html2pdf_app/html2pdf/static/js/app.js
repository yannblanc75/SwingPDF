/* static/js/app.js - interactions globales */

(() => {
  // Helper: debounce
  const debounce = (fn, delay = 250) => {
    let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), delay); };
  };

  // Helper: toast Bootstrap (fallback si container absent)
  function showToast(message, variant = 'success') {
    let container = document.querySelector('#toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container position-fixed top-0 end-0 p-3';
      document.body.appendChild(container);
    }

    const el = document.createElement('div');
    el.className = `toast align-items-center text-bg-${variant} border-0`;
    el.role = 'alert';
    el.ariaLive = 'assertive';
    el.ariaAtomic = 'true';
    el.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    `;
    container.appendChild(el);
    const t = new bootstrap.Toast(el, { delay: 2500 });
    t.show();
    el.addEventListener('hidden.bs.toast', () => el.remove());
  }

  // Enable all tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el);
  });

  // 1) Copier le lien (history)
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.js-copy-link');
    if (!btn) return;
    const url = btn.getAttribute('data-url');
    try {
      await navigator.clipboard.writeText(url);
      showToast('Lien copié dans le presse-papiers.', 'success');
      const tt = bootstrap.Tooltip.getInstance(btn);
      if (tt) { tt.setContent({ '.tooltip-inner': 'Copié !' }); btn.addEventListener('mouseleave', () => tt.hide(), { once:true }); }
    } catch (err) {
      showToast('Impossible de copier le lien.', 'danger');
      console.error(err);
    }
  });

  // 2) Filtre de l’historique
  const filterInput = document.querySelector('#history-filter');
  if (filterInput) {
    const clearBtn = document.querySelector('#clear-filter');
    const list = document.querySelector('#history-list');
    const items = list ? Array.from(list.querySelectorAll('[data-filename]')) : [];

    const applyFilter = () => {
      const q = filterInput.value.trim().toLowerCase();
      items.forEach(li => {
        const match = li.dataset.filename.toLowerCase().includes(q);
        li.style.display = match ? '' : 'none';
      });
    };
    filterInput.addEventListener('input', debounce(applyFilter, 100));
    if (clearBtn) clearBtn.addEventListener('click', () => { filterInput.value = ''; applyFilter(); filterInput.focus(); });
  }

  // 3) Compteurs de caractères sur les inputs/textarea (via maxlength)
  document.querySelectorAll('[data_counter="true"], input[maxlength].form-control, textarea[maxlength].form-control')
    .forEach(input => {
      const max = Number(input.getAttribute('maxlength')) || null;
      if (!max) return;

      const counter = document.createElement('div');
      counter.className = 'form-text text-end mt-1';
      counter.textContent = `0/${max}`;
      input.insertAdjacentElement('afterend', counter);

      const update = () => {
        const len = input.value.length;
        counter.textContent = `${len}/${max}`;
        if (len > max) counter.classList.add('text-danger'); else counter.classList.remove('text-danger');
      };
      input.addEventListener('input', update);
      update();
    });

  // 4) Auto-size des textarea
  document.querySelectorAll('textarea[data_autosize="true"]').forEach(ta => {
    const autosize = () => {
      ta.style.height = 'auto';
      ta.style.height = `${ta.scrollHeight + 2}px`;
    };
    ['input', 'change'].forEach(evt => ta.addEventListener(evt, autosize));
    setTimeout(autosize, 0);
  });

  // 5) Smooth scroll pour liens internes (optionnel)
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
})();
