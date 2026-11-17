---
id: computing-software.data-engineering.apache-nifi.common-flowfile-attributes
name: common-flowfile-attributes
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, attributes, filename, uuid, entrydate, filesize]
level: intro
status: docs-checked
description: "Core FlowFile attributes: filename, path, uuid, entryDate, lineageStartDate, fileSize, which are system generated, and how Expression Language reads them."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/getting-started.html
  - https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common attributes

Every FlowFile has at least these attributes:

- `filename`: a filename that can be used to store the data on a local or remote file system.
- `path`: the name of a directory that can be used to store the data on a local or remote file system.
- `uuid`: a universally unique identifier that distinguishes the FlowFile from others in the system.
- `entryDate`: when the FlowFile entered the system (was created), as milliseconds since midnight 1 Jan 1970 UTC.
- `lineageStartDate`: when the oldest ancestor entered the system (children arise from clone, merge or split); effectively the FlowFile's latency through the system, also in epoch milliseconds.
- `fileSize`: the number of bytes taken up by the FlowFile's content.

`uuid`, `entryDate`, `lineageStartDate` and `fileSize` are system generated and cannot be changed.

Read them with Expression Language, for example `${fileSize:plus(1000)}` (100 becomes 1100) or `${filename:toUpper()}`.

Verify: List queue, then the FlowFile details, shows these keys on a queued FlowFile.

## Checked

Confirmed against the getting-started guide (Common Attributes) and the Expression Language guide (plus, toUpper examples).

Method: docs-only read of cited pages, 2026-11-08
