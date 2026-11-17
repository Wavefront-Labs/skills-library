---
id: computing-software.data-engineering.apache-nifi.system-requirements
name: system-requirements
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, requirements, java, browsers, sizing]
level: intro
status: docs-checked
description: "Supported Java versions, operating systems and browsers for NiFi, plus what the admin guide says about sizing disks and CodeCache."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NiFi system requirements

Per the admin guide version read:
- Java: Java 8 or Java 11 are the officially supported JVMs.
- OS: Linux, Unix, Windows, macOS.
- Browsers: Edge, Firefox, Chrome, Safari, current and previous version.
- Hardware: no numeric minimums; sizing depends on the dataflow. Provide enough disk for the content, FlowFile and provenance repositories.
- Under sustained very high throughput the JVM CodeCache settings may need tuning (the guide points to its Bootstrap Properties section).

Verify: `java -version` reports a supported release before starting NiFi.

## Checked

Checked against the NiFi Administration Guide, System Requirements section: Java 8 or Java 11 (the guide says these are the only officially supported releases), the four operating systems, the four browsers at current and current minus one, the sizing statement and the CodeCache note match. Removed the throughput figures, which come from a page that is not cited.

Method: docs-only read of cited pages, 2026-11-08
