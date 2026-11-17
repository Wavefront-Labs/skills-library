---
id: computing-software.cloud-infrastructure-engineering.garage.scrub-disable-and-schedule
name: scrub-disable-and-schedule
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [disable-scrub, data-scrub, garage-repair-scrub, scrub-tranquility]
level: practitioner
status: docs-checked
description: "Understand the automatic data scrub, run it manually, slow it with scrub tranquility, or disable it."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/durability-repairs/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A scrub reads every data block and verifies its hash. A block found corrupted (bitrot, accidental changes) is restored from another node holding a valid copy. Garage schedules scrubs automatically about every 25 to 35 days, with a random delay so nodes do not scrub together. `garage worker get` shows the next run.

Commands:
- `garage repair scrub start` launches one by hand.
- `garage worker list` finds the scrub worker's task ID, then `garage worker info <scrub_task_id>` shows runtime statistics. Run it on each node for cluster-wide numbers.
- `garage repair scrub pause` pauses it, but the scrub resumes automatically 24 hours later because Garage will not run without regular scrubs.
- `garage worker set scrub-tranquility` is the recommended way to ease a heavy scrub: a higher value means longer pauses between block verifications, and a longer scrub overall.

A scrub is very disk-intensive and may slow the cluster.

In the configuration file, `disable_scrub = true` turns off the scheduled scrub, for instance when you scrub at filesystem level. The configuration reference then says that if you find a corrupted data file you should delete it and run `garage repair blocks` on the node so it fetches a copy from another node.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Durability & Repairs. Confirmed on the durability page: 25-35 day schedule, `garage worker get`, `garage repair scrub start`, `garage worker list` and `info`, pause with 24 hour resume, `scrub-tranquility`. Confirmed on the configuration page: `disable_scrub` and the delete-then-`garage repair blocks` advice. No claims removed.

Method: documentation only; no commands were run.
