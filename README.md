# Caltech Library Customizations for LibGuides CMS

Within LibGuides CMS we can customize things like HTML headers and templates, CSS files, and jQuery/JavaScript code at the system, group, and guide level.

While we cannot directly use the code from this repository with LibGuides, we still want to track our changes here to have a canonical version of the customizations for our site. The code stored here and/or any generated assets must be copied and pasted into various places within LibGuides that are appropriate for the specific snippets. This README file along with other inline comments will be the source for instructions on where to add code for our customizations.

## Table of Contents

- [GitHub Actions](#github-actions)
- [CSS/SCSS](#cssscss)
- [HTML](#html)
  - [Templates & `<head>` Code](#templates--head-code)
  - [Header & Footer Code](#header--footer-code)
  - [Widget Code](#widget-code)
- [JavaScript](#javascript)
- [bootstrap/config.json](#bootstrapconfigjson)
- [LibCal-based Notices](#libcal-based-notices)

## GitHub Actions

We are using [GitHub Actions](https://docs.github.com/en/actions) to automate the compilation of CSS, HTML, and JavaScript artifacts and their deployment to LibGuides CMS.

Most commonly, the workflow is triggered when a relevant source file is committed and pushed to this repository. Additionally, an individual file may be recompiled and redeployed by manually running the [Deploy Components workflow](https://github.com/caltechlibrary/libguine/actions/workflows/deploy.yml) with the filename specified as an input parameter.

See [`ACTIONS.md`](https://github.com/caltechlibrary/libguine/blob/main/ACTIONS.md) for details.

## CSS/SCSS

The CSS for the site is written with the [SCSS syntax of Sass](https://sass-lang.com/documentation/syntax#scss). It cannot be directly pasted anywhere that CSS is expected. When an `scss` file is modified, committed, and pushed to this repositiory, the compiled `custom.css` file will be downloadable as part of the artifacts produced during the GitHub Actions workflow run. Additionally, the updated `custom.css` file will be uploaded to LibGuides automatically.

## HTML

### Templates & `<head>` Code

The contents of any of the template files in this repository can be pasted directly into LibGuides. The GitHub Actions workflow will automatically update any existing templates within LibGuides, provided they already exist. Automatic creation of new templates has not been implemented.

The contents of the [`head--system.html`](https://github.com/caltechlibrary/libguine/blob/main/head--system.html) file can be pasted directly into LibGuides, as well. The GitHub Actions workflow will automatically update modified systemwide `<head>` code within LibGuides. Currently, the workflow will not support custom `<head>` code for a specific Group.

### Header & Footer Code

HTML code for the header and footer sections of the site is compiled from multiple snippets in an attempt to adhere to [the DRY principle](https://en.wikipedia.org/wiki/Don't_repeat_yourself).

Currently, we enter code into the systemwide header and footer sections, as well as the group header and footer sections for Archives & Special Collections.

The GitHub Action workflow scripts identify which header and/or footer files have been modified and paste the correct compiled HTML into the appropriate places in LibGuides.

### Widget Code

Code for widgets can be created and updated through this repository and GitHub Actions.

Name the widget code file starting with `widget--` followed by a unique name and the `.html` extension. See [`widget--notices-library-4hoj8pnB.html`](https://github.com/caltechlibrary/libguine/blob/main/widget--notices-library-4hoj8pnB.html) as an example. Appending a [randomly generated string](https://www.random.org/strings/?num=1&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new) to the end of the name will help ensure uniqueness.

See [`.github/workflows/compile.py`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/compile.py) and [`.github/workflows/deploy.py`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/deploy.py) and the conditions related to widgets.

## JavaScript

The [`custom.js`](https://github.com/caltechlibrary/libguine/blob/main/custom.js) file can be uploaded directly into LibGuides. The GitHub Actions workflow will automatically upload a modified custom JavaScript file to LibGuides.

## [bootstrap/config.json](https://github.com/caltechlibrary/libguine/blob/main/bootstrap/config.json)

Custom Bootstrap 3 configuration file that can be uploaded on their [Customize and download](https://getbootstrap.com/docs/3.4/customize/) page to generate a full build of Bootstrap 3 with custom global settings.

Some of the overrides for our site are much more easily accomplished if we change the default settings at the Bootstrap level.

The `bootstrap.min.css` and `bootstrap.min.js` that are downloaded from the custom build site should be uploaded on the “Custom JS/CSS” tab of the Admin ➜ Look & Feel section of LibGuides in the “Upload Customization Files” section.

**NOTE:** There is a namespace conflict between the Bootstrap `tooltip()` function and the jQuery UI `tooltip()` function. Paste the following code that renames the Bootstrap function (and enables tooltips) at the end of the `bootstrap.min.js` file before uploading to LibGuides.

```javascript
var bsTooltip = $.fn.tooltip.noConflict();
$.fn.bs_tooltip = bsTooltip;
$(function() {
  $('[data-toggle="tooltip"]').bs_tooltip()
});
```

## LibCal-based Notices

In order to display temporal alert notices on the homepage we use a LibCal calendar and transform its RSS feed into HTML fragments that are pulled onto the page via a custom JavaScript widget. We needed to use this workflow to both overcome LibGuides aggressive caching of RSS feeds and to avoid CORS issues when trying to manipulate the feed directly with JavaScript.

A `LIBCAL_RSS_NOTICES_TODAY_URL` repository secret is required to store the URL for the calendar *day* feed. The URL is typically in the form of `https://libcal.caltech.edu/rss.php?cid=#️⃣&m=day` where the #️⃣ symbol stands for the numeric calendar ID.

We have created both a [Library notices widget](https://github.com/caltechlibrary/libguine/blob/main/widget--notices-library-4hoj8pnB.html) and an [Archives notices widget](https://github.com/caltechlibrary/libguine/blob/main/widget--notices-archives-YwAWE98Z.html) that will insert the fragments where needed. (To add these widgets in a LibGuides box, select Media / Widget, then the Reuse Existing Widget tab, and finally search for the unique widget name.)

The [Widget Code deployment workflow](#widget-code) can create and update this code in the site.
