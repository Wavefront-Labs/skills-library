---
id: computing-software.data-engineering.apache-nifi.start-stop-nifi
name: start-stop-nifi
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, nifi-sh, startup, service, getting-started]
level: intro
status: docs-checked
description: "Start, stop and check NiFi with bin/nifi.sh or run-nifi.bat, wait for init, install as a Linux service, and find the UI URL."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/getting-started.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Starting and stopping NiFi

Linux/macOS, from the install directory:
- `bin/nifi.sh run` foreground (Ctrl-C stops it).
- `bin/nifi.sh start` background; `status` and `stop` do the obvious.
- `bin/nifi.sh start --wait-for-init 120` blocks until components are scheduled; the default wait is 15 minutes.
- `bin/nifi.sh install [name]` registers a service (default name `nifi`), then `sudo service nifi start|stop|status`.

Windows: double-click `run-nifi.bat` in `bin`; stop with Ctrl+C in its window. Homebrew installs expose `nifi start` and `nifi stop` from any directory.

UI: `https://localhost:8443/nifi`; the port comes from `nifi.properties` in `conf`.

The certificate NiFi generates on first start is self-signed and expires after 60 days; the guide says production deployments should provision a certificate from a trusted authority and update the keystore and truststore configuration.

Verify: `bin/nifi.sh status` reports running and the UI URL loads over HTTPS.

## Checked

Confirmed in the NiFi Getting Started guide: nifi.sh run, start, status and stop; the --wait-for-init flag with a seconds timeout and 15 minute default; bin/nifi.sh install with default service name nifi and an optional custom name; sudo service nifi start, stop and status; run-nifi.bat on Windows; Homebrew nifi start and nifi stop; the https://localhost:8443/nifi UI address and port change via nifi.properties; the 60 day self-signed certificate.

Method: docs-only read of cited pages, 2026-11-08
