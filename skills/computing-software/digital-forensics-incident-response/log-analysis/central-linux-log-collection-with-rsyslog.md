---
id: computing-software.digital-forensics-incident-response.log-analysis.central-linux-log-collection-with-rsyslog
name: central-linux-log-collection-with-rsyslog
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [rsyslog, linux-logging, log-forwarding, forensic-readiness, dfir]
level: practitioner
status: docs-checked
description: "Configure rsyslog to forward Linux logs off-host for investigations: omfwd with TLS, disk-assisted queues, and what a queue does and does not protect."
sources: ["https://www.rsyslog.com/doc/configuration/modules/omfwd.html", "https://www.rsyslog.com/doc/concepts/queues.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Central Linux log collection with rsyslog

Attackers clear local logs; forwarding them in near-real time to a collector they do not
control keeps the evidence. rsyslog's `omfwd` module forwards messages over UDP, TCP or TLS; it
is built in and needs no explicit loading. The `imjournal` input module reads the systemd
journal when journald is the primary log source.

## Forwarding action (RainerScript)
```text
action(
    type="omfwd"
    target="logs.example.internal"
    port="6514"                       # standard port for TLS syslog
    protocol="tcp"
    StreamDriver="ossl"               # or "gtls" / "mbedtls"
    StreamDriverMode="1"              # TLS-only
    StreamDriverAuthMode="x509/name"
    StreamDriverPermittedPeers="logs.example.internal"
    queue.type="LinkedList"
    queue.filename="fwdq"             # naming a queue file makes it disk-assisted
    queue.maxDiskSpace="1g"
    queue.saveOnShutdown="on"
)
```
Per the omfwd page:
- Prefer TCP with TLS over plain TCP or UDP; if reliable delivery is critical, consider
  `omrelp`. UDP can suit low-latency, non-blocking networks.
- Always define a queue for TCP forwarding so rsyslog does not block if the remote server is
  unavailable; tune `queue.size` for high volume or long outages.
- The legacy `@@server` and `@server` forms bypass queues and lack back-pressure control, so use
  the `action()` form.
- Hostnames in `target` are resolved on each connection attempt.

## Queues (from the queues page)
- Action queues default to direct (non-queueing) mode; you must set `queue.type`.
- In-memory queue types are LinkedList and FixedArray; the docs advise LinkedList if in doubt.
- Setting `queue.filename` makes an in-memory queue disk-assisted: data spills to disk when
  the queue fills (high watermark) or must be persisted on shutdown, and the queue is limited
  only by free disk space unless `queue.maxDiskSpace` is set (the limit is approximate). The
  docs recommend a disk-assisted LinkedList queue in front of each "send via tcp" action.
- `queue.saveOnShutdown="on"` persists the in-memory portion only at an orderly shutdown; it
  cannot run after a kill, crash or power loss. Where every accepted message must survive
  those events the docs say to use a pure disk queue (`queue.type="Disk"`, always the slowest
  mode) and tune `queue.checkpointInterval` and `queue.syncqueuefiles`.
- Set `global(workDirectory=...)` for where queue files are written.

## Verify
Send a test message from the client, confirm it reaches the collector, then stop the collector
and restart it to confirm queued messages are delivered. Write the collector side (inputs,
storage, retention) from the documentation for your rsyslog version; it is not covered here.

## Checked
2026-11-09. Confirmed on the omfwd and queues pages (omfwd read to line 150 of its page, queues read to line 125): TLS drivers and parameters, port 6514 comment, best practices, legacy forms, direct default for action queues, LinkedList advice, disk-assisted behaviour, maxDiskSpace, saveOnShutdown caveat, Disk queue durability. Confirmed on the configuration index that imjournal exists. Removed: the template, collector config (imtcp/omfile), `action.resumeRetryCount`, file paths, the "what to forward" list, `logger` verify command, UDP-spoofable claim.
Method: documentation only; no commands were run.
