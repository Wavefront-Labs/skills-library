---
id: computing-software.messaging-and-integration.apache-camel.stream-caching
name: stream-caching
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, stream-caching, spooling, memory, inputstream]
level: practitioner
status: docs-checked
description: "Camel stream caching: re-readable InputStream bodies, spool-to-disk defaults (128 KB threshold), buffer size, spool directory, per-route enable."
sources:
  - https://camel.apache.org/manual/stream-caching.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream caching

Streams (`StreamSource`, `InputStream`, `Reader`) can be read once; stream caching makes them re-readable. Cached in memory by default.

Defaults:
- `enabled` true
- `bufferSize` 4096
- `spoolEnabled` false (set true to write big streams to a temp file)
- `spoolThreshold` 128 KB (0 or negative keeps everything in memory)
- `spoolDirectory` `${java.io.tmpdir}/camel/camel-tmp-#uuid#`
- `spoolCipher` null (e.g. AES/CTR/NoPadding)
- `spoolUsedHeapMemoryThreshold` 0
- `anySpoolRules` false (all rules must match)
- `removeSpoolDirectoryWhenStopping` true
- `statisticsEnabled` false

Enable: `context.setStreamCaching(true)`, or per route `.streamCache(true)` (XML/YAML `streamCache="true"`). Configure in code via `context.getStreamCachingStrategy()` setters, or in application properties as `camel.main.streamCachingSpoolEnabled` etc. Only `java.io.InputStream` classes are allowed by default (`allowClasses`/`denyClasses` adjust that).

Camel 4.11+ has `StreamCachingProcessor` to convert the body to a `StreamCache` mid-route.

Streams are not logged at DEBUG by default; set `camel.main.globalOptions[CamelLogDebugBodyStreams] = true` to log them.

Verify: with `spoolEnabled=true`, a body over 128 KB creates a file under the spool directory that is deleted after the exchange.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel Stream caching manual page. Confirmed: every StreamCachingStrategy option and default listed, the spool directory default, 128 KB threshold, enabling via context.setStreamCaching, route streamCache, getStreamCachingStrategy setters and camel.main properties, allowed classes default (java.io.InputStream), StreamCachingProcessor since Camel 4.11, and CamelLogDebugBodyStreams for DEBUG logging of streams.
