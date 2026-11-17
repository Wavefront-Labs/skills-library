---
id: computing-software.software-engineering.git.email-patches-format-patch-and-am
name: email-patches-format-patch-and-am
category: computing-software
field: software-engineering
product: git
tags: [git, distributed-workflows, git-format-patch, git-am, send-email, patches, mailing-list, range-diff]
level: practitioner
status: verified
description: "Produce, send and apply patch series by email with format-patch, send-email and am, including cover letters, rerolls and resolving failed applies."
sources:
  - https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project
  - https://git-scm.com/docs/git-format-patch
  - https://git-scm.com/docs/git-am
  - https://git-scm.com/docs/git-send-email
  - https://www.kernel.org/doc/html/latest/process/submitting-patches.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Email patches with format-patch, send-email and am

**Goal:** contribute to or maintain a mailing-list project (Linux, Git, QEMU, PostgreSQL style) where patches travel as emails, not pull requests.

## 1. Produce a series
```bash
git format-patch -o outgoing/ --cover-letter -v2 origin/master..my-topic
# outgoing/v2-0000-cover-letter.patch, v2-0001-....patch, ...
```
- `-v2` marks a reroll (`[PATCH v2 1/3]`); `--cover-letter` adds patch 0 with a shortlog and diffstat; edit its subject and blurb.
- `--base=auto` (or `format.useAutoBase`) records the base commit so maintainers can apply to the right tree; it needs the topic branch to track an upstream, otherwise it fails with "failed to get upstream" (pass `--base=<commit>` instead).
- `--range-diff=v1-tag` appends a range-diff to the cover letter showing what changed since v1.
- Each commit message becomes the email body; a `---` line separates it from notes that are not committed (put "changes since v1" there).

## 2. Check and send
```bash
./scripts/checkpatch.pl outgoing/*.patch           # kernel; other projects have their own linters
git send-email --to=list@example.org --cc=maintainer@example.org outgoing/*.patch
```
Configure SMTP once:
```ini
[sendemail]
    smtpServer = smtp.example.com
    smtpServerPort = 587
    smtpEncryption = tls
    smtpUser = me@example.com
```
Send to yourself first (`--to=me@example.com`). Never paste patches into a webmail client; it rewraps lines and converts tabs.

## 3. Apply (maintainer side)
```bash
git am -3 --signoff < series.mbox      # -3 = three-way fallback using blob ids in the patch
b4 am <message-id>                      # kernel workflow: fetch a whole thread from lore and apply
```
When `git am` stops:
```bash
git am --show-current-patch=diff
# fix files, then
git add -u && git am --continue        # or --skip / --abort
```
`git apply --reject` leaves `.rej` hunks for manual merging when `-3` is impossible (blob missing).

## Gotchas
- `git am` preserves author and date from the email; `git apply` does not create commits at all.
- Binary files: `format-patch` emits a `GIT binary patch` block by default (checked), so `git am` can apply it.
- `Signed-off-by` (DCO) is added with `git commit -s` / `git am --signoff`; it is a legal statement, not decoration.
- Reply rerolls to the v1 thread with `--in-reply-to=<v1 cover message-id>` if the project asks for it; many prefer a new thread.

## Verify
- `git am` the generated mbox onto a fresh branch from the stated base: series applies cleanly and builds after every patch.
