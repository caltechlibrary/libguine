# Deploy steps

For now (10/20/26), nothing in this repository deploys automatically. GitHub builds the files and
saves them to `dist/`. You upload or paste them into SpringShare by hand.

## The rule

- A push to **main** builds files with their normal names, like `libguides.css`.
- A push to **any other branch** builds CSS and JS files with `-test` names,
  like `libguides-test.css`.
- HTML files keep their normal names on every branch.
- Visiting a page with `?test=on` makes that browser load the `-test` files.
  `?test=off` turns it back off. Patrons never see the test files.

See [ADR 0002](decisions/0002-build-test-files-on-every-branch-except-main.md)
for why it works this way.

## Branches

- `main` holds what is live, or ready to go live.
- `test` is the one long-lived branch for everyday work. It is never deleted.
- A short-lived branch, like `hotfix`, is only for urgent fixes when `test`
  has unfinished work. Delete it after it merges.

## Before each development session

```
git switch main
git pull
git switch test
git pull
git merge main
git push
```

- The first `git pull` gets the changes GitHub and the blog and notices robots
  saved to main.
- The second `git pull` gets the `-test` files GitHub saved to `test`.
- `git merge main` copies main's changes into `test`.
- `git push` sends the updated `test` to GitHub.

## Before every push to test

While on `test`:

```
git pull
git merge origin/main
git push
```

- `git pull` gets the files GitHub saved after your last push to test. It also
  downloads main's latest changes.
- `git merge origin/main` copies those main changes into `test`.
- If you skip `git pull`, GitHub refuses the push.

## Merging into main

Two ways to do it. Both make a merge commit, which is what starts the build of
the live files.

### On the GitHub website

1. Open a pull request from `test` into `main`.
2. Check that the title does not contain `[skip ci]`. GitHub skips the build
   when it does.
3. Merge with **Create a merge commit**. Not "Squash and merge" or "Rebase and
   merge": both skip the build.
4. Wait for the Deploy Components run to finish on main (Actions tab).
5. On your computer:
   ```
   git switch main
   git pull
   ```

### On the command line

```
git switch main
git pull
git merge --no-ff test
git push
```

- `--no-ff` makes a new merge commit every time. Without it, the newest commit
  on main can be GitHub's own `[skip ci]` commit, and then nothing gets built.

Then wait for the Deploy Components run to finish on main (Actions tab), and:

```
git pull
```

## Copying main back into test

```
git switch test
git pull
git merge main
git push
```

## CSS and JS changes

These can be checked on real pages before they go live.

1. On `test` branch, edit the source: `scss/`, `*.scss`, `libguides.js`,
   `libcal.js`, `libanswers.js`, or `chat.css`.
2. Commit and push:
   ```
   git add .
   git commit -m "describe the change"
   git pull
   git merge origin/main
   git push
   ```
3. Wait for the Deploy Components run to finish on `test` (Actions tab), then:
   ```
   git pull
   ```
4. Upload the `-test` files from `dist/` to SpringShare, for example
   `dist/libguides-test.css` and `dist/libguides-test.js`.
5. Open a real page with `?test=on` and check the change.
6. If it needs more work, go back to step 1.
7. When it passes, follow [Merging into main](#merging-into-main).
8. Upload the live files from `dist/`, for example `dist/libguides.css` and
   `dist/libguides.js`.
9. Follow [Copying main back into test](#copying-main-back-into-test).

## HTML changes

This covers head code, headers, footers, templates, and widgets. The test
switch cannot check these. They change the live site as soon as they are
pasted.

1. On `test` branch, edit the source file.
2. Commit and push:
   ```
   git add .
   git commit -m "describe the change"
   git pull
   git merge origin/main
   git push
   ```
3. Follow [Merging into main](#merging-into-main).
4. Paste the built file from `dist/` into its SpringShare field. Head code goes
   in the "JS/CSS Code" field on the "Custom JS/CSS" tab under
   Admin ➜ Look & Feel.
5. Check the live site.
6. Follow [Copying main back into test](#copying-main-back-into-test).

Paste from main's `dist/`, never from the `test` branch. The repo file is what
gets pasted next time, so main must match what is live.

## Hot fixes while test has unfinished work

Everything on `test` goes to main together when it merges. If `test` has
unfinished work that is already pushed, make the fix on its own branch.

1. Save your work on `test`:
   ```
   git add .
   git commit -m "describe the change"
   ```
2. Start the fix branch from main:
   ```
   git switch main
   git pull
   git switch -c hotfix
   ```
3. Make the fix, then commit and push:
   ```
   git add .
   git commit -m "describe the fix"
   git push -u origin hotfix
   ```
   - `-u origin hotfix` creates the branch on GitHub. Later pushes on this
     branch only need `git push`.
4. For CSS or JS only: wait for the Deploy Components run to finish on `hotfix`
   (Actions tab), then:
   ```
   git pull
   ```
   Upload the `-test` files from `dist/` and check with `?test=on`.
5. Merge into main, one of two ways.

   **On the GitHub website:**
   1. Open a pull request from `hotfix` into `main`.
   2. Check that the title does not contain `[skip ci]`.
   3. Merge with **Create a merge commit**.
   4. Click **Delete branch** on the pull request.
   5. Wait for the Deploy Components run to finish on main (Actions tab).
   6. On your computer:
      ```
      git switch main
      git pull
      git branch -d hotfix
      ```
      - `git branch -d hotfix` deletes the branch from your computer.

   **On the command line:**
   ```
   git switch main
   git pull
   git merge --no-ff hotfix
   git push
   ```
   - `--no-ff` makes a new merge commit, so the build runs.

   Wait for the Deploy Components run to finish on main (Actions tab), then:
   ```
   git pull
   git branch -d hotfix
   git push origin --delete hotfix
   ```
   - `git branch -d hotfix` deletes the branch from your computer.
   - `git push origin --delete hotfix` deletes it from GitHub.
6. Upload or paste the live files from `dist/`.
7. Follow [Copying main back into test](#copying-main-back-into-test).
8. SpringShare holds one set of test files, and the fix replaced them. Upload
   `test`'s `-test` files from `dist/` again before you keep testing.

### If copying main into test reports a conflict in dist/

The hot fix branch and `test` each built their own `-test` files, so git may
not know which to keep. Keep `test`'s version, while on `test`:

```
git status
git checkout --ours -- dist/
git add dist/
git commit --no-edit
git push
```

- `git status` lists the conflicted files. Only use these steps if every one
  is in `dist/`.
- `git checkout --ours -- dist/` keeps `test`'s version of each file.
- `git add dist/` marks the conflicts as fixed.
- `git commit --no-edit` finishes the merge with git's default message.

## If uncommitted work is in the way

If you need to switch branches but your changes are not ready to commit, save
them aside:

```
git stash
```

Switch branches and do what you need. Then come back and restore the work:

```
git switch test
git stash pop
```

Stash only holds uncommitted work. It cannot hold back work that is already
committed or pushed.

## Rebuilding one file by hand

On GitHub, open Actions ➜ Deploy Components ➜ Run workflow.

- Pick the branch under "Use workflow from". Main builds normal names. Any
  other branch builds `-test` names.
- Enter the source file name, for example `libguides.scss` or `libguides.js`.
