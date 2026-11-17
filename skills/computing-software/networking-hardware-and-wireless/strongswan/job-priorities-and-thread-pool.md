---
id: computing-software.networking-hardware-and-wireless.strongswan.job-priorities-and-thread-pool
name: job-priorities-and-thread-pool
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, job-priority, thread-pool, processor, priority-threads]
level: advanced
status: docs-checked
description: "Prevent charon thread starvation under load by reserving worker threads per job priority with charon.processor.priority_threads, and understand the CRITICAL to LOW classes."
sources:
  - https://docs.strongswan.org/docs/latest/config/jobPriority.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# job priorities and thread pool
charon performs synchronous blocking operations on IKE_SAs, such as talking to a RADIUS server with EAP-RADIUS or fetching CRL/OCSP data during chain verification. Under load the thread pool can run dry and important jobs like liveness checks may run late. Job priorities reserve threads for higher classes.

| Priority | Used for |
|---|---|
| CRITICAL | long-running dispatcher jobs |
| HIGH | INFORMATIONAL exchanges, e.g. liveness checking (DPD) |
| MEDIUM | everything else, including IKE_SA_INIT processing |
| LOW | IKE_AUTH processing (RADIUS and CRL fetching block here) |

IKE_SA_INIT stays MEDIUM on purpose so the DH exchange can run while other threads are blocked in IKE_AUTH. To stop the daemon accepting more IKE_SA_INIT messages than it can handle, use IKE_SA_INIT dropping (described on the page).

The pool serves jobs strictly by priority. A class with n reserved threads always has n available to it. Reserve them under `charon.processor`:

```
charon {
  processor {
    priority_threads {
      high = 1
      medium = 4
    }
  }
}
```

Keys `priority_threads.critical|high|medium|low` default to 0. Keep `charon.threads` (default 16) high enough: several threads are reserved for long-running internal tasks, and idle workers shown by `swanctl --stats` hint at how many are reserved.

## Checked
2026-11-04. Confirmed against the strongSwan Job Priority Management page (priority classes, priority_threads keys and defaults, IKE_SA_INIT staying MEDIUM, strict priority order) and the strongswan.conf reference (charon.threads default 16 and its note on reserved threads). Nothing removed.

Method: documentation only; no commands were run.
