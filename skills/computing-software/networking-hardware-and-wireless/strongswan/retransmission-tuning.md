---
id: computing-software.networking-hardware-and-wireless.strongswan.retransmission-tuning
name: retransmission-tuning
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, retransmission, timeouts, retransmit-tries, backoff]
level: practitioner
status: docs-checked
description: "Tune IKE retransmission in strongSwan with the charon retransmit_tries, timeout, base, jitter and limit options and the exponential backoff formula."
sources:
  - https://docs.strongswan.org/docs/latest/config/retransmission.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# retransmission tuning
Retransmission is configured globally in strongswan.conf under `charon`:

| Option | Default | Meaning |
|---|---|---|
| `retransmit_tries` | 5 | retransmissions before giving up |
| `retransmit_timeout` | 4.0 | timeout in seconds |
| `retransmit_base` | 1.8 | base of exponential backoff |
| `retransmit_jitter` | 0 | max random reduction in percent (0 disables) |
| `retransmit_limit` | 0 | upper limit in seconds for the timeout (0 disables) |

Formula: `relative timeout = retransmit_timeout * retransmit_base ^ (n-1)`, where n is the current retransmission count. The result cannot exceed `retransmit_limit`, which is useful with many retries. With jitter: `relative timeout - random(0, retransmit_jitter * relative timeout)`.

With the defaults, retransmissions occur after 4s, 7s, 13s, 23s and 42s (absolute 4, 11, 24, 47, 89 seconds), and charon gives up after a further 76s, at 165s.

## Checked
2026-11-04. Confirmed against the strongSwan Retransmission page: the five options with types and defaults, both formulas, and the default timeout table (4, 7, 13, 23, 42s; give up at 165s). Removed the IKEv2 liveness remark, which is not on that page.

Method: documentation only; no commands were run.
