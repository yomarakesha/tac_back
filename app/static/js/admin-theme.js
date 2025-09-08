(function() {
  try {
    // Инициализация быстрого поиска по текущей таблице
    document.addEventListener('DOMContentLoaded', function() {
      var table = document.querySelector('table.table');
      if (!table) return;
      if (document.querySelector('#quickListSearch')) return;
      var container = document.createElement('div');
      container.style.margin = '8px 0 12px';
      var input = document.createElement('input');
      input.type = 'search';
      input.placeholder = 'Быстрый поиск по видимой таблице...';
      input.className = 'form-control';
      input.id = 'quickListSearch';
      container.appendChild(input);
      table.parentNode.insertBefore(container, table);
      input.addEventListener('input', function(e) {
        var q = e.target.value.toLowerCase();
        var rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
          var text = row.innerText.toLowerCase();
          row.style.display = text.indexOf(q) !== -1 ? '' : 'none';
        });
      });
    });
  } catch (e) {
    console.error('admin-theme init error', e);
  }
})();


