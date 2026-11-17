---
id: computing-software.messaging-and-integration.apache-camel.file-consumer
name: file-consumer
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, file, consumer, read-lock, idempotent]
level: practitioner
status: docs-checked
description: "Camel file consumer: default .camel move, noop, delete, move, moveFailed, idempotent, readLock modes and timeouts, polling delays, filters, sorting and done files."
sources:
  - https://camel.apache.org/components/next/file-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File consumer

`directoryName` must be a directory (use `fileName` for one file). `autoCreate` true; `jailStartingDirectory` true; no `charset` default (UTF-8 unless `org.apache.camel.default.charset`).

After processing:
- Default with no `move` or `delete`: files go to a `.camel` subfolder.
- `noop` false (true leaves files and turns on `idempotent`), `delete` false.
- `move` runs after the route completes; `preMove` before processing (e.g. `inprogress`); `moveFailed` for failures (not picked up again).

Idempotency: `idempotent` false; key defaults to absolute path, `idempotentKey` e.g. `${file:name}-${file:size}`; default repository is an in-memory LRU of 1000.

`readLock` (default `none`): `markerFile`, `fileLock`, `rename`, `changed`, `idempotent`, `idempotent-changed`, `idempotent-rename`. `readLockTimeout` 10000 ms (0 or less waits forever), `readLockCheckInterval` 1000 ms.

Polling: `initialDelay` 1000, `delay` 500 (ms), `greedy` false, `sendEmptyMessageWhenIdle` false.

Selection: `include`/`exclude` regex (case-insensitive), `antInclude`/`antExclude` (exclude wins), `recursive` false, `maxDepth`, hidden files off, `maxMessagesPerPoll` unlimited. Sorting: `sortBy` e.g. `reverse:file:modified`, `shuffle`.

Done file: `doneFileName` with `${file:name}` or `${file:name.noext}`; deleted after consumption unless `noop`.

Headers: `CamelFileName`, `CamelFileNameOnly`, `CamelFileAbsolutePath`, `CamelFileLength`, `CamelFileLastModified`; batch properties `CamelBatchSize`, `CamelBatchIndex`, `CamelBatchComplete`. Body is a `GenericFile`.

Verify: a consumed file appears in `.camel` and is not re-read.

## Checked

Method: docs-checked 2026-11-09 against https://camel.apache.org/components/next/file-component.html
