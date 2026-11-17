---
id: computing-software.software-engineering.git.external-diff-and-merge-tools
name: external-diff-and-merge-tools
category: computing-software
field: software-engineering
product: git
tags: [git, git-difftool, git-mergetool, vscode-merge, beyond-compare, kdiff3, meld]
level: practitioner
status: verified
description: "Configure git difftool and mergetool (VS Code, Meld, Beyond Compare, KDiff3): tool commands, directory diffs, trustExitCode and keepBackup."
sources: ["https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration", "https://git-scm.com/docs/git-difftool", "https://git-scm.com/docs/git-mergetool", "https://code.visualstudio.com/docs/sourcecontrol/overview#_merge-conflicts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External diff and merge tools

**Goal:** review diffs and resolve conflicts in a graphical 3-way tool without Git
leaving `.orig` litter or misreading the tool's exit status.

## List built-in support
```bash
git difftool --tool-help      # shows tools Git knows and which are installed
git mergetool --tool-help
```
Built-ins (meld, kdiff3, bc, vimdiff, opendiff, p4merge, ...) need only the name:
```bash
git config --global diff.tool meld
git config --global merge.tool meld
```

## Custom tool: VS Code
```bash
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff "$LOCAL" "$REMOTE"'
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait --merge "$REMOTE" "$LOCAL" "$BASE" "$MERGED"'
```
Variables (custom `cmd` ran with all of these set): `$LOCAL` (ours), `$REMOTE` (theirs), `$BASE` (common ancestor), `$MERGED`
(file to write the result into). Quote them: paths can contain spaces.

## Useful settings
```bash
git config --global difftool.prompt false
git config --global mergetool.keepBackup false        # no *.orig files
git config --global mergetool.<tool>.trustExitCode true    # per tool (no global key); only if the tool returns non-zero on cancel
git config --global mergetool.vscode.trustExitCode false   # default: Git checks the file's timestamp, else asks "was the merge successful?"
```

## Usage
```bash
git difftool main...feature              # one window per file
git difftool -d main...feature           # directory diff: whole change set in one window (best)
git difftool --staged
git mergetool                            # iterate over conflicted files
git mergetool -- path/to/file
```
After mergetool closes, Git stages the file if it considers the merge resolved; check
`git diff --staged` before committing.

## Windows path quirks
Use forward slashes and quote the exe: `'"<BC_INSTALL_DIR>/bcomp.exe" "$LOCAL" "$REMOTE"'`.
Beyond Compare is built-in as `bc` (`difftool.bc.path` sets the exe).

## Verify
- [ ] `git difftool -d HEAD~1` opens one directory comparison.
- [ ] After `git mergetool`, no `*.orig` files and no conflict markers (`git diff --check`).
