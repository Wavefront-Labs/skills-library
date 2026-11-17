---
id: computing-software.data-engineering.apache-nifi.common-processors-quickstart
name: common-processors-quickstart
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, processors, getfile, routeonattribute, updateattribute, mergecontent]
level: intro
status: docs-checked
description: "What the getting-started guide says common processors do: GetFile, PutFile, RouteOnAttribute, UpdateAttribute, MergeContent, SplitText, ExtractText, InvokeHTTP and LogAttribute."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/getting-started.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common processors

- GetFile: pulls files from a local directory and deletes the originals; not for copying.
- PutFile: writes content to a local or network directory.
- RouteOnAttribute: Expression Language rules; with "Route to Property name" each property is a relationship; others go to `unmatched`.
- UpdateAttribute: user-defined properties set attributes, may use Expression Language; Advanced UI supports conditional rules.
- MergeContent: concatenate or build ZIP/TAR; bins by attribute, count or bytes, with timeout; can defragment split pieces.
- SplitText: splits by line count.
- ExtractText: regex matches stored as attributes.
- InvokeHTTP: sends a configured HTTP request; needs an incoming FlowFile so it cannot start a flow.
- Also mentioned: LogAttribute, ReplaceText, EvaluateJsonPath, CompressContent, SplitJson, SplitXml, ListenHTTP, GetHTTP, PutSQL.
- Right-click > Usage shows each processor's documentation.

Verify: a GetFile to LogAttribute flow logs attributes for a test file.

## Checked

Confirmed against the NiFi Getting Started guide (processor categories, GetFile move semantics, RouteOnAttribute "Route to Property name" with `unmatched`, UpdateAttribute Advanced UI, MergeContent bins/defragment/timeout, SplitText by lines, ExtractText attributes, InvokeHTTP needing an incoming FlowFile, right-click Usage). Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
