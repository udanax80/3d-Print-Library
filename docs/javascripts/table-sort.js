function bindSortableTables() {
  document.querySelectorAll("table.sortable").forEach(function (table) {
    if (table.dataset.sortBound === "1" || !table.tHead) return;
    table.dataset.sortBound = "1";
    Array.from(table.tHead.rows[0].cells).forEach(function (th, index) {
      th.addEventListener("click", function () {
        var asc = th.dataset.asc !== "1";
        Array.from(th.parentNode.cells).forEach(function (cell) {
          delete cell.dataset.asc;
        });
        th.dataset.asc = asc ? "1" : "0";
        var rows = Array.from(table.tBodies[0].rows);
        rows.sort(function (a, b) {
          var av = a.cells[index].dataset.sort || a.cells[index].textContent.trim();
          var bv = b.cells[index].dataset.sort || b.cells[index].textContent.trim();
          var an = Number(av);
          var bn = Number(bv);
          var cmp;
          if (av !== "" && bv !== "" && av !== "~" && bv !== "~" && !Number.isNaN(an) && !Number.isNaN(bn)) {
            cmp = an - bn;
          } else {
            cmp = av.localeCompare(bv, undefined, { numeric: true, sensitivity: "base" });
          }
          return asc ? cmp : -cmp;
        });
        rows.forEach(function (row) {
          table.tBodies[0].appendChild(row);
        });
      });
    });
  });
}

if (typeof document$ !== "undefined" && document$.subscribe) {
  document$.subscribe(bindSortableTables);
} else {
  document.addEventListener("DOMContentLoaded", bindSortableTables);
}
