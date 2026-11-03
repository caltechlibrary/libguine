# 5. Use the library footer on Archives pages

- Status: accepted
- Date: 2026-02-11

## Context and Problem Statement

The Archives pages in LibGuides had their own footer, with the Archives email,
phone number, name, and logo. It was built from three Archives versions of
the footer parts:

- `footer--contact-archives.html`
- `footer--links-archives.html`
- `footer--idea-statement-archives.html`

The Archives is part of the library. A separate footer made its LibGuides
pages look like a separate site. The website committee approved combining
them, so the Archives uses the same footer as the main library website.

## Considered Options

1. Keep a separate Archives footer on the Archives pages
2. Use the library footer on the Archives pages

## Decision Outcome

**Chosen: Option 2.**

### Option 1: separate Archives footer — rejected

It treats the Archives as its own site.

### Option 2: library footer — chosen

- The Archives pages in LibGuides use the library footer
  (`dist/footer--system.html`).
- The Archives pages keep their own header and menu. Only the footer is
  shared.

## Consequences

Good:

- The Archives pages look like the rest of the library website.
- One LibGuides footer to paste and maintain.

Bad, and accepted:

- **The Archives contact details are no longer in the footer** of the Archives
  LibGuides pages, but they are on the Archives
  [Visitor Information](https://library.caltech.edu/archives/access/visit)
  page instead. 

## More Information

- **Headers and footers build differently on purpose.** `compile.py` builds a
  header for every group in the `LIBGUIDES_GROUPS` secret, but a footer for
  `system` only. Don't add an Archives footer back.
- `archives` stays in the secret. Deploy uses it for the Archives header.
- The change went live on 2026-02-11. The Archives footer files stayed in the
  repo, and the build kept making `dist/footer--archives.html` (last on
  2026-10-12), until it was removed on 2026-11-03.
