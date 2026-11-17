---
id: computing-software.software-engineering.git.preparing-a-release-describe-shortlog-archive
name: preparing-a-release-describe-shortlog-archive
category: computing-software
field: software-engineering
product: git
tags: [git, distributed-workflows, git-describe, git-archive, git-shortlog, release, versioning, changelog]
level: practitioner
status: verified
description: "Cut a release from Git: derive version strings with describe, build changelogs with shortlog/log, and produce reproducible source tarballs with archive."
sources:
  - https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project
  - https://git-scm.com/docs/git-describe
  - https://git-scm.com/docs/git-archive
  - https://git-scm.com/docs/git-shortlog
  - https://git-scm.com/docs/gitattributes
  - https://git-scm.com/docs/gitmailmap
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Preparing a release with describe, shortlog and archive

**Goal:** a tagged release with a meaningful version string, release notes and a source tarball that matches the tag exactly.

## 1. Version strings with describe
```bash
git describe --tags --always --dirty       # v2.3.0-14-g1a2b3c4-dirty
git describe --abbrev=0 --tags             # nearest tag only: v2.3.0
git describe --match 'v[0-9]*' --exclude '*-rc*'
```
Format: `<tag>-<commits since tag>-g<abbrev sha>`; `-dirty` if the working tree has changes. Use the output as the build's version string.
- Without `--tags`, only **annotated** tags are used; `--tags` lets lightweight tags count too (`--always` falls back to an abbreviated commit id when nothing matches).
- A shallow CI clone may lack the tags and history describe needs: `git fetch --tags --unshallow` fetches them.

## 2. Release notes
```bash
prev=$(git describe --abbrev=0 --tags HEAD^)
git shortlog --no-merges -sn $prev..HEAD          # contributor counts
git shortlog --no-merges $prev..HEAD              # commits grouped by author
git log --no-merges --format='- %s (%h)' $prev..HEAD
```
Map duplicate identities with a `.mailmap` file (`Proper Name <proper@x> <old@y>`); `git shortlog` applies it, as does `git log` with the mailmap placeholders such as `%aN` (see gitmailmap).

## 3. Tag and archive
```bash
git tag -a v2.4.0 -m "Release 2.4.0"
git archive --format=tar.gz --prefix=project-2.4.0/ -o project-2.4.0.tar.gz v2.4.0
```
Control archive contents with `.gitattributes`:
```
/tests       export-ignore
.github      export-ignore
version.txt  export-subst      # $Format:%H$ / $Format:%(describe)$ expanded at archive time
```

## Gotchas
- `git archive` only includes committed files; generated files must be built into a separate release artifact.
- Check whether submodule contents are included before relying on an archive of a repository that uses submodules; the git-archive manual is the authority.
- The `tar.gz` format uses Git's internal gzip implementation by default (`tar.<format>.command` can override it), so compression output can differ between tools and versions; publish your own checksums of the tarball you release.
- Sign the tag (`git tag -s`) so consumers can verify the source.

## Verify
- `tar tzf project-2.4.0.tar.gz | head` shows the prefix and no `tests/`.
- `git describe --exact-match v2.4.0^{commit}` succeeds on the release commit.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed: `git describe` options `--tags`, `--always`, `--dirty`, `--abbrev`, `--match`, `--exclude`, `--exact-match`; annotated-only default; `git shortlog` `-s` / `-n` and mailmap use; `git archive` `--format=tar.gz`, `--prefix`, `-o`, internal gzip default; `export-ignore` and `export-subst` with `%(describe)`; `git fetch --unshallow`. Removed as unconfirmed: the Go `-ldflags` example, the `actions/checkout` remark, the `sha256sum` line and the claim that submodule contents are never archived (the manual page does not state it).

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `describe --tags --always --dirty` (appends `-dirty` after a working tree edit), `--abbrev=0 --tags`, `--match` with `--exclude`, `--exact-match <tag>^{commit}`; `shortlog --no-merges -sn` and plain form; `log --no-merges --format`; `.mailmap` applied by `shortlog -sne` and `%aN`; `git archive --format=tar.gz --prefix=... -o` with `.gitattributes` `export-ignore` (tests and .github absent) and `export-subst` (`$Format:%H$` expanded); `git config tar.tar.xz.command` produced an xz stream; `git archive --list`; `git fetch --tags --unshallow` on a depth 1 clone.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
