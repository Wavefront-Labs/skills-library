---
id: computing-software.cloud-infrastructure-engineering.netdata.streaming-compression-bandwidth
name: streaming-compression-bandwidth
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, bandwidth, stream-compression, zstd]
level: advanced
status: docs-checked
description: "Choose a Netdata streaming compression algorithm order in stream.conf, with the documented zstd bandwidth figure and what Cloud traffic carries."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/sizing-netdata-agents/bandwidth-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Documented figure: with `zstd`, 1 million samples per second is about 84 Mbps (10.5 MiB/s).

Algorithms:
- `zstd`: default, best CPU versus compression balance.
- `lz4`: fastest; choose when CPU matters more than bandwidth.
- `gzip`: better compression at more CPU; choose when bandwidth matters more.
- `brotli`: most CPU, best compression.

Set the order per `[API KEY]` in `stream.conf`:

```
compression algorithms order = zstd lz4 brotli gzip
```

The first algorithm, left to right, available on both Child and Parent is used. Compression can be disabled in `stream.conf` on either side.

Standalone bandwidth comes from remote collection jobs (none enabled by default), dashboard use and Netdata Cloud communication. Cloud receives metadata only (system info, running collectors and jobs, available metrics and retention, alert configuration and transitions): a handshake at startup, then updates on status changes. Samples reach Cloud only while a user views a dashboard, usually aggregated.

## Checked

2026-11-04. Confirmed against the Netdata Bandwidth Requirements page: the 84 Mbps (10.5 MiB/s) zstd figure, the four algorithm roles with zstd as default, the compression algorithms order line and left-to-right selection, disabling on either side, the standalone bandwidth sources and the Cloud metadata list. Removed the closing edit-config and restart line, which the page does not state.

Method: documentation only; no commands were run.
