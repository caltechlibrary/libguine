// context hacks
document.addEventListener("DOMContentLoaded", function(event) {
  if (document.getElementById("s-lg-admin-command-bar")) {
    var admin = true;
    console.log("‼️ ADMIN");
    // remove elements that conflict with the LibGuides admin UI
    document.getElementById("custom-css").remove();
    document.getElementById("bootstrap-css").remove();
    // display admin-only content (elements have style="display:none" set)
    // see https://stackoverflow.com/a/54819633 regarding fancy syntax
    [...document.getElementsByClassName("c3-admin-show")].forEach(e => e.removeAttribute("style"));
  }
  else {
    var _public = true;
    console.log("‼️ PUBLIC");
    // add customized Bootstrap source to public-facing pages
    const bootstrap_js = document.createElement("script");
    bootstrap_js.id = "bootstrap-js";
    bootstrap_js.src = "//libapps.s3.amazonaws.com/sites/64/include/bootstrap.min.js";
    document.head.appendChild(bootstrap_js);
    // remove scroll-to-top javascript
    if (document.getElementById("s-lib-scroll-top")) {
      document.getElementById("s-lib-scroll-top").remove();
    }
    // move the breadcrumbs where we want them
    document.getElementById("c3-breadcrumbs").appendChild(document.getElementById("s-lib-bc"));
    // hours widget script cannot be included in footer code nor on admin pages
    var s_lc_tdh_3271_0 = new $.LibCalTodayHours( $("#s_lc_tdh_3271_0"), { iid: 3271, lid: 0 });
    // grab tokenized login link and rebuild elsewhere
    const login_link = document.createElement("a");
    login_link.setAttribute("href", document.getElementById("s-lib-footer-login-link").getElementsByTagName("a")[0].getAttribute("href"));
    login_link.setAttribute("aria-label", "Staff Login");
    login_link.innerHTML = `<i class="glyphicon glyphicon-log-in" aria-hidden="true"></i>`;
    document.getElementById("c3-footer-login").appendChild(login_link);
    // site search form does not show facets without hidden parameter
    // <input type="hidden" name="default_lg" value="1">
    if (document.getElementById("s-lg-srch-form")) {
      const default_lg = document.createElement("input");
      default_lg.setAttribute("type", "hidden");
      default_lg.setAttribute("name", "default_lg");
      default_lg.setAttribute("value", "1");
      document.getElementById("s-lg-srch-form").appendChild(default_lg);
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
            first_img.removeAttribute("vspace");
            first_img.removeAttribute("width");
            first_img.setAttribute("id", `img${i}`);
            items[i].innerHTML += first_img.outerHTML;
          }
          title_link.removeAttribute("target");
          items[i].innerHTML += `<h3>${title_link.outerHTML}</h3>`;
          items[i].innerHTML += `<div class="text-secondary">${post_date.textContent}</div>`;
          items[i].innerHTML += `<p>${first_p.innerHTML}</p>`;
        }
        // NOTE images are not loaded by the end of the mutation observation
        // TODO refactor as DRY code
        img0 = document.getElementById("img0");
        if (img0) {
          img0.addEventListener("load", function() {
            console.log(img0.naturalWidth);
            console.log(img0.naturalHeight);
            if (img0.naturalWidth <= 240) {
              img0.classList.add("pull-right");
            }
            else {
              img0.classList.add("center-block");
            }
          });
        }
        img1 = document.getElementById("img1");
        if (img1) {
          img1.addEventListener("load", function() {
            console.log(img1.naturalWidth);
            console.log(img1.naturalHeight);
            if (img1.naturalWidth <= 240) {
              img1.classList.add("pull-left");
            }
            else {
              img1.classList.add("center-block");
            }
          });
        }
        img2 = document.getElementById("img2");
        if (img2) {
          img2.addEventListener("load", function() {
            console.log(img2.naturalWidth);
            console.log(img2.naturalHeight);
            if (img2.naturalWidth <= 240) {
              img2.classList.add("pull-right");
            }
            else {
              img2.classList.add("center-block");
            }
          });
        }
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
     * with subjects:
     * ```html
     * <h2 class="s-lg-blog-header">Post Title</h2>
     * <span>
     * by Post Author on 
     * <span>[Post Date]</span>
     *  | 
     * <a href="/example#comments">Comments</a>
     * </span>
     * <br>
     * ```
     *
     * without subjects:
     * ```html
     * <h2 class="s-lg-blog-header">Post Title</h2>
     * <span>
     * by Post Author on 
     * <span>[Post Date]</span>
     * in 
     * <a>Subject 1</a>
     * , 
     * <a>Subject 2</a>
     * , 
     * <a>Subject 3</a>
     * </span>
     *  | 
     * <a href="/example#comments">Comments</a>
     * <br>
     * ```
     * 
     * @param {node} node The `span` immediately following `.s-lg-blog-header`.
     */
    function removeCommentsLink(node) {
      // console.log(node.nextSibling);
      if (node.nextSibling.nodeName === "BR") {
        if (node.lastChild.previousSibling.nodeName === "#text" && node.lastChild.previousSibling.nodeValue === " | ") {
          // console.log(node.lastChild.previousSibling);
          node.lastChild.previousSibling.remove();
        }
        else if (node.lastChild.nodeName === "A" && node.lastChild.href.endsWith("#comments")) {
          // console.log(node.lastChild);
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