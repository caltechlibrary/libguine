# Caltech Library Customizations for LibGuides CMS

Within LibGuides CMS we can customize things like HTML headers and templates, CSS files, and jQuery/JavaScript code at the system, group, and guide level.

While we cannot directly use the code from this repository with LibGuides, we still want to track our changes here to have a canonical version of the customizations for our site. The code stored here and/or any generated assets must be copied and pasted into various places within LibGuides that are appropriate for the specific snippets. This README file along with other inline comments will be the source for instructions on where to add code for our customizations.

## GitHub Actions

The [`.github/workflows/workflow.yml`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/workflow.yml) file defines a [GitHub Actions](https://docs.github.com/en/actions/quickstart) workflow that handles the compilation of CSS, HTML, and JavaScript artifacts (using [`workflow-compile.py`](https://github.com/caltechlibrary/libguine/blob/main/workflow-compile.py)) and the deployment of them to LibGuides CMS (using [`workflow-deploy.py`](https://github.com/caltechlibrary/libguine/blob/main/workflow-deploy.py)). The workflow is triggered when a relevant source file is committed and pushed to this repository. See [`ACTIONS.md`](https://github.com/caltechlibrary/libguine/blob/main/ACTIONS.md) for details.

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

## JavaScript

The [`custom.js`](https://github.com/caltechlibrary/libguine/blob/main/custom.js) file can be uploaded directly into LibGuides. The GitHub Actions workflow will automatically upload a modified custom JavaScript file to LibGuides.

## ~~[build.sh](https://github.com/caltechlibrary/libguine/blob/main/build.sh)~~ [DEPRECATED]

~~A POSIX-compliant shell script that will generate assets for the sections of the site that differ slightly between groups. For example, the main navigation menu will be the same between the Library and Archives groups, but the logos will be different. This build script overwrites a placeholder in a wrapper file like `header.shtm` with the contents of a file like `header-branding--archives.html` which contains the Archives logo.~~

~~The script is run like~~

<strike>

```sh
/bin/sh build.sh header archives
```

</strike>

~~with the `archives` argument being optional. If the group argument is not specified the script will supply default arguments for building both the archives and the dev group assets.~~

~~The optional arguments are useful with the [Run on Save extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave). A configuration example for building assets automatically upon save is like:~~

<strike>

```json
"emeraldwalk.runonsave": {
    "commands": [
        {
            "match": "/libguides-cms/(?<!(assets).*)[\\d\\w-]+\\.s?html?",
            "cmd": "/bin/sh ${workspaceFolder}/build.sh $(echo ${fileBasenameNoExt} | cut -d- -f1)"
        },
        {
            "match": "/libguides-cms/.*.scss",
            "cmd": "/bin/sh ${workspaceFolder}/build.sh scss"
        }
    ]
}
```

</strike>

## ~~[header.shtm](https://github.com/caltechlibrary/libguides-cms/blob/main/header.shtm)~~

~~Header content containing the main navigation menu for LibGuides CMS. This file includes a placeholder for inserting additional code like a logo, secondary navigation links, and site search using the `build.sh` script.~~

## ~~[header-branding--archives.shtm](https://github.com/caltechlibrary/libguides-cms/blob/main/header-branding--archives.shtm)~~

~~Snippet containing a Bootstrap `row` with a logo and links for the *Caltech Archives* group in LibGuides CMS. It can be combined with `header.shtm` by running `/bin/sh build.sh header archives` and will result in a file called `assets/header--archives.html` that can be pasted into the “Group Header” section of the “Header / Footer / Tabs / Boxes” tab of the *Caltech Archives* group edit page.~~

## ~~[header-branding--dev.shtm](https://github.com/caltechlibrary/libguides-cms/blob/main/header-branding--dev.shtm)~~

~~Snippet containing a Bootstrap `row` with a logo and links for the *dev* group in LibGuides CMS. It can be combined with `header.shtm` by running `/bin/sh build.sh header dev` and will result in a file called `assets/header--dev.html` that can be pasted into into the “Group Header” section of the “Header / Footer / Tabs / Boxes” tab of the *dev* group edit page.~~

## ~~[footer.shtm](https://github.com/caltechlibrary/libguides-cms/blob/main/footer.shtm)~~

~~Footer content for LibGuides CMS. Used with the `build.sh` script.~~

## ~~[footer-contact--archives.html](https://github.com/caltechlibrary/libguides-cms/blob/main/footer-contact--archives.html)~~

~~Snippet containing variable information for the *Contact Us* section of the Archives footer.~~

## ~~[footer-org--archives.html](https://github.com/caltechlibrary/libguides-cms/blob/main/footer-org--archives.html)~~

~~Snippet containing variable information for the *Our Organization* section of the Archives footer.~~

## ~~[footer-contact--dev.html](https://github.com/caltechlibrary/libguides-cms/blob/main/footer-contact--dev.html)~~

~~Snippet containing variable information for the *Contact Us* section of the DEV footer.~~

## ~~[footer-org--dev.html](https://github.com/caltechlibrary/libguides-cms/blob/main/footer-org--dev.html)~~

~~Snippet containing variable information for the *Our Organization* section of the DEV footer.~~

## ~~[head.shtm](https://github.com/caltechlibrary/libguides-cms/blob/main/head.shtm)~~

~~HTML `<head>` content for LibGuides CMS. Used with the `build.sh` script.~~

~~Paste the contents of the resulting `head--system.html` asset file into the “JS/CSS Code” field on the “Custom JS/CSS” tab under Admin ➜ Look & Feel.~~

~~The code in the asset file must be included on both guide edit pages and public pages. It relies on Bootstrap CSS and JS code. LibGuides includes Bootstrap in its own edit page stylesheets, so our customized Bootstrap code must only be included on public pages to avoid breaking the edit interface.~~

~~Additionally, the following `<link>` and `<script>` tags must be added into the Custom JS/CSS Code boxes for each Group:~~

<strike>

```html
<link rel="stylesheet" type="text/css" href="//libapps.s3.amazonaws.com/sites/64/include/bootstrap.min.css">
<script type="text/javascript" src="//libapps.s3.amazonaws.com/sites/64/include/bootstrap.min.js"></script>
```

</strike>

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
