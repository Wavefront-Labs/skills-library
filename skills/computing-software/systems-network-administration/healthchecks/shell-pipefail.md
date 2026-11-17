---
id: computing-software.systems-network-administration.healthchecks.shell-pipefail
name: shell-pipefail
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, pipefail, shell-pipeline, certbot-example, exit-code-accuracy]
level: practitioner
status: docs-checked
description: "Report accurate exit codes from shell pipelines to Healthchecks with set -o pipefail, so a failing first stage is not masked by a succeeding last stage."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/bash.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a pipeline's exit status is that of its rightmost command, so `$?` can report success even when an earlier stage failed. Use `pipefail` before pinging with the exit status.

```
#!/bin/sh

set -o pipefail
pg_dump somedb | gpg --encrypt --recipient alice@example.org --output somedb.sql.gpg
# Without pipefail, if pg_dump fails but gpg succeeds, $? is 0
# and the script reports success.
# With pipefail, a pg_dump failure is reported with its exit code.
curl -m 10 --retry 5 <ping-url>/$?
```

Notes:
- Appending an exit status (0-255) to the ping URL: Healthchecks treats 0 as success and non-zero values as failures.

Similar pattern with certbot: run `/usr/bin/certbot renew`, then `curl -m 10 --retry 5 <ping-url>/$?`.

To attach the output too, capture it with `m=$(... 2>&1)` and send via `--data-raw "$m"` (see ping-body-logging).

## Checked

2026-11-04. Confirmed against the Healthchecks Shell Scripts page: the rightmost-command default for pipeline exit status, the pipefail example with pg_dump and gpg, the certbot renew example, exit status 0-255 semantics and the m=$(... 2>&1) with --data-raw capture. Removed two notes (reading $? immediately, ping on its own line) that the page does not state.

Method: documentation only; no commands were run.
