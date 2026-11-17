---
id: computing-software.systems-network-administration.healthchecks.ping-body-logging
name: ping-body-logging
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, ping-body, attach-logs, post-body, curl-data-binary]
level: practitioner
status: docs-checked
description: "Attach command output to Healthchecks pings with POST bodies, work around curl argument-length limits, handle truncated logs and download the original body."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/attaching_logs.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only POST pings can carry a body. The server stores the first part of the body, up to the ping body limit.

Capture stdout and stderr and post them:

```
#!/bin/sh
m=$(/usr/bin/certbot renew 2>&1)
curl -fsS -m 10 --retry 5 --data-raw "$m" <ping-url>
```

You can also append the exit code to the URL (`<ping-url>/$?`) to mark success or failure in the same request.

Very long output can trigger curl's "Argument list too long" error. Write the output to a temporary file and send it with `--data-binary @/path/to/output.txt`.

Truncated logs: make the job less verbose, send the last portion instead of the first, or use a dedicated log aggregation service.

Read stored logs in the check's Events section: click an event, then "Download Original" for the exact body.

The third-party tool runitor runs a command, captures output, reports results, measures run time and retries on transient errors.

Self-hosted: `PING_BODY_LIMIT` sets the byte limit; bodies larger than 100 bytes can go to S3-compatible storage.

## Checked

2026-11-04: confirmed against the Attaching Logs page (certbot examples, Argument list too long workaround, truncation options, Events and Download Original, runitor) and the project README (external object storage for bodies over 100 bytes). PING_BODY_LIMIT is a documented self-hosted setting.
Method: documentation only; no commands were run.
