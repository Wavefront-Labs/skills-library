---
id: computing-software.systems-network-administration.restic.faq-multi-host-repos
name: faq-multi-host-repos
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, faq, multiple-hosts, shared-repository, group-by, deduplication]
level: practitioner
status: docs-checked
description: "Decide between one shared restic repository and separate repositories per host, weighing deduplication against key isolation and retention."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/faq.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One repository or many?

## Shared repository

Works for hosts with the same trust and access needs.

Pros:

- Deduplication across hosts, so common files are stored once.
- Only one repository to maintain.

Cons:

- Anyone holding the repository key can read every host's snapshots.
- Retention policies such as `forget` apply to the snapshots stored there.

Snapshots keep their host and path metadata, so you can filter and group them with options such as `--host` and `--group-by`.

## Separate repositories

Pros:

- Separate keys, retention policies and maintenance.
- Stronger isolation between hosts or users.

Cons:

- The same data stored in separate repositories cannot be deduplicated across them.

## Rule of thumb

Shared trust means one repository. Need isolation between hosts, users or policies means separate repositories.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/faq.rst.

Method: documentation only; no commands were run.
