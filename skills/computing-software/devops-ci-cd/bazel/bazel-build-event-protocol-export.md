---
id: computing-software.devops-ci-cd.bazel.bazel-build-event-protocol-export
name: bazel-build-event-protocol-export
category: computing-software
field: devops-ci-cd
product: bazel
tags: [build-event-protocol, bep, build-event-json-file, build-event-binary-file, bes-backend, build-event-service]
level: advanced
status: docs-checked
description: "Export the Build Event Protocol to a file or a Build Event Service backend for dashboards and IDE tooling."
sources: ["https://bazel.build/remote/bep"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel Build Event Protocol

BEP is a stream of protocol buffer events describing a build: progress, configuration, targets, test results, metrics. Each event has an identifier, a list of child identifiers it announces, and a payload (which may be an `Aborted` message). Events form a DAG; every event except `BuildStarted` is announced by an earlier one. Announcement is not delivery order: events post concurrently, but `TargetComplete`, `TestResult` and `TestSummary` are held back until prerequisites are posted. A build is complete when all announced children are posted or aborted; the last event has `last_message` set. `BuildFinished` carries the authoritative exit code.

Consume it three ways:

```bash
bazel build //foo --build_event_binary_file=/path/to/bep.bin   # length-delimited protos
bazel build //foo --build_event_json_file=/path/to/bep.json
bazel build //foo --build_event_text_file=/path/to/bep.txt
bazel build //foo --bes_backend=grpcs://bes.example.com:443
```

Read the binary file with the protobuf library's `parseDelimitedFrom(InputStream)`; each message is prefixed with a varint length. For a Build Event Service, prefix the address with `grpc://` (plaintext) or `grpcs://` (TLS). Related flags: `--[no]bes_lifecycle_events`, `--bes_results_url`, `--bes_timeout`, `--bes_instance_name`.

Use BEP instead of scraping console output when building IDE plugins or result dashboards.

## Checked

2026-11-04. Read against the Bazel docs page(s): Build Event Protocol (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line.
Method: documentation only; no commands were run.
