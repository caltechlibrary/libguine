# 1. Record architecture decisions

- Status: accepted
- Date: 2026-10-20

## Context and Problem Statement

This repository has run the library website's LibGuides customizations for
years, and none of its decisions were written down. The reasoning lived in
commit messages, issues, Confluence, and people's memory. The next person to
look sees only the surviving design and is free to "simplify" it back into the
thing that already did not work.

Many of those decisions are workarounds for SpringShare limits. They look
strange without the limit they work around.

## Decision

Record architecturally significant decisions as ADRs in `docs/decisions/`,
following [MADR](https://adr.github.io/madr/), matching the conventions in
[design-system](https://github.com/caltechlibrary/design-system/tree/main/docs/decisions).

Conventions:

- One file per decision, `NNNN-title-in-kebab-case.md`, numbered sequentially
  in the order recorded (not the order decided).
- Each has a status: `proposed`, `accepted`, `rejected`, `deprecated`, or
  `superseded by ADR-NNNN`.
- **ADRs are immutable once accepted.** A decision that changes is not edited;
  a new ADR supersedes it, and the old one is marked as superseded.
- Corrections of *fact* about what shipped are fine to amend in place, dated
  and noted. Changes of *decision* get a new ADR.
- Record the rejected options and why. That is usually the most valuable part
  and the part that cannot be recovered from the code.
- Decisions made before 2026-10-20 can be recorded after the fact. Their date
  is the date the decision shipped, not the date it was written down.

## Consequences

Decisions with consequences outliving the change that introduced them get a
stable home.

Older decisions are only recorded when someone works in that area again. There
is no plan to backfill all of them.

`.gitignore` ignores `*.md`, so it has an exception for `docs/`.

