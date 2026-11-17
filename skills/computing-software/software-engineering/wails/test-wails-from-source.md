---
id: computing-software.software-engineering.wails.test-wails-from-source
name: test-wails-from-source
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, local-development, git, go-install, go-mod-replace, testing]
level: practitioner
status: docs-checked
description: "Install the latest Wails CLI from a git clone, or test a branch or pull request, and point a project at it with a go.mod replace line."
sources: [https://wails.io/docs/guides/local-development]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use unreleased Wails code (master, a branch or a PR).

## Latest master
```sh
git clone https://github.com/wailsapp/wails
cd wails/v2/cmd/wails
go install
```
The directory you cloned into is the "clonedir". The CLI is now at the latest version.

## Point your project at it
Add to the bottom of the project's `go.mod`:

```
replace github.com/wailsapp/wails/v2 => <clonedir>
```

The page's examples point at the `v2` folder of the clone (for example `/path/to/wails/v2`).

## Revert to stable
```sh
go install github.com/wailsapp/wails/v2/cmd/wails@latest
```

## A branch
```sh
git clone https://github.com/wailsapp/wails
cd wails
git checkout -b branch-to-test --track origin/branch-to-test
cd v2/cmd/wails
go install
```

## A PR
Replace `[IDofThePR]` with the PR number:

```sh
git clone https://github.com/wailsapp/wails
cd wails
git fetch -u origin pull/[IDofThePR]/head:test/pr-[IDofThePR]
git checkout test/pr-[IDofThePR]
git reset --hard HEAD
cd v2/cmd/wails
go install
```

Always update your project's `go.mod` replace line as above for branch and PR tests.

## Gaps
The page defines "clonedir" as the directory you cloned into and writes the replace line with `<clonedir>`, yet both of its examples (Windows and Unix) end in `/v2`. Follow the examples (the clone's `v2` folder).

## Checked

2026-11-07. Read the whole Local Development guide (website/docs/guides/local-development.mdx): latest-master steps (clone, cd wails/v2/cmd/wails, go install), the clonedir note, the go.mod replace line and its two examples, reverting with go install ...@latest, testing a branch (checkout -b --track) and testing a PR (fetch pull/[IDofThePR]/head, checkout, reset --hard, cd v2/cmd/wails, go install). Rewrote the Gaps note to state only what the page shows (clonedir wording versus /v2 examples) instead of a rule. No other claims were trimmed. Commands were compared by reading only; none were run.

Method: documentation only; no commands were run.
