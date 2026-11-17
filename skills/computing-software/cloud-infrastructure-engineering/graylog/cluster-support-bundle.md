---
id: computing-software.cloud-infrastructure-engineering.graylog.cluster-support-bundle
name: cluster-support-bundle
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [support-bundle, diagnostics, system-stats, troubleshooting]
level: practitioner
status: docs-checked
description: "Generate a Graylog Cluster Support Bundle from System > Logging and review its contents before sending it to Support."
sources:
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/cluster_support_bundle.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cluster support bundle

This is a Graylog Enterprise feature. Create it at **System > Logging**: click Create Support Bundle, then download the .zip from the Cluster Support Bundle list. Attach it to support tickets.

The zip may include sensitive information such as IP addresses and passwords. Examine it before sending.

Contents include `system-stats.json` with:
- File system information: disk usage for the data, journal, plugin and bin directories, mount points and free space.
- JVM configuration: Java version and vendor, heap settings (for example `-Xms1g -Xmx1g`), garbage collector (G1GC), system properties.
- Operating system metrics: CPU information and more.

Other diagnostic files cover further layers of the system.

## Checked

2026-11-04. Confirmed against the Cluster Support Bundle page. Added the Enterprise-only note.

Method: documentation only; no commands were run.
