// Select2
$(document).ready(function () {
  $(".select2").select2()
})

// Bootstrap tooltip
window.addEventListener("DOMContentLoaded", (event) => {
  const tooltipTriggerList = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
  );
  const tooltipList = Array.from(tooltipTriggerList).map(
    (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
  );
});
