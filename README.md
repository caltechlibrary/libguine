# Caltech Library customizations for LibGuides CMS

Within LibGuides CMS we can customize things like HTML headers and templates, CSS files, and jQuery/JavaScript code at the system, group, and guide level.

While we cannot directly use the code from this repository with LibGuides, we still want to track our changes here to have an official version of the customizations for our site. The code stored here and/or any generated assets must be copied and pasted into various places within LibGuides that are appropriate for the specific snippets. This README file along with other inline comments will be the source for instructions on where to add code for our customizations.

## [build.sh](https://github.com/caltechlibrary/libguides-cms/blob/main/build.sh)

A POSIX-compliant shell script that will generate assets for the sections of the site that differ slightly between groups. For example, the main navigation menu will be the same between the Library and Archives groups, but the logos will be different. This build script joins a file like `header-top-archives.html` which contains the Archives logo with the `header-wrapper.html` file that contains the `<header>` HTML element within which is a placeholder for the logo snippet and the full shared navigation menu.

## [header-wrapper.html](https://github.com/caltechlibrary/libguides-cms/blob/main/header-wrapper.html)

Header content containing the main navigation menu for LibGuides CMS. This file includes a placeholder for inserting additional code like a logo and top links using the `build.sh` script.

## [header-top-dev.html](https://github.com/caltechlibrary/libguides-cms/blob/main/header-top-dev.html)

Snippet containing a Bootstrap `row` with a logo and links for the *dev* group in LibGuides CMS. It can be combined with `header-wrapper.html` by running `/bin/sh build.sh header dev` and will result in a file called `assets/header-dev.html` that can be pasted into into the “Group Header” section of the “Header / Footer / Tabs / Boxes” tab of the *dev* group edit page.

## [footer-dev.html](https://github.com/caltechlibrary/libguides-cms/blob/main/footer-dev.html)

Footer content for the `dev` group in LibGuides CMS. Paste the contents of this file into the “Group Footer” section of the “Header / Footer / Tabs / Boxes” tab of the `dev` group edit page.

## [template-dev.html](https://github.com/caltechlibrary/libguides-cms/blob/main/template-dev.html)

Template content for the `dev` group in LibGuides CMS. Paste the contents of this file into the “Customize Homepage Templates” section of the “Templates” sub-tab of the “Look & Feel and Layout” tab when editing the `dev` group.

## [head-dev.html](https://github.com/caltechlibrary/libguides-cms/blob/main/head-dev.html)

HTML `<HEAD>` content for the `dev` group in LibGuides CMS. Paste the contents of this file into the “Public Pages Header/Footer Customization” section of the “Custom JS/CSS Code” tab when editing the `dev` group.

## [header-top-archives.html](https://github.com/caltechlibrary/libguides-cms/blob/main/header-top-archives.html)

Snippet containing a Bootstrap `row` with a logo and links for the *Caltech Archives* group in LibGuides CMS. It can be combined with `header-wrapper.html` by running `/bin/sh build.sh header archives` and will result in a file called `assets/header-archives.html` that can be pasted into the “Group Header” section of the “Header / Footer / Tabs / Boxes” tab of the *Caltech Archives* group edit page.

## [footer-archives.html](https://github.com/caltechlibrary/libguides-cms/blob/main/footer-archives.html)

Footer content for the `Caltech Archives` group in LibGuides CMS. Paste the contents of this file into the “Group Footer” section of the “Header / Footer / Tabs / Boxes” tab of the `Caltech Archives` group edit page.

## [template-archives.html](https://github.com/caltechlibrary/libguides-cms/blob/main/template-archives.html)

Template content for the `Caltech Archives` group in LibGuides CMS. Paste the contents of this file into the “Customize Homepage Templates” section of the “Templates” sub-tab of the “Look & Feel and Layout” tab when editing the `Caltech Archives` group.

## [head-archives.html](https://github.com/caltechlibrary/libguides-cms/blob/main/head-archives.html)

HTML `<HEAD>` content for the `Caltech Archives` group in LibGuides CMS. Paste the contents of this file into the “Public Pages Header/Footer Customization” section of the “Custom JS/CSS Code” tab when editing the `Caltech Archives` group.
