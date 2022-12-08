document.addEventListener("DOMContentLoaded", function(event) {

  // move the breadcrumbs to the footer
  document.getElementById("footer-breadcrumbs").appendChild(document.querySelector("nav.s-la-breadcrumbs"));

  // include the hours widget code in the JS/CSS field;
  // scripts cannot be added to the footer field alongside the HTML
  var s_lc_tdh_3271_0 = new $.LibCalTodayHours( $("#s_lc_tdh_3271_0"), { iid: 3271, lid: 0 });

  // create a (hard-coded) login link for the footer
  const login_link = document.createElement("a");
  login_link.setAttribute("href", "https://libanswers.caltech.edu/admin");
  login_link.setAttribute("aria-label", "Staff Login");
  login_link.innerHTML = '<i class="fa fa-sign-in" aria-hidden="true"></i>';
  document.getElementById("footer-login").appendChild(login_link);

});
