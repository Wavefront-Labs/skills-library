---
id: computing-software.software-engineering.git.scripting-refs-with-plumbing
name: scripting-refs-with-plumbing
category: computing-software
field: software-engineering
product: git
tags: [git, git-update-ref, for-each-ref, symbolic-ref, git-plumbing, git-scripting, rev-parse]
level: advanced
status: verified
description: "Write robust Git scripts with plumbing: for-each-ref formats, update-ref with old-value checks and transactions, symbolic-ref, rev-parse --verify, and avoiding porcelain parsing."
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-Git-References
  - https://git-scm.com/docs/git-for-each-ref
  - https://git-scm.com/docs/git-update-ref
  - https://git-scm.com/docs/git-symbolic-ref
  - https://git-scm.com/docs/git-rev-parse
  - https://git-scm.com/docs/git-show-ref
  - https://git-scm.com/docs/git-remote
  - https://git-scm.com/docs/git-push
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Scripting refs with plumbing

**Goal:** automation that keeps working across Git versions, locales and user configs,
by using plumbing commands with stable output instead of parsing porcelain.

## Reading refs
```bash
git rev-parse --verify --quiet refs/heads/main^{commit}   # sha or exit 1; no ambiguity
git rev-parse --abbrev-ref HEAD                            # current branch ("HEAD" if detached)
git symbolic-ref --short -q HEAD || echo detached
git for-each-ref --format='%(refname:short) %(objectname:short) %(upstream:short) %(upstream:track)' refs/heads/
git for-each-ref --sort=-creatordate --count=5 --format='%(refname:short) %(creatordate:iso)' refs/tags/
git for-each-ref --merged=main --format='%(refname:short)' refs/heads/   # merged branches
git show-ref --verify --quiet refs/heads/feature || echo "no such branch"
```
`%(refname:lstrip=2)`, `%(contents:subject)`, `%(objecttype)`, `%(*objectname)` (peeled tag
target) are commonly useful. `--shell`/`--python` quote values safely for eval.

## Writing refs safely
```bash
git update-ref refs/heads/release <new-sha> <expected-old-sha>   # fails if ref moved: compare-and-swap
git update-ref -d refs/heads/tmp <expected-old-sha>
git update-ref -m "bot: fast-forward release" refs/heads/release <sha>   # reflog message
```
Atomic multi-ref transactions:
```bash
git update-ref --stdin <<'EOF'
start
update refs/heads/release 1a2b3c... 9f8e7d...
create refs/tags/v2.0.0 1a2b3c...
delete refs/heads/rc 4d5e6f...
prepare
commit
EOF
```
Never write files under `.git/refs/` directly: refs may be packed (`.git/packed-refs`) or
stored in the reftable backend (Git 2.45+), and direct writes skip locking and reflogs.

## HEAD and symbolic refs
```bash
git symbolic-ref HEAD refs/heads/main          # point HEAD at a branch (bare repos: change default branch)
git symbolic-ref refs/remotes/origin/HEAD      # remote default branch
git remote set-head origin --auto              # refresh it
```

## Script hygiene
- Prefix with `git -c core.quotepath=off --no-pager` if parsing text (`core.quotepath` controls quoting of unusual path bytes).
- Prefer NUL-separated output (`-z`, or `%00` in a for-each-ref format) for names that may contain unusual characters.
- Check exit codes (`set -euo pipefail`); `--quiet --verify` turns "not found" into status 1.
- Push atomically on the remote too: `git push --atomic origin main v2.0.0`.

## Verify
- [ ] Script contains no `git branch | grep` / `git status` text parsing.
- [ ] Ref updates pass an expected old value where races are possible.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the Git 2.45 release notes. Confirmed: `git for-each-ref` options `--count`, `--sort`, `--merged`, `--shell`/`--python`, and format atoms `refname:lstrip=<n>`, `upstream:track`, `contents`, `*objectname`; `git update-ref` old-value check, `-d`, `-m` and the `--stdin` transaction verbs (`start`, `update`, `create`, `delete`, `prepare`, `commit`); `git symbolic-ref [-q] [--short]`; `git show-ref --verify --quiet`; `git rev-parse --verify --abbrev-ref`; `git remote set-head <name> --auto`; `git push --atomic`; reftable backend integrated in Git 2.45. Removed as unconfirmed: the `LC_ALL=C` advice.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `rev-parse --verify --quiet` (sha or exit 1) and `--abbrev-ref HEAD`; `symbolic-ref --short -q HEAD`; the `for-each-ref` formats shown, `--sort`, `--count`, `--merged`, `lstrip=2`, `contents:subject`, `objecttype`, `*objectname`, `--shell` and `--python` quoting, `%00`; `show-ref --verify --quiet`; `update-ref` with a correct old value (succeeds) and a wrong one (`cannot lock ref ... is at X but expected Y`, exit 128); `-m` message in the reflog; `-d` with old value; a `--stdin` transaction with `start`, `create`, `update`, `delete`, `prepare`, `commit`; `symbolic-ref HEAD refs/heads/...`; `remote set-head origin --auto`; `push --atomic`. Not run: the reftable backend (docs only).

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
