# 3. Show home page blog posts from a scheduled job

- Status: accepted
- Date: 2026-08-24

## Context and Problem Statement

The library home page shows two blog posts. Editors need to be able to pin a
post to the first spot with the LibGuides "featured" flag, even when newer
posts exist.

SpringShare gives no way to do that:

- The LibGuides blog widget has no featured setting. It returns finished HTML
  with no featured marking, no per-post class, and nothing to filter on.
- The blog's Atom feed (`/blogs/rss.xml?blogConfigId=1449`) has no featured
  field. It only moves the featured post to the top of the list, which can't
  be told apart from "newest" when the featured post is also the newest.
- The public blog page (`/blog`) does mark it clearly: a
  `#featured_posts_container` block, and `featured` instead of `not-featured`
  on the post body. But the page is about 320 KB.

## Decision Drivers

- The featured post always takes the first spot.
- Visitors don't wait on a large page download.
- No requests from the visitor's browser to sites that block them (CORS).
- Follow a pattern the repository already uses.

## Considered Options

1. The SpringShare blog widget, rewritten into cards by `libguides.js`
2. Fetch the feed and blog page in the visitor's browser
3. Use content-buddy's `posts.json`
4. A scheduled job builds a small file, and a widget loads it

## Decision Outcome

**Chosen: Option 4.**

### Option 1: SpringShare widget plus a JS rewrite — rejected

This was the home page before. It can't tell which post is featured, because
the widget's output has nothing to tell it by.

### Option 2: fetch in the browser — rejected

Every visitor would download the 320 KB blog page, and the requests would run
into cross-site blocking.

### Option 3: content-buddy's `posts.json` — rejected

It is built from the feed and keeps only six fields, so it has no featured
marker. Editing it would gain nothing: the feed doesn't carry one either.

### Option 4: scheduled job — chosen

The same pattern as the LibCal notices
(`notices.yml` ➜ `fragments/notices/` ➜ GitHub Pages ➜ notices widget).

- `.github/workflows/blog.yml` runs `blog.py` every minute during work hours
  Monday–Friday, once a day otherwise, and on demand.
- `blog.py` reads the **blog page** for which post is featured, and the
  **feed** for titles, dates, content, and images of the recent posts.
- It writes `fragments/blog/library.html`, commits it if it changed, and
  publishes it to GitHub Pages through `fragments.yml`.
- `widget--blog-library-T1dHrHvS.html` on the home page loads that one small
  file.
- The featured post goes first, and the most recent post fills the other spot.
  With no featured post, the two most recent are shown.
- The markup matches what `libguides.js` built from the SpringShare widget, so
  the same card styles apply (`.cl-blog-widget` in `scss/libguides/_blog.scss`).

## Consequences

Good:

- The featured post is always first, whatever its date.
- Visitors download one small file.
- The slow, heavy reading happens in the job, where nobody waits on it.

Bad, and accepted:

- **It depends on the blog page's markup.** If SpringShare renames
  `#featured_posts_container` or the post classes, the job stops finding the
  featured post.
- **Changes reach the home page on the next run, not instantly.**
- **The old path is still in the code.** The SpringShare widget styles for
  `#s-lg-widget-1770820610259` and the `libguides.js` rewrite are kept as a
  way back. Remove both together once the new widget is settled.

## More Information

Traps found while building, each of which cost a full debugging round:

- **The feed and the page use different paths for the same post**
  (`/blogs/news/<slug>` and `/blog/<slug>`). Match on the last part of the URL,
  or the featured post shows twice.
- **Don't build the fragment locally and commit it.** The publish step only
  runs when the job's build differs from the committed file. A pre-built file
  means no difference, so nothing gets published. Let the job build it.
- **The first publish of a new fragment needs one manual run of
  `fragments.yml`.** Until then its URL returns 404.
- **`fragments.yml` checks out `ref: main`.** Without it, it publishes the
  state from before the calling job's commit.
- **The calling job must grant `contents: read`.** A called workflow can't use
  a permission the caller didn't give it, and the run fails before it starts.

[ADR 0004](0004-use-the-library-news-subject-to-choose-home-page-posts.md)
later added a subject filter on top of this.
