---
id: computing-software.software-engineering.git.rebase-and-history-repair
name: rebase-and-history-repair
category: computing-software
field: software-engineering
product: git
tags: [git, rebase, interactive-rebase, git-rebase-i, fixup, autosquash, squash, reflog, git-reflog, force-with-lease, force-if-includes, rerere, git-bisect, cherry-pick, reset, update-refs, stacked-branches, history-rewrite, merge-conflicts, git-range-diff, recovery]
level: practitioner
status: docs-checked
description: "Rewrite branch history safely with interactive rebase and autosquash, recover anything via reflog, push with --force-with-lease, reuse conflict fixes with rerere, bisect regressions."
sources:
  - https://git-scm.com/docs/git-rebase
  - https://git-scm.com/docs/git-commit
  - https://git-scm.com/docs/git-reflog
  - https://git-scm.com/docs/git-rerere
  - https://git-scm.com/docs/git-bisect
  - https://git-scm.com/docs/git-push
  - https://git-scm.com/docs/git-range-diff
  - https://git-scm.com/docs/git-reset
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rebase and history repair — clean history without ever losing work

**Goal:** turn a messy feature branch into a reviewable series of commits, update it
against main, and undo any mistake (bad rebase, wrong reset, deleted branch) in minutes.

## 0. Safety net first
- Nothing committed is lost for ~90 days: the reflog keeps reachable-entry history
  (`gc.reflogExpire`, default 90 days; unreachable entries `gc.reflogExpireUnreachable`,
  default 30 days). **Uncommitted** work is not protected — commit or `git stash` before
  any rewrite.
- Before a scary operation: `git branch backup/feat-$(date +%s)` — free and instant.
- Only rewrite commits that nobody else has built on. Shared branches (main, release)
  get `git revert`, not a rewrite.

## 1. Recommended config
```
git config --global rebase.autoSquash true      # honour fixup!/squash! automatically
git config --global rebase.autoStash true       # stash/unstash dirty tree around rebase
git config --global rebase.updateRefs true      # move stacked branch refs too (git >= 2.38)
git config --global rerere.enabled true         # record & replay conflict resolutions
git config --global merge.conflictStyle zdiff3  # shows the base in conflicts (also available: diff3)
git config --global push.useForceIfIncludes true
```

## 2. Fixups the cheap way
While working, don't amend old commits by hand. Commit the correction targeted at the
commit it belongs to:
```
git commit --fixup=<sha>          # becomes "fixup! <subject>"
git commit --fixup=amend:<sha>    # also replaces the message
git commit --fixup=reword:<sha>   # message only
git rebase -i --autosquash origin/main
```
The todo list arrives pre-sorted; just save.

## 3. Interactive rebase
`git rebase -i origin/main` (or `HEAD~N`). Todo verbs: `pick`, `reword`, `edit`,
`squash` (merge messages), `fixup` (drop message; `fixup -C` takes this one's message),
`drop`, `exec <cmd>`, `break`. Useful patterns:
- Run tests on every commit: `git rebase -i --exec "make test" origin/main` — stops at
  the first commit that fails, so each commit stays bisectable.
- Split a commit: mark `edit`, then `git reset HEAD^`, `git add -p`, commit pieces,
  `git rebase --continue`.
- Rebase onto a new base, keeping only your commits:
  `git rebase --onto main old-base feature`.
- Abandon cleanly at any time: `git rebase --abort`. Skip a now-empty commit: `--skip`.
- Compare before/after the rewrite: `git range-diff origin/feat...HEAD` (or
  `git range-diff ORIG_HEAD...HEAD` right after).

## 4. Conflicts and rerere
With `rerere.enabled`, every resolution is recorded under `.git/rr-cache` and replayed
when the same conflict reappears (repeated rebases of a long-lived branch). Recorded
resolutions are applied but still left for you to `git add` unless
`rerere.autoUpdate=true`. Wrong recorded fix? `git rerere forget <path>`.

## 5. Recovery with the reflog
```
git reflog                 # HEAD's history: "rebase (finish)", "reset: moving to"...
git reflog show feature    # a single branch's history
git reset --hard HEAD@{5}  # or a sha from the list; ORIG_HEAD = pre-rebase/reset tip
```
- Deleted branch: find its last sha in `git reflog` and `git branch feature <sha>`.
- Dropped stash: `git fsck --unreachable | grep commit` then inspect with `git show`.
- Prefer `git reset --keep` over `--hard` when you have local edits you want to keep.

## 6. Pushing rewritten history
`git push --force-with-lease --force-if-includes`. Plain `--force-with-lease` compares
against your *remote-tracking ref*, which a background `git fetch` (IDE auto-fetch)
silently updates — making the lease useless. `--force-if-includes` (git >= 2.30) also
checks that the remote tip is in your local reflog. Never plain `--force`.

## 7. Bisect in brief
```
git bisect start <bad> <good>
git bisect run ./test.sh   # exit 0 good, 1-124/126-127 bad, 125 = skip (untestable)
git bisect reset
```
About log2(N) steps: ~10 for 1,000 commits. `git bisect skip` (or exit code 125 from the script) for unbuildable commits.

## Gotchas
- `git pull` with rebase on a branch where a teammate force-pushed: use
  `git pull --rebase` — it uses the fork point to drop the old copies of rewritten
  commits; a merge pull duplicates them.
- Rebasing a branch containing merges flattens them; use `--rebase-merges` to keep the shape.
- `--autosquash` matches on the subject line; rewording the target first orphans the fixup.
- Reflogs are local: a colleague's lost commit is only recoverable on *their* clone
  (or from the server's reflog/backup, if enabled).
- `git stash` entries are not in `git reflog` HEAD; they live in `git reflog stash`.

## Verify
- [ ] `git log --oneline origin/main..HEAD` shows one logical change per commit, no `fixup!` left.
- [ ] `git range-diff` confirms the final tree change matches intent (no lost hunks).
- [ ] Every commit builds/tests (`rebase --exec` passed).
- [ ] Pushed with `--force-with-lease --force-if-includes`, not `--force`.
- [ ] You can name the reflog entry that would restore the pre-rebase state.
- [ ] `rerere.enabled` is on for long-lived branches.

Related: computing-software.software-engineering.code-review.reviewing-a-diff

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the Git 2.30 and 2.38 release notes. Confirmed: reflog expiry defaults (`gc.reflogExpire` 90 days, `gc.reflogExpireUnreachable` 30 days); `--fixup=[amend|reword:]`, todo verbs including `fixup -C`, `exec`, `break`, `--exec`, `--onto`, `--rebase-merges`, `--update-refs` with `rebase.updateRefs` (2.38 release notes); `rebase.autoSquash`, `rebase.autoStash`, `rerere.enabled`, `rerere.autoUpdate` (default false), `git rerere forget`; `push.useForceIfIncludes` and `--force-if-includes` (2.30 release notes) and the remote-tracking-ref weakness of plain `--force-with-lease`; `git range-diff <rev1>...<rev2>`; `git reset --keep`; `git bisect run` exit codes (0 good, 1-127 except 125 bad, 125 skip); the stash reflog and the `git fsck --unreachable` recovery recipe (git-stash); rebase assumes `--fork-point` when the upstream is configured. Removed as unconfirmed: the version gate for `zdiff3`, the third-party `git absorb` remark and the note on signed commits being re-signed.

Method: documentation only; no commands were run.
