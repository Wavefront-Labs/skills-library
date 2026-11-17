---
id: computing-software.systems-network-administration.healthchecks.reliability-tips
name: reliability-tips
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, request-timeout, retries, exception-handling, reliable-pinging]
level: practitioner
status: docs-checked
description: "Make Healthchecks pings reliable: set an HTTP request timeout, retry failed requests with increasing delays and decide how to handle client exceptions."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/reliability_tips.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/bash.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Specify an HTTP request timeout. A hung ping should not stall your work. This matters most for start signals (a hung ping must not prevent the job from running) and long-running workers (a stuck request after each item could block the whole process).

```
curl -m 10 <ping-url>
```

`-m` is short for `--max-time`.

2. Use retries to cut false alerts. Retry failed requests several times with increasing delays.

```
curl --retry 5 <ping-url>
```

curl's delays grow 1s, 2s, 4s, 8s and so on.

3. Handle exceptions. Know how your HTTP client reports failures. If the library raises exceptions on failed requests, decide whether to catch them in your code or let them propagate.

The silent one-liner from the shell scripts page combines the timeout and retry options:

```
curl -fsS -m 10 --retry 5 -o /dev/null <ping-url>
```

## Checked

2026-11-04: confirmed against the Pinging Reliability Tips page (timeout, retries with 1s, 2s, 4s, 8s delays, exception handling) and the Shell Scripts page (curl one-liner). Removed advice to catch and log exceptions and a closing remark that the pages do not make in this context.
Method: documentation only; no commands were run.
