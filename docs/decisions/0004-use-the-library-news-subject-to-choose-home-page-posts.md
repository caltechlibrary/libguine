# 4. Use the Library News subject to choose home page posts

- Status: accepted
- Date: 2026-09-29

## Context and Problem Statement

[ADR 0003](0003-show-home-page-blog-posts-from-a-scheduled-job.md) puts the
featured post and the most recent post on the library home page. Every
published post was a candidate.

Archives needs a post live on its blog on the 1st of the month, so a
newsletter link works, but not on the library home page until about two weeks
later.

SpringShare has no scheduling or visibility setting for this. The feed carries
no subjects, and there is no "hide from home page" flag anywhere.

## Decision Drivers

- Editors control it themselves, with no code change or deploy.
- A held-back post stays off the home page even if someone marks it featured.
- No extra work on old posts.

## Considered Options

1. A code change or a list of hidden posts for each held-back post
2. A LibGuides subject as an on/off switch

## Decision Outcome

**Chosen: Option 2.**

### Option 1: code change per post — rejected

Every held-back post would need a commit and a reminder to undo it two weeks
later.

### Option 2: subject as a switch — chosen

Only posts with the `Library News` subject reach the home page.

- Editors publish without the subject, then add `Library News` when the post
  should appear. The next scheduled run picks it up.
- **The rule applies to the featured post too.** Otherwise marking a held-back
  post as featured would put it on the home page anyway.
- To guarantee a post the first spot, give it `Library News` and mark it
  featured.

How it is built:

- `blog.py` sets `SUBJECT = "Library News"`.
- Subjects only appear in the **blog page** markup, never in the feed, so the
  job reads them from the page and matches posts to the feed by the last part
  of the URL.
- In the markup, several subjects sit comma-separated inside one link, and the
  featured block repeats its subject links. `blog.py` strips the commas and
  removes duplicates.

## Consequences

Good:

- Editors release a post on their own schedule.
- Nothing in the repo changes when a post is held back or released.

Bad, and accepted:

- **A post labeled late can miss the open spot.** It's dated when it was
  published, and recent posts are newest first, so a newer labeled post can
  take the spot. At one or two posts a month this is unlikely. The featured
  flag is the way to guarantee a spot.
- **The subject name is in the code.** Renaming `Library News` in LibGuides
  hides every post until `SUBJECT` in `blog.py` is updated.
- **Only the first page of the blog is read**, about 11 posts. A post labeled
  after it has dropped off that page is never found.

## More Information

- Old posts don't need the subject. Only two posts are ever shown, so older
  ones never reach the home page, labeled or not.
- LibGuides can filter the blog by subject with `?subjects%5B%5D=<id>`, as in
  `header--navbar-archives.html`. The job doesn't need it today, but it reaches past the
  first page if a future job needs one subject in depth. `Library News` is
  subject 215942.
