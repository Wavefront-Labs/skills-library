---
id: computing-software.data-engineering.apache-nifi.content-claims-copy-on-write
name: content-claims-copy-on-write
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, content-repository, content-claim, copy-on-write, resource-claim]
level: advanced
status: docs-checked
description: "NiFi content storage model: immutable content, copy-on-write, containers and sections, resource claims versus content claims, and which processors copy or share content."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/nifi-in-depth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content claims and copy-on-write

- Content lives on disk and is read only when needed; it is immutable.
- Changing content streams new data to a new location and repoints the FlowFile (for example CompressContent writes C2 and the FlowFile moves from C1 to C2; earlier provenance events keep referencing C1).
- Layout: Containers (root directories) and Sections (subdirectories); multiple containers spread I/O over partitions.
- A Resource Claim identifies a file by id, section and container. A Content Claim is a Resource Claim plus offset and length, so many FlowFiles share one file.
- MergeContent always copies input into merged content and emits JOIN. SplitText makes pointer-based FlowFiles without copying; RouteText copies when non-contiguous lines route together.
- UpdateAttribute changes only attributes and emits ATTRIBUTES_MODIFIED.
- Deleting content leaves lineage visible but makes replay impossible.

Verify: a CONTENT_MODIFIED event shows different input and output content claims.

## Checked

Confirmed against NiFi In Depth (Repositories, Content Claim, Copy on Write, Extended Copy on Write, Extended Routing Use-cases, Provenance Repository, Updating Attributes).

Method: docs-only read of cited pages, 2026-11-08
