---
id: computing-software.cloud-infrastructure-engineering.saltstack.targeting-batch
name: targeting-batch
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, targeting, batch, batch-size, batch-wait, rolling]
level: practitioner
status: docs-checked
description: "Run Salt commands on a rolling window of minions with -b/--batch-size (count or percent) and pause between minions using --batch-wait."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/targeting/batch.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch execution

`-b` or `--batch-size` limits how many targeted minions run a command at once. It is a rolling window: when one minion returns, the command goes to another, so the number of running minions stays steady.

- A whole number (`10`) is a fixed count.
- A percentage (`25%`) is a share of the targeted minions.
- `--batch-wait` (added in 2016.3) sets seconds to pause after a minion returns before the command goes to a new one.

Examples:

```
salt '*' -b 10 test.version
salt -G 'os:RedHat' --batch-size 25% apache.signal restart
```

The second restarts apache on 25% of the RedHat minions at a time until all are done.

## Checked

2026-11-04: read the Salt targeting batch page in full. Confirmed -b/--batch-size with counts and percentages, the rolling window behaviour, the two examples and --batch-wait (2016.3). Nothing removed.

Method: documentation only; no commands were run.
