document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('[data-director-input]');
  const addButton = document.querySelector('[data-director-add]');
  const tagsContainer = document.querySelector('[data-director-tags]');
  const hidden = document.querySelector('input[name="director_names"]');

  if (!input || !addButton || !tagsContainer || !hidden) return;

  const state = hidden.value
    ? hidden.value.split(',').map((item) => item.trim()).filter(Boolean)
    : [];

  const sync = () => {
    hidden.value = state.join(', ');
    tagsContainer.innerHTML = '';

    state.forEach((name) => {
      const tag = document.createElement('span');
      tag.className = 'director-tag';
      tag.innerHTML = `<span>${name}</span>`;

      const remove = document.createElement('button');
      remove.type = 'button';
      remove.setAttribute('aria-label', `Удалить ${name}`);
      remove.textContent = '×';
      remove.addEventListener('click', () => {
        const index = state.findIndex((item) => item.toLowerCase() === name.toLowerCase());
        if (index !== -1) {
          state.splice(index, 1);
        }
        sync();
      });

      tag.appendChild(remove);
      tagsContainer.appendChild(tag);
    });
  };

  const addCurrent = () => {
    const value = input.value.trim();
    if (!value) return;
    if (!state.some((item) => item.toLowerCase() === value.toLowerCase())) {
      state.push(value);
    }
    input.value = '';
    sync();
  };

  addButton.addEventListener('click', addCurrent);
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      addCurrent();
    }
  });

  sync();
});
