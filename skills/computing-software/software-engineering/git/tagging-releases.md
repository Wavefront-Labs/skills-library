---
id: computing-software.software-engineering.git.tagging-releases
name: tagging-releases
category: computing-software
field: software-engineering
product: git
tags: [git, git-tag, annotated-tags, lightweight-tags, signed-tags, push-tags, release-tags, semver]
level: practitioner
status: verified
description: "Create, push, sign, move and delete Git tags correctly; why release tags must be annotated and never silently re-pointed."
sources:
  - https://git-scm.com/book/en/v2/Git-Basics-Tagging
  - https://git-scm.com/docs/git-tag
  - https://git-scm.com/docs/git-push
  - https://git-scm.com/docs/git-describe
  - https://docs.gitlab.com/ee/user/project/protected_tags.html
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tagging releases

**Goal:** an immutable, discoverable marker for every release that CI and humans agree on.

## Annotated vs lightweight
- **Annotated** (`git tag -a v1.4.0 -m "Release 1.4.0"`) is a full object: tagger,
  date, message, optional signature. `git describe` uses only annotated tags by default.
  Use for every release.
- **Lightweight** (`git tag tmp-mark`) is just a ref. Fine for private bookmarks.

## Common operations
```bash
git tag -a v1.4.0 <sha> -m "Release 1.4.0"   # tag an older commit
git tag -s v1.4.0 -m "..."                   # signed (GPG or SSH, see commit-signing skill)
git tag -l 'v1.4.*' --sort=-v:refname        # list, semver-aware sort
git show v1.4.0                              # tag object + commit
git push origin v1.4.0                       # push one tag
git push --follow-tags                       # push annotated tags reachable from pushed commits
git config --global push.followTags true     # make that the default
```
Plain `git push` does NOT push tags. `git push --tags` pushes every local tag,
including junk ones; prefer one tag or `--follow-tags`.

## Deleting and moving
```bash
git tag -d v1.4.0 && git push origin --delete v1.4.0
```
Never move a published release tag. Clients that already fetched it keep the old
target (`git fetch` will not overwrite an existing tag without `--force`), so two people
"on v1.4.0" have different code. Cut v1.4.1 instead. If you must (tag pushed seconds
ago to the wrong commit), delete remotely, retag, and announce it.

## Conventions
- Pick one naming convention and keep it (for example `v1.4.0` following SemVer); version-aware sorting (`--sort=-v:refname`) and `git describe --match` patterns depend on it.
- Protect release tags on the server (GitHub rulesets can target tags; GitLab has protected tags) so
  only CI or maintainers can create them.
- Tag the exact commit CI built, ideally from the pipeline itself.

## Verify
- [ ] `git cat-file -t v1.4.0` prints `tag` (annotated), not `commit`.
- [ ] `git ls-remote --tags origin v1.4.0` shows it on the remote.
- [ ] `git describe --tags` on the release commit prints exactly the tag.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22), the Pro Git tagging chapter, the GitLab docs mirror and the github/docs repository. Confirmed: annotated versus lightweight tags and that `git describe` uses annotated tags by default; `git tag -a`, `-s`, `-d`, `-l` with `--sort=v:refname`; `git push` does not transfer tags by default, `--follow-tags` pushes annotated tags reachable from pushed commits, `push.followTags`; the git-tag "On Re-tagging" guidance (use a new name; Git does not silently replace a tag others already have); GitLab protected tags and GitHub rulesets targeting tags. Removed as unconfirmed: the claim that goreleaser, Go modules and setuptools-scm parse `v` prefixes.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `tag -a <name> <sha> -m`; lightweight vs annotated (`cat-file -t` prints `tag` or `commit`); `git describe` skips a lightweight tag unless `--tags`; `tag -l 'v1.4.*' --sort=-v:refname`; `git show` of a tag; `push origin <tag>`, `push --follow-tags`, `tag -d` plus `push origin --delete`; `ls-remote --tags`. Not run: `git tag -s` (no signing key) and server-side tag protection (docs only).

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
