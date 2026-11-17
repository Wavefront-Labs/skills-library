---
id: computing-software.software-engineering.git.git-objects-and-cat-file
name: git-objects-and-cat-file
category: computing-software
field: software-engineering
product: git
tags: [git, git-internals, git-objects, git-cat-file, blobs-trees-commits, plumbing, hash-object]
level: practitioner
status: verified
description: "Inspect and create Git's blob, tree, commit and tag objects with cat-file, hash-object, ls-tree and the other plumbing commands that porcelain is built on."
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
  - https://git-scm.com/docs/git-cat-file
  - https://git-scm.com/docs/git-hash-object
  - https://git-scm.com/book/en/v2/Git-Internals-Packfiles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Git objects and cat-file

**Goal:** understand and debug what Git actually stores, so corrupt repos, odd diffs and scripting tasks stop being mysterious.

## 1. The four object types
| Type | Content | Created by |
|---|---|---|
| blob | file bytes (no name, no mode) | `git add` |
| tree | entries `mode type sha name` | `git write-tree` / commit |
| commit | tree, parents, author, committer, message | `git commit-tree` / commit |
| tag | object, type, tag name, tagger, message, signature | `git tag -a` |
Object id = SHA-1 (or SHA-256 in `--object-format=sha256` repos) of `"<type> <size>\0<content>"`. Same content = same id, everywhere.

## 2. Reading objects
```bash
git cat-file -t HEAD              # commit
git cat-file -p HEAD              # pretty-print commit
git cat-file -p 'HEAD^{tree}'     # root tree
git ls-tree -r --long HEAD src/   # recursive, with sizes
git cat-file -p HEAD:src/main.go  # blob by path
git cat-file -s <sha>             # size
git rev-parse HEAD:README.md      # path -> blob id
```
Batch mode for scripts (fast, one process):
```bash
git rev-list --objects --all | git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(rest)' |
  sort -k3 -n | tail -20         # largest objects in history
```

## 3. Writing objects by hand (plumbing)
```bash
echo 'hello' | git hash-object -w --stdin     # store blob, print id
git update-index --add --cacheinfo 100644,<blob>,hello.txt
tree=$(git write-tree)
commit=$(echo "manual commit" | git commit-tree $tree -p HEAD)
git update-ref refs/heads/manual $commit
```

## 4. Loose vs packed
New objects are zlib-compressed loose files in `.git/objects/ab/cdef...`. `git gc` / `git maintenance` packs them into `.git/objects/pack/*.pack` with delta compression and `.idx` indexes.
```bash
git count-objects -vH
git verify-pack -v .git/objects/pack/pack-*.idx | sort -k3 -n | tail
```

## Gotchas
- Modes in trees: `100644` file, `100755` executable, `120000` symlink, `040000` tree, `160000` gitlink (submodule).
- Git never stores diffs as objects; deltas exist only inside packfiles, chosen heuristically.
- Hash collisions: modern Git uses SHA-1DC (collision detection). SHA-256 repositories use `--object-format=sha256` (64-hex ids).

## Checked
Run with Git 2.46.2 on 2026-10-18 in a scratch repo: `git hash-object` equals the SHA-1 of `blob <size>\0<content>` computed by hand; `hash-object -w --stdin`, `update-index --add --cacheinfo 100644,<blob>,name`, `write-tree`, `commit-tree -p HEAD` and `update-ref` build a commit by hand; `ls-tree -r --long`, `cat-file -t/-p/-s`, `rev-parse HEAD:path` and `rev-list --objects --all | cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(rest)'` print what the skill shows; `git gc` creates a `.pack` and `.idx` and `verify-pack -v` lists them; `git init --object-format=sha256` yields 64-hex ids. Git's 2.13.0 release notes describe the collision-detecting SHA-1 variant. Tree mode `160000` (gitlink) appears in the fast-import documentation; the symlink mode `120000` could not be produced on the Windows test machine and is stated from the Git format documentation, not re-run.

## Verify
- `git cat-file -p $(git rev-parse HEAD:file)` equals `git show HEAD:file`, and `git hash-object file` equals that blob id when the working copy is unchanged (and no filters apply).
