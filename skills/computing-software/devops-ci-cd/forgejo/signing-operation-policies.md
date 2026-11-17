---
id: computing-software.devops-ci-cd.forgejo.signing-operation-policies
name: signing-operation-policies
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [signing-policies, initial-commit, crud-actions, merges-signing]
level: advanced
status: docs-checked
description: "Decide when Forgejo signs by operation using values like pubkey, twofa, parentsigned and approved."
sources:
  - https://forgejo.org/docs/latest/admin/advanced/signing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For each operation Forgejo can create a commit, and you choose when to sign it. Values are given as a comma-separated list, except `always` and `never`, which are special and cannot be combined with other values.

Settings live in the `[repository.signing]` section. Settings and their values:

- `INITIAL_COMMIT` (first commit of a new repository): `pubkey` (user has a GPG or SSH key on the account), `twofa` (user uses two-factor authentication).
- `WIKI` (wiki commits): `pubkey`, `twofa`, `parentsigned` (parent commit is signed).
- `CRUD_ACTIONS` (web editor and API file changes): `pubkey`, `twofa`, `parentsigned`.
- `MERGES` (pull request merge commits): `pubkey`, `twofa`, `basesigned` (parent in the base repository is signed), `headsigned` (head commit of the head branch is signed), `commitssigned` (all commits up to the merge point are signed), and `approved` (the pull request targets a protected branch and has at least one approval).

The page does not say whether multiple values in one list are combined with AND or OR, so test a combined setting such as `MERGES = commitssigned, approved` on a scratch instance before relying on it.

## Checked

Date: 2026-11-07
Confirmed against the "Instance Commit Signing" page, read in full including its code blocks: the operations Forgejo can sign, the `[repository.signing]` section, the comma-separated list rule with `always` and `never` that cannot be combined, and the exact value lists and descriptions for `INITIAL_COMMIT`, `WIKI`, `CRUD_ACTIONS` and `MERGES`.
Removed: the worked example claiming `MERGES = commitssigned, approved` means both must hold, and the pointer to `DEFAULT_TRUST_MODEL` (neither is stated on this page); replaced with a note that combination semantics are not documented there.
Method: documentation only; no commands were run.
