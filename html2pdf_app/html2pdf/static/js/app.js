// static/js/app.js

// --- Normalisation pour recherche (accents, majuscules) ------------------
function normalizeText(s) {
  return (s || "")
    .toString()
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .trim();
}

// --- Historique : filtre temps réel -------------------------------------
function initHistoryFilter() {
  const input = document.querySelector("#history-filter");
  const list  = document.querySelector("#history-list");
  const clearBtn = document.querySelector("#history-clear");

  if (!input || !list) return;

  const items = Array.from(list.querySelectorAll("li[data-filename]"));
  items.forEach(li => {
    const name = li.getAttribute("data-filename") || li.textContent || "";
    li.dataset.search = normalizeText(name);
  });

  const noResultId = "history-no-result";

  function renderEmptyState(show) {
    let empty = document.getElementById(noResultId);
    if (show) {
      if (!empty) {
        empty = document.createElement("li");
        empty.id = noResultId;
        empty.className = "list-group-item text-muted";
        empty.textContent = "Aucun résultat.";
        list.appendChild(empty);
      }
    } else if (empty) {
      empty.remove();
    }
  }

  function applyFilter(q) {
    const nq = normalizeText(q);
    const tokens = nq.split(/\s+/).filter(Boolean);
    let visibleCount = 0;

    items.forEach(li => {
      const hay = li.dataset.search || "";
      const match = tokens.every(t => hay.includes(t));
      li.classList.toggle("d-none", !match);
      if (match) visibleCount++;
    });

    renderEmptyState(visibleCount === 0);
  }

  input.addEventListener("input", () => applyFilter(input.value));

  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      input.value = "";
      applyFilter("");
      input.blur();
    }
  });

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      input.value = "";
      input.focus();
      applyFilter("");
    });
  }

  applyFilter(input.value);
}

// --- Copie de lien dans l’historique ------------------------------------
function initCopyButtons() {
  document.querySelectorAll(".js-copy-link").forEach(btn => {
    btn.addEventListener("click", () => {
      const url = btn.dataset.url;
      if (!url) return;
      navigator.clipboard.writeText(url).then(() => {
        btn.textContent = "Copié !";
        setTimeout(() => (btn.textContent = "Copier le lien"), 1500);
      });
    });
  });
}

// --- Démarrage -----------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  initHistoryFilter();
  initCopyButtons();
});
