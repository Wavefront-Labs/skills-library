---
id: computing-software.data-engineering.apache-nifi.bootstrap-conf-properties
name: bootstrap-conf-properties
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, bootstrap-conf, jvm, java-arg, nifi-sh]
level: practitioner
status: docs-checked
description: "bootstrap.conf keys and defaults: java, run.as, preserve.environment, lib.dir, conf.dir, java.arg.N numbering, listen port and notification retry attempts."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bootstrap.conf

- `java`: `java`
- `run.as`: no default; ignored on Windows
- `preserve.environment`: false
- `lib.dir`: `./lib`; `conf.dir`: `./conf`
- `graceful.shutdown.seconds`: no default stated; seconds the bootstrap waits for a clean shutdown before killing the process
- `nifi.bootstrap.listen.port`: random ephemeral port if missing, empty or 0
- `notification.max.attempts`: 5
- `java.arg.N`: JVM arguments (heap, GC, temp dir ship by default). Numbering is arbitrary so long as each is unique; the guide's examples use 15 and 16 for Kerberos flags.

Notification services are defined in an XML file named by `notification.services.file`; the default location is `conf/bootstrap-notification-services.xml`. Changes to bootstrap.conf take effect only after NiFi is stopped and restarted.

Verify: `bin/nifi.sh status` after restart and the JVM shows the argument you changed.

## Checked

Confirmed in the NiFi Administration Guide, Bootstrap Properties table: java, run.as, preserve.environment, lib.dir, conf.dir, graceful.shutdown.seconds, java.arg.N naming, notification.max.attempts 5, nifi.bootstrap.listen.port behaviour, the notification services file default, the restart requirement, and the java.arg.15 and 16 Kerberos examples elsewhere in the guide.

Method: docs-only read of cited pages, 2026-11-08
