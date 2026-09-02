document.addEventListener("DOMContentLoaded", function(event) {

  // move the breadcrumbs to the footer
  const breadcrumbs = document.getElementById("s-lc-public-bc");
  breadcrumbs.removeAttribute("id");
  [...breadcrumbs.getElementsByTagName("li")].forEach(e => e.classList.remove("s-lc-desktop-only"));
  document.getElementById("footer-breadcrumbs").appendChild(breadcrumbs);

  // include the hours widget code in the JS/CSS field;
  // scripts cannot be added to the footer field alongside the HTML
  var s_lc_tdh_3271_0 = new $.LibCalTodayHours( $("#s_lc_tdh_3271_0"), { iid: 3271, lid: 0 });

  // create a (hard-coded) login link for the footer
  const login_link = document.createElement("a");
  login_link.setAttribute("href", "https://libcal.caltech.edu/admin");
  login_link.setAttribute("aria-label", "Staff Login");
  login_link.innerHTML = '<i class="fa fa-sign-in" aria-hidden="true"></i>';
  document.getElementById("footer-login").appendChild(login_link);

});

// move focus into the header search field when its dropdown opens,
// and back to the toggle when it closes
// NOTE registered on document at parse time; this file is injected
// dynamically, so DOMContentLoaded may already have fired
const SEARCH_TOGGLE = '.branding .dropdown-toggle[aria-label="Toggle Search"]';
document.addEventListener("shown.bs.dropdown", function(event) {
  const toggle = event.target.closest?.(SEARCH_TOGGLE);
  if (!toggle) return;
  toggle.closest(".dropdown").querySelector('input[type="search"]')?.focus();
});
document.addEventListener("hidden.bs.dropdown", function(event) {
  const toggle = event.target.closest?.(SEARCH_TOGGLE);
  if (!toggle) return;
  const dropdown = toggle.closest(".dropdown");
  const active = document.activeElement;
  if (dropdown.contains(active)) {
    toggle.focus();
  } else if (!active || active.contains(dropdown)) {
    toggle.focus({ preventScroll: true });
  }
});

