# 2. Build test files on every branch except main

- Status: proposed
- Date: 2026-10-20

## Context and Problem Statement

The library website has no staging site. Every change to the CSS and JS goes
straight to patrons, with no way to check it on real pages first.

The plan is a test switch in the site's head code. Visiting any page with
`?test=on` saves a flag in that browser, and from then on the browser loads
test copies of the files, like `libguides-test.css`, instead of the live ones.
`?test=off` clears it. Patrons never see the test files.

That needs test copies of the files. This doc decides how they get made.

Three considerations were addressed:

Consideration 1: The file that was tested should be the file that goes live,
built the same way, by the same tools.

Consideration 2: Deploy is turned off. Every file reaches SpringShare by a
manual upload, so the process has to stay simple and hard to get wrong.

Consideration 3: The build only looked at the last commit in a push. A push
with several commits skipped files, a merge built nothing, and a deleted file
crashed the build ([#40](https://github.com/caltechlibrary/libguine/issues/40)).
A test-then-merge workflow depends on merges, so this had to be fixed.

## Decision Drivers

- Tested and live files come from the same build.
- No renaming files by hand before uploading.
- One long-lived `test` branch, not a new branch for every change.
- An urgent fix can still be tested when `test` has unfinished work.
- The same steps for libguides, libcal, and libanswers.

## Considered Options

1. Build test files locally
2. A "test" checkbox on the manual Run workflow button
3. Every push builds both test and live files
4. Main builds live files; every other branch builds test files

## Decision Outcome

**Chosen: Option 4.**

### Option 1: build test files locally — rejected

Fast, with no waiting on GitHub. But the test file comes from the local
computer, not GitHub. Local sass was 1.105.1, and comparing a local build to
`dist/libguides.css` showed different color formats and rule order. The file
that was tested would not be the file that went live.

### Option 2: a test checkbox on Run workflow — rejected

Builds on GitHub with the same tools, so it meets Consideration 1. But it
builds one file per run and needs a manual step on every change. Option 4 gets
the same result with no extra step.

### Option 3: both on every push — rejected

The test and live copies would always be the same, so test would only mean
"what was uploaded." Untested work on main would also produce a live file
ready to be pasted.

### Option 4: branch decides the name — chosen

| Push to | Builds | Example |
|---|---|---|
| `main` | Normal names | `dist/libguides.css` |
| Any other branch | `-test` names for CSS and JS | `dist/libguides-test.css` |

- This applies to every CSS and JS file: libguides, libcal, libanswers, admin,
  and chat.
- HTML files keep their normal names on every branch.
- Work happens on one long-lived `test` branch. A short-lived branch, like
  `hotfix`, also builds test files, so an urgent fix can be tested while `test`
  has unfinished work.
- Merges into main use `git merge --no-ff`. A fast-forward merge can leave
  GitHub's own `[skip ci]` commit as the newest one, and then nothing builds.

Changes made with this decision:

- `compile.yml` lists every file changed between where the branch was before
  the push and where it is after. On the first push of a new branch, it
  compares the branch to main instead.
- That list skips `dist/` and deleted files.
- `compile.yml` passes the branch name to `compile.py`.
- `compile.py` adds `-test` to CSS and JS file names on any branch except main.
- `compile.py` prints a note and moves on if a file is missing, instead of
  crashing.

## Consequences

Good:

- The tested file and the live file are built by the same tools from the same
  source. Only the name differs.
- No renaming before upload.
- Multi-commit pushes and merges now build every changed file.
- Deleting a file no longer crashes the build. This closes #40.

Bad, and accepted:

- **Everything on `test` goes to main together.** Unfinished work has to be
  finished or taken out before merging, or the fix goes on its own branch.
- **`test` falls behind main.** GitHub and the blog and notices robots save to
  main, so main is copied into `test` before every work session and before every push.
- **SpringShare holds one set of test files.** A hot fix branch's test files
  replace `test`'s, and `test`'s have to be uploaded again afterward.
- **HTML can't be tested this way.** Head code, headers, footers, templates,
  and widgets are pasted into fields, not loaded as files, so the switch does
  not cover them.
- **The head switch itself can't be tested this way.** It lives in the head.

## More Information

- Steps and commands: [`docs/deploy-steps.md`](../deploy-steps.md).
- Design system versions are chosen by the head switch, not by this build. With
  the flag on, it loads the unpinned design system (`/design-system/`). With it
  off, it loads a pinned minor version (`/design-system/v1.x/`). This only
  holds while the design system stays a separate file loaded from the head. If
  `libguides.scss` ever pulls design-system code in with `@use`, test and live
  would need different builds. See design-system ADR 0005.
