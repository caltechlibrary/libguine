# Caltech Library Customizations for LibGuides CMS

Within LibGuides CMS we can customize things like HTML headers and templates, CSS files, and jQuery/JavaScript code at the system, group, and guide level.

While we cannot directly use the code from this repository with LibGuides, we still want to track our changes here to have a canonical version of the customizations for our site. The code stored here and/or any generated assets must be copied and pasted into various places within LibGuides that are appropriate for the specific snippets. This README file along with other inline comments will be the source for instructions on where to add code for our customizations.

## Table of Contents

- [Docs](#docs)
- [GitHub Actions](#github-actions)
- [CSS/SCSS](#cssscss)
- [HTML](#html)
  - [Templates & `<head>` Code](#templates--head-code)
  - [Header & Footer Code](#header--footer-code)
  - [Widget Code](#widget-code)
- [JavaScript](#javascript)
- [LibCal-based Notices](#libcal-based-notices)
- [Blog Posts on the Library Home Page](#blog-posts-on-the-library-home-page)

## Docs

- [`docs/deploy-steps.md`](https://github.com/caltechlibrary/libguine/blob/main/docs/deploy-steps.md): the steps and commands for testing and releasing CSS, JS, and HTML changes.
- [`docs/decisions/`](https://github.com/caltechlibrary/libguine/tree/main/docs/decisions): architecture decision records (ADRs) explaining why things work the way they do.

## GitHub Actions

We are using [GitHub Actions](https://docs.github.com/en/actions) to compile CSS, HTML, and JavaScript artifacts. Automated deployment to LibGuides CMS is turned off for now. Every built file is uploaded or pasted into LibGuides by hand.

The workflow is triggered when a relevant source file is committed and pushed to this repository. It builds every file changed in the push and commits the results to the `dist/` folder on the branch that was pushed. An individual file may also be rebuilt by manually running the [Deploy Components workflow](https://github.com/caltechlibrary/libguine/actions/workflows/deploy.yml) with the filename specified as an input parameter.

A push to `main` builds files with their normal names, like `libguides.css`. A push to any other branch builds CSS and JS files with `-test` names, like `libguides-test.css`, for checking changes on real pages before they go live. See [`docs/deploy-steps.md`](https://github.com/caltechlibrary/libguine/blob/main/docs/deploy-steps.md) for the steps.

See [`ACTIONS.md`](https://github.com/caltechlibrary/libguine/blob/main/ACTIONS.md) for details.

## CSS/SCSS

The CSS for the site is written with the [SCSS syntax of Sass](https://sass-lang.com/documentation/syntax#scss). It cannot be directly pasted anywhere that CSS is expected. When an `scss` file is modified, committed, and pushed to this repository, the compiled CSS is saved in `dist/`: `libguides.css`, `libcal.css`, `libanswers.css`, or `admin.css`, depending on which files changed. Changes in `scss/common/` rebuild all three site stylesheets.

Upload each compiled file to its own site. For LibGuides, use the “Upload Customization Files” section of the “Custom JS/CSS” tab under Admin ➜ Look & Feel. On branches other than `main`, the files are named with `-test`, like `libguides-test.css`.

## HTML

Note: Most HTML files have a comment header which includes a Last Modified date/time that can be updated automatically with the [Auto Time Stamp](https://github.com/lpubsppop01/vscode-auto-timestamp) extension for Visual Studio Code.

HTML files keep their normal names on every branch. They change the live site as soon as they are pasted, so paste them from `main`'s `dist/` folder.

### Templates & `<head>` Code

The built template files in `dist/` can be pasted directly into LibGuides.

The systemwide `<head>` code is split across [`head--system-css.html`](https://github.com/caltechlibrary/libguine/blob/main/head--system-css.html) and [`head--system-js.html`](https://github.com/caltechlibrary/libguine/blob/main/head--system-js.html). Paste the built files from `dist/` into the “JS/CSS Code” field on the “Custom JS/CSS” tab under Admin ➜ Look & Feel. Custom `<head>` code for a specific Group is not supported.

### Header & Footer Code

HTML code for the header and footer sections of the site is compiled from multiple snippets in an attempt to adhere to [the DRY principle](https://en.wikipedia.org/wiki/Don't_repeat_yourself).

We enter code into the systemwide header and footer sections only. Paste `dist/header--system.html` and `dist/footer--system.html` into the appropriate places in LibGuides.

### Widget Code

Code for widgets is kept in this repository, built into `dist/`, and pasted into LibGuides by hand.

Name the widget code file starting with `widget--` followed by a unique name and the `.html` extension. See [`widget--notices-library-4hoj8pnB.html`](https://github.com/caltechlibrary/libguine/blob/main/widget--notices-library-4hoj8pnB.html) as an example. Appending a [randomly generated string](https://www.random.org/strings/?num=1&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new) to the end of the name will help ensure uniqueness.

See [`.github/workflows/compile.py`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/compile.py) and the conditions related to widgets.

## JavaScript

[`libguides.js`](https://github.com/caltechlibrary/libguine/blob/main/libguides.js), [`libcal.js`](https://github.com/caltechlibrary/libguine/blob/main/libcal.js), and [`libanswers.js`](https://github.com/caltechlibrary/libguine/blob/main/libanswers.js) are copied into `dist/` with one comment line added at the top. Upload each file from `dist/` to its own site. For LibGuides, use the “Upload Customization Files” section of the “Custom JS/CSS” tab. On branches other than `main`, the files are named with `-test`, like `libguides-test.js`.

Run `node --check` on the file before uploading. A syntax error in the uploaded file fails silently on the site.

## LibCal-based Notices

In order to display temporal alert notices on the homepage we use a LibCal calendar and transform its RSS feed into HTML fragments that are pulled onto the page via a custom JavaScript widget. We needed to use this workflow to both overcome LibGuides aggressive caching of RSS feeds and to avoid CORS issues when trying to manipulate the feed directly with JavaScript.

A `LIBCAL_RSS_NOTICES_TODAY_URL` repository secret is required to store the URL for the calendar *day* feed. The URL is typically in the form of `https://libcal.caltech.edu/rss.php?cid=#️⃣&m=day` where the #️⃣ symbol stands for the numeric calendar ID.

We have created both a [Library notices widget](https://github.com/caltechlibrary/libguine/blob/main/widget--notices-library-4hoj8pnB.html) and an [Archives notices widget](https://github.com/caltechlibrary/libguine/blob/main/widget--notices-archives-YwAWE98Z.html) that will insert the fragments where needed. (To add these widgets in a LibGuides box, select Media / Widget, then the Reuse Existing Widget tab, and finally search for the unique widget name.)

See [Widget Code](#widget-code) for how this code is built and pasted into the site.

## Blog Posts on the Library Home Page

The library home page shows two blog posts: the featured post first, then the most recent post. With no featured post, it shows the two most recent. Only posts with the `Library News` subject appear.

The LibGuides blog widget cannot show a featured post, and the blog feed carries no featured marker or subjects. Instead, a scheduled GitHub Actions job in [`.github/workflows/blog.yml`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/blog.yml) runs [`.github/workflows/blog.py`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/blog.py), which reads the blog page for the featured post and subjects, and the blog feed for titles, dates, and content. It writes [`fragments/blog/library.html`](https://github.com/caltechlibrary/libguine/blob/main/fragments/blog/library.html) and publishes it with GitHub Pages. The [Library blog widget](https://github.com/caltechlibrary/libguine/blob/main/widget--blog-library-T1dHrHvS.html) on the home page loads that file.

To get a post on the home page, publish it without the `Library News` subject, then add the subject when it should appear. The next scheduled run picks it up; no code change is needed. To put a post in the first spot on the home page, also mark it as featured. A featured post without the `Library News` subject does not appear.

See [ADR 0003](https://github.com/caltechlibrary/libguine/blob/main/docs/decisions/0003-show-home-page-blog-posts-from-a-scheduled-job.md) and [ADR 0004](https://github.com/caltechlibrary/libguine/blob/main/docs/decisions/0004-use-the-library-news-subject-to-choose-home-page-posts.md) for why it works this way.
