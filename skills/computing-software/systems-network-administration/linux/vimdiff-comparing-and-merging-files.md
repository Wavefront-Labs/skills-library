---
id: computing-software.systems-network-administration.linux.vimdiff-comparing-and-merging-files
name: vimdiff-comparing-and-merging-files
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vim, vimdiff, diff-mode, rpmnew, dpkg-dist, git-mergetool, config-merge, sysadmin]
level: practitioner
status: docs-checked
description: "Compare and merge config files with vimdiff: navigate hunks, pull/push changes, merge .rpmnew/.dpkg-dist after upgrades, diff remote files and use it as git mergetool."
sources:
  - https://vimhelp.org/diff.txt.html
  - https://git-scm.com/docs/git-mergetool
  - https://docs.fedoraproject.org/en-US/quick-docs/dnf/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vimdiff: compare and merge

**Goal:** reconcile your edited config with the package's new default (or two hosts' versions)
line by line, without losing either side's changes.

## 1. Open
```bash
vimdiff /etc/ssh/sshd_config /etc/ssh/sshd_config.rpmnew
vim -d a b c                       # up to 8 files
vimdiff /etc/hosts scp://web02//etc/hosts          # netrw remote file; // after the host means an absolute path
```
Find merge candidates after upgrades:
```bash
find /etc -name '*.rpmnew' -o -name '*.rpmsave'                       # RHEL/Fedora
find /etc -name '*.dpkg-dist' -o -name '*.dpkg-old'                  # Debian/Ubuntu (dpkg)
```

## 2. Navigate and merge
```vim
]c  [c          " next / previous change
do              " diff obtain: pull the other window's version of this hunk here
dp              " diff put: push this hunk to the other window
:diffget 3      " with 3+ buffers, say which buffer to get from (:ls for numbers)
:'<,'>diffget   " only the selected lines
:diffupdate     " re-scan after manual edits
zo zc zR zM     " open/close folds of unchanged text (all with zR)
:set diffopt+=iwhite,algorithm:histogram,indent-heuristic   " ignore whitespace changes; histogram algorithm; indent heuristic
:wqa            " write all and quit
```
Typical workflow for `.rpmnew`: left = your live file, right = new default; walk `]c`, `do`
the new defaults you want, leave your customisations, `:wqa`, then delete the `.rpmnew` so
the next check is clean.

## 3. As git mergetool
```bash
git config --global merge.tool vimdiff
git config --global mergetool.vimdiff.layout "LOCAL,BASE,REMOTE / MERGED"   # this is also the default layout
git mergetool
```
In the MERGED window: `:diffget LOCAL`, `:diffget REMOTE` (or buffer numbers), `]c` to the
next conflict, `:wqa`. `:cq` quits Vim without writing and returns an error exit status (so git treats the merge as unresolved).

## Gotchas
- Windows out of sync after edits: `:diffupdate`.
- `diffopt` algorithms are myers (default), minimal, patience and histogram; try `algorithm:patience` or `histogram` when hunks look odd.
- `do` and `dp` act on the hunk under the cursor (`dp` does not work in a Visual-mode selection).
- There can be up to eight buffers in diff mode.

## Verify
- [ ] After merging, `diff -u live new` shows only the customisations you meant to keep.
- [ ] Service config test passes (`sshd -t`, `nginx -t`, `named-checkconf`) before reload.
- [ ] No leftover `.rpmnew`/`.dpkg-dist` files for merged configs.

## Checked

2026-10-26. Documentation checked: Vim runtime/doc help files on vim/vim master (last commit 2026-10-25, Vim 9.2 series). Also: git Documentation (config/merge.adoc, mergetools/vimdiff.adoc, tag v2.56.0), rpm source (.rpmnew, .rpmsave suffixes in lib/fsm.cc and rpm-spec(5)), dpkg man page source (.dpkg-dist, .dpkg-old). Confirmed: up to eight diff buffers, ]c [c do dp :diffget [bufspec] :diffupdate, fold commands zo zc zR zM, diffopt iwhite, algorithm values and indent-heuristic, netrw scp:// double-slash absolute path, :cq, mergetool.vimdiff.layout and its default layout, merge.tool. Removed the unconfirmed git 2.37 version gate, the .ucf-dist suffix, the process-substitution alternative and the sudo diff-mode caveat.

Method: documentation only; no commands were run.
