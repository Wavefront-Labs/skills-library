---
id: computing-software.software-engineering.git.writing-objects-with-hash-object-and-commit-tree
name: writing-objects-with-hash-object-and-commit-tree
category: computing-software
field: software-engineering
product: git
tags: [git, git-hash-object, commit-tree, write-tree, update-index, mktree, git-internals]
level: advanced
status: verified
description: "Build commits without a working tree using hash-object, update-index, write-tree/mktree and commit-tree: for bots that publish generated files to a branch."
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
  - https://git-scm.com/docs/git-hash-object
  - https://git-scm.com/docs/git-commit-tree
  - https://git-scm.com/docs/git-mktree
  - https://git-scm.com/docs/git-update-index
  - https://git-scm.com/docs/git-fast-import
  - https://git-scm.com/docs/git-config
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Writing objects with hash-object and commit-tree

**Goal:** create blobs, trees and commits directly, e.g. a CI job that publishes docs
to a `gh-pages` branch without checking it out, or to understand what `git commit` does.

## The pipeline `git commit` runs
1. `hash-object -w` content -> blob
2. `update-index` records blob + path + mode in the index
3. `write-tree` index -> tree object(s)
4. `commit-tree` tree + parent(s) + message -> commit
5. `update-ref` moves the branch

## By hand (Pro Git walkthrough)
```bash
echo 'hello' | git hash-object -w --stdin           # prints blob sha; -w writes it
git hash-object -w docs/index.html
git cat-file -p <sha>                                # read back
```
Object id = SHA-1 (or SHA-256 repos) of `"blob <size>\0<content>"`, so the same content
always has the same id.

## Publish to another branch without touching the working tree
Use a temporary index so the user's staging area is untouched:
```bash
export GIT_INDEX_FILE=$(mktemp)            # throwaway index
rm -f "$GIT_INDEX_FILE"
parent=$(git rev-parse -q --verify refs/heads/gh-pages || true)
git --work-tree=site add -A                # stage site/ contents as the branch root
tree=$(git write-tree)
commit=$(git commit-tree "$tree" ${parent:+-p "$parent"} -m "Publish docs $(git rev-parse --short HEAD)")
git update-ref refs/heads/gh-pages "$commit" ${parent:-}
unset GIT_INDEX_FILE
git push origin gh-pages
```
`--work-tree=site add -A` against an empty temp index makes the new tree exactly the
contents of `site/` (paths relative to it); files deleted from `site/` disappear from the branch.

## Building trees from scratch
```bash
printf '100644 blob %s\tREADME.md\n040000 tree %s\tdocs\n' "$blob" "$subtree" | git mktree
git update-index --add --cacheinfo 100644,"$blob",path/in/repo.txt   # stage without a file on disk
```
Modes: `100644` file, `100755` executable, `120000` symlink, `040000` tree, `160000` gitlink.

## Gotchas
- `commit-tree` uses `GIT_AUTHOR_NAME/EMAIL/DATE` and committer equivalents from env or
  config; set them in CI for reproducible commits.
- Objects written but never referenced are pruned by `git gc` once older than `gc.pruneExpire` (default `2.weeks.ago`).
- Skip-empty: compare `$tree` with `git rev-parse "$parent^{tree}"` and exit if equal.

## Verify
- [ ] `git ls-tree -r --name-only gh-pages` lists exactly the published files.
- [ ] The user's `git status` is unchanged after the script ran.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the Pro Git objects chapter. Confirmed: `git hash-object -w --stdin`, `git commit-tree <tree> -p <parent> -m`, `git mktree` (reads `ls-tree` style input), `git update-index --add --cacheinfo <mode>,<object>,<path>`, tree entry modes `100644`, `100755`, `120000`, `040000` and gitlink `160000` (git-fast-import), author/committer values taken from `GIT_AUTHOR_*` / `GIT_COMMITTER_*` (git), `gc.pruneExpire` default of 2 weeks, SHA-1 default with optional SHA-256 object format, `GIT_INDEX_FILE` and `--work-tree`; Pro Git shows the object header being hashed with the content. No claims needed removal in this skill.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `echo hello | git hash-object -w --stdin` equals the SHA-1 of `blob 6\0hello\n` computed with sha1sum; `cat-file -p` reads it back; the temporary-index publish recipe (`GIT_INDEX_FILE`, `--work-tree=site add -A`, `write-tree`, `commit-tree`, `update-ref`, `push`) creates a `gh-pages` branch whose `ls-tree -r --name-only` lists exactly `index.html`; the working tree and index of the user were untouched; `git mktree` with a blob and a nested tree; `update-index --add --cacheinfo 100644,<sha>,<path>`; `gc.pruneExpire` is unset by default (default value is docs only).

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
