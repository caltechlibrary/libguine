// context hacks
document.addEventListener("DOMContentLoaded", function(event) {
  if (document.getElementById("s-lg-admin-command-bar")) {
    var admin = true;
    console.log("‼️ ADMIN");
    // remove elements that conflict with the LibGuides admin UI
    document.getElementById("libguides-css").remove();
    document.getElementById("bootstrap-css").remove();
    // display admin-only content (elements have style="display:none" set)
    // see https://stackoverflow.com/a/54819633 regarding fancy syntax
    [...document.getElementsByClassName("c3-admin-show")].forEach(e => e.removeAttribute("style"));
    // ensure all details elements are open
    [...document.querySelectorAll("details")].forEach(e => e.open = true);
    // expand all details elements inside the WYSIWYG editor
    const body = document.getElementsByTagName("body")[0];
    const config = { childList: true, subtree: true };
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (document.getElementById("cke_s-lg-editor-content")) {
          // jQuery
          // add custom CSS to WYSIWYG editor inside iframe
          var head = $(".cke_wysiwyg_frame").contents().find("head");
          var css = '<style>.cke_editable details > summary { display: list-item; cursor: pointer; } .cke_editable summary > h3 { display: inline-block; }</style>';
          $(head).append(css);
          // /jQuery
          const iframe = document.querySelector(".cke_wysiwyg_frame");
          iframe.addEventListener("load", () => {
            const childDoc = iframe.contentDocument;
            [...childDoc.querySelectorAll("details")].forEach(e => e.open = true);
          });
        }
      });
    });
    observer.observe(body, config);
    // customize admin ui for Digital Exhibits Thumbnails page;
    // remove hardcoded navigation elements, widen columns
    let digital_exhibits_introduction_row = document.querySelector(".digital-exhibits-thumbnails #c3-introduction-row");
    if (digital_exhibits_introduction_row) {
      digital_exhibits_introduction_row.firstElementChild.classList.add("col-md-12");
      digital_exhibits_introduction_row.firstElementChild.classList.remove("col-md-6");
      digital_exhibits_introduction_row.lastElementChild.remove();
    }
  }
  else {
    var _public = true;
    console.log("‼️ PUBLIC");
    // add customized Bootstrap JS to public-facing pages
    const bootstrap_js = document.createElement("script");
    bootstrap_js.id = "bootstrap-js";
    bootstrap_js.src = "//libapps.s3.amazonaws.com/sites/64/include/bootstrap.min.js";
    document.head.appendChild(bootstrap_js);
    // Remove Website CSS from `Guides` Group content.
    if (document.getElementById("s-lib-bc-group")) {
      if (document.getElementById("s-lib-bc-group").textContent == "Guides") {
        document.getElementById("libguides-css").remove();
      }
    }
    // remove scroll-to-top javascript
    if (document.getElementById("s-lib-scroll-top")) {
      document.getElementById("s-lib-scroll-top").remove();
    }
    if (document.getElementById("footer-wrapper")) {
      // move the breadcrumbs to the footer
      document.getElementById("footer-breadcrumbs").appendChild(document.getElementById("s-lib-bc"));
      // this javascript code for the hours widget cannot be added alongside the
      // HTML, instead it must be entered in a CSS/JS-specific field
      var s_lc_tdh_3271_0 = new $.LibCalTodayHours( $("#s_lc_tdh_3271_0"), { iid: 3271, lid: 0 });
      // grab tokenized login link and rebuild elsewhere
      const login_link = document.createElement("a");
      login_link.setAttribute("href", document.getElementById("s-lib-footer-login-link").getElementsByTagName("a")[0].getAttribute("href"));
      login_link.setAttribute("aria-label", "Staff Login");
      login_link.innerHTML = `<i class="fa fa-sign-in" aria-hidden="true"></i>`;
      document.getElementById("footer-login").appendChild(login_link);
    }
    // update page title
    const page_name = document.getElementById("s-lib-bc-page").textContent;
    const site_name = "Caltech Library";
    if (document.getElementById("s-lib-bc-group")) {
      const group_name = document.getElementById("s-lib-bc-group").textContent;
      if (document.body.classList.contains("c3-asc")) {
        document.title = `${page_name} - ${group_name} - ${site_name}`;
      }
      else {
        document.title = `${page_name} - ${site_name}`;
      }
    }
    else {
      document.title = `${page_name} - ${site_name}`;
    }
    // site search alert
    if (document.getElementById("s-lg-srch-cols")) {
      const search_alert = document.createElement("div");
      search_alert.id = "search-alert";
      search_alert.classList.add("alert", "alert-warning", "alert-dismissable");
      search_alert.setAttribute("role", "alert");
      search_alert.innerHTML = '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>Looking for a book, journal, database, or other resource? Try <a href="/libsearch">LibSearch</a> instead. You can also browse our <a href="/az.php">Databases List</a> or <a href="https://libanswers.caltech.edu/">FAQs</a>.';
      let parent = document.getElementById("s-lg-srch-cols").parentNode;
      let target = document.getElementById("s-lg-srch-cols");
      parent.insertBefore(search_alert, target);
    }
  }
  if (document.getElementById("tpl-web")) {
    if (document.getElementById("s-lg-guide-tabs") && !document.getElementById("s-lg-guide-tabs").firstElementChild.firstElementChild.classList.contains("active")) {
      var content = true;
      console.log("‼️ CONTENT");
      // hide landing-only elements from content pages
      [...document.getElementsByClassName("c3-content-hide")].forEach(e => e.classList.add("hidden"));
    }
    else {
      var landing = true;
      console.log("‼️ LANDING");
      // hide content-only elements from landing pages
      [...document.getElementsByClassName("c3-landing-hide")].forEach(e => e.classList.add("hidden"));
    }
  }
  if (document.getElementById("s-lg-blog-content")) {
    var blog = true;
    console.log("‼️ BLOG");
  }
  // COMPLEX CONDITIONS
  if (_public && document.getElementById("tpl-a-home")) {
    console.log("‼️ ARCHIVES HOME");
    const widget = document.getElementById("s-lg-widget-1653629897969");
    const config = { childList: true, subtree: true };
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        observer.disconnect();
        console.log(mutation.type);
        var items = widget.getElementsByTagName("ul")[0].getElementsByTagName("li");
        for (var i = 0; i < items.length; i++) {
          items[i].setAttribute("id", `blogpost${[i]}`);
          console.log(items[i]);
          let title_link = items[i].getElementsByTagName("a")[0];
          console.log(title_link);
          let post_date = items[i].getElementsByTagName("span")[0];
          console.log(post_date);
          let first_img = items[i].getElementsByTagName("img")[0];
          console.log(first_img);
          // TODO account for no p
          // TODO account for br inside p
          let first_p = items[i].getElementsByTagName("p")[0];
          console.log(first_p);
          let p_images = first_p.getElementsByTagName("img");
          while(p_images.length > 0) {
            p_images[0].parentNode.removeChild(p_images[0]);
          }
          // create element
          items[i].innerHTML = "";
          if (first_img) {
            first_img.removeAttribute("align");
            first_img.removeAttribute("border");
            first_img.removeAttribute("height");
            first_img.removeAttribute("hspace");
            first_img.removeAttribute("style");
            first_img.removeAttribute("vspace");
            first_img.removeAttribute("width");
            first_img.classList.add("blogpost-img");
            items[i].innerHTML += first_img.outerHTML;
          }
          title_link.removeAttribute("target");
          items[i].innerHTML += `<h3>${title_link.outerHTML}</h3>`;
          items[i].innerHTML += `<div class="text-secondary">${post_date.textContent}</div>`;
          items[i].innerHTML += `<p>${first_p.innerHTML}</p>`;
        }
        // NOTE images are not loaded by the end of the mutation observation
        // apply classes based on image size, orientation, and aspect ratio
        [...document.getElementsByClassName("blogpost-img")].forEach(e => e.addEventListener("load", function () {
          console.log(e.naturalWidth);
          console.log(e.naturalHeight);
          if (e.naturalWidth <= 240) {
            e.classList.add("img-xs");
          }
          else if (e.naturalWidth <= 535) {
            e.classList.add("img-sm");
          }
          if (e.naturalWidth / e.naturalHeight < 4/3) {
            e.classList.add("img-narrow");
          }
        }));
      });
    });
    observer.observe(widget, config);
  }
  else if (admin && landing) {}
  else if (admin && content) {}
  // else if (admin && blog) {} // custom <HEAD> code not added on blog admin
  else if (_public && landing) {
    // identify public-facing landing pages to CSS
    document.body.classList.add("c3-landing");
    // Digital Exhibits Thumbnails
    if (document.querySelector("#tpl-web.digital-exhibits-thumbnails")) {
      // TODO implement for all landing pages
      // wrap link from figcaption around figure
      [...document.getElementsByTagName("figure")].forEach(e => {
        let link = document.createElement("a");
        link.innerHTML = e.outerHTML;
        link.setAttribute("href", e.getElementsByTagName("a")[0].href)
        e.parentElement.insertBefore(link, e);
        e.remove();
      });
      // remove link from figcaption
      [...document.getElementsByTagName("figcaption")].forEach(e => {
        e.innerHTML = e.innerText;
      });
    }
  }
  else if (_public && content) {
    document.body.classList.add("c3-content");
    // remove the 'active' class from a dropdown parent if a child is active
    if (document.getElementById("c3-sidenav").getElementsByClassName("active dropdown")[0]) {
      if (document.getElementById("c3-sidenav").getElementsByClassName("active dropdown")[0].getElementsByClassName("active")[1]) {
        document.getElementById("c3-sidenav").getElementsByClassName("active dropdown")[0].classList.remove("active");
      }
    }
    // expand nested lists by removing dropdown classes
    [...document.getElementById("c3-sidenav").getElementsByClassName("dropdown")].forEach(e => e.classList.remove("dropdown", "clearfix"));
    [...document.getElementById("c3-sidenav").getElementsByClassName("pull-left")].forEach(e => e.classList.remove("pull-left"));
    [...document.getElementById("c3-sidenav").getElementsByClassName("dropdown-menu")].forEach(e => e.classList.remove("dropdown-menu"));
    [...document.getElementById("c3-sidenav").getElementsByClassName("dropdown-toggle")].forEach(e => e.remove());
    // save link for use if needed
    const link = document.querySelector(".c3-asc #c3-sidenav > ul > li:first-of-type a");
    // remove landing page links in Archives sidebar (jQuery)
    $(".c3-asc #c3-sidenav > ul > li:first-of-type a").contents().unwrap();
    // add custom sidebar menu title for Research Collections
    const sidenav = document.getElementById("c3-sidenav");
    const config = { attributes: true };
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        observer.disconnect();
        // NOTE custom guide classes added via admin ui
        // TODO refactor as DRY code
        if (document.querySelector("#c3-sidenav.g1230812 > ul")) {
          // first link was unwrapped; rewrap with the link (jQuery)
          $("#c3-sidenav.g1230812 > ul > li:first-of-type span").wrap(link);
          // add the new custom element
          const sidenav_title = document.createElement("li");
          sidenav_title.textContent = "Research Collections";
          document.querySelector("#c3-sidenav.g1230812 > ul").insertAdjacentElement('afterbegin', sidenav_title);
        }
        if (document.querySelector("#c3-sidenav.g1230813 > ul")) {
          // first link was unwrapped; rewrap with the link (jQuery)
          $("#c3-sidenav.g1230813 > ul > li:first-of-type span").wrap(link);
          // add the new custom element
          const sidenav_title = document.createElement("li");
          sidenav_title.textContent = "Explore Exhibits";
          document.querySelector("#c3-sidenav.g1230813 > ul").insertAdjacentElement('afterbegin', sidenav_title);
        }
      });
    });
    observer.observe(sidenav, config);
  }
  else if (_public && blog) {
    // NOTE unsure if this script will always run before main blog script;
    // #s-lg-blog-content is initially empty on the /blog page, but on blog
    // post pages it is populated with #s-lg-blog-posts and more
    /**
     * Removes a Comments link and its preceding text node.
     *
     * We want to remove the link to Comments and its preceding text node
     * containing a horizontal bar character (` | `). The markup is different
     * depending on whether the post contains subject tags or not.
     *
     * Example without subjects:
     * ```html
     * <h2 class="s-lg-blog-header">Post Title</h2>
     * <span>by Post Author on <span>[Post Date]</span> | <a href="/example#comments">Comments</a></span><br>
     * ```
     *
     * Example with subjects:
     * ```html
     * <h2 class="s-lg-blog-header">Post Title</h2>
     * <span>by Post Author on <span>[Post Date]</span> in <a>Subject 1</a>, <a>Subject 2</a>, <a>Subject 3</a></span> | <a href="/example#comments">Comments</a><br>
     * ```
     *
     * @param {node} node The span element immediately following the .s-lg-blog-header element.
     */
    function removeCommentsLink(node) {
      if (node.nextSibling.nodeName === "BR") {
        if (node.lastChild.previousSibling.nodeName === "#text" && node.lastChild.previousSibling.nodeValue === " | ") {
          node.lastChild.previousSibling.remove();
        }
        else if (node.lastChild.nodeName === "A" && node.lastChild.href.endsWith("#comments")) {
          node.lastChild.remove();
        }
      }
      else if (node.nextSibling.nodeName === "#text" && node.nextSibling.nodeValue === " | ") {
        // console.log(node.nextSibling);
        if (node.nextSibling.nextSibling.nodeName === "A" && node.nextSibling.nextSibling.href.endsWith("#comments")) {
          // console.log(node.nextSibling.nextSibling);
          node.nextSibling.nextSibling.remove();
          // console.log(node.nextSibling);
          node.nextSibling.remove();
        }
      }
    }
    if (document.getElementById("s-lg-blog-posts")) {
      console.log("‼️ BLOG POST");
      document.body.classList.add("blog-post");
      // console.log(document.getElementById("s-lg-blog-posts").querySelector(".s-lg-blog-header + span"));
      removeCommentsLink(document.getElementById("s-lg-blog-posts").querySelector(".s-lg-blog-header + span"));
    }
    else {
      console.log("‼️ BLOG LANDING");
      // /blog landing content is populated by another script
      const blog_content = document.getElementById("s-lg-blog-content");
      const config = { childList: true, subtree: true };
      const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
          observer.disconnect();
          // console.log(mutation.type);
          const blog_posts = document.getElementById("s-lg-blog-posts").getElementsByClassName("row");
          for (var i = 0; i < blog_posts.length; i++) {
            // console.log(blog_posts[i]);
            blog_posts[i].querySelectorAll(".s-lg-blog-header + span").forEach(node => removeCommentsLink(node));
          }
        });
      });
      observer.observe(blog_content, config);
    }
  }
});
// keep menu open upon non-link click within
$(document).ready(function() {
  $('.megatoggle').on({
    "click": function(e) { // handles click event
      // if megamenu or any child of megamenu is clicked
      if ($(e.target).is('.megamenu') || $(e.target).parents().is('.megamenu')) {
        this.closable = false // do not close it
        return;
      } else {
        this.closable = true; // else close it
      }
    },
    "hide.bs.dropdown": function() {
      return this.closable;
    } // save state
  });
});
