---
id: computing-software.systems-network-administration.varnish-cache.varnishlog-basics
name: varnishlog-basics
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [varnishlog, vsl, log-grouping, shared-memory-log]
level: practitioner
status: docs-checked
description: "Read Varnish logs with varnishlog: why there is no log file, -d backlog, -g grouping, -q queries, -w/-r binary files, and sizing the circular buffer with vsl_space."
sources:
  - https://www.varnish.org/docs/tutorials/vsl-cheatsheet/
  - https://www.varnish.org/docs/tutorials/varnishlog/
  - https://www.varnish.org/docs/tutorials/varnish-access-logs-varnishncsa/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# varnishlog basics

Varnish writes logs to an in-memory circular buffer (VSL), not to files, so logging is fast and a consumer tool reads it. The buffer is `vsl_space` (default 80M, needs a restart; `-l` is shorthand). The VSM should reside on a tmpfs volume.

```bash
varnishlog                              # live, per-transaction
varnishlog -d                           # read the existing backlog, then exit
varnishlog -g request                   # group client request with its backend requests
varnishlog -q 'ReqURL eq "/foo"' -g request
varnishlog -i RespHeader:^Age           # only some tags (-I regex, -x/-X to exclude)
varnishlog -d -g raw -w /path/to/log.bin   # save binary
varnishlog -r /path/to/log.bin          # read it back
```

A client transaction shows tags like `ReqMethod`, `ReqURL`, `VCL_call`, `VCL_return`, `Timestamp`, `RespStatus`, `ReqAcct`; a backend transaction shows `BereqURL`, `BackendOpen`, `BerespStatus`, `TTL`, `Storage`.

varnishlog is for debugging; for stored access logs use varnishncsa.

Limit what is recorded with `vsl_mask` and `vsl_reclen` (default 255 bytes per record).

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the SIGHUP log-rotation claim (not on the pages) and corrected the tmpfs note to the VSM.

Method: documentation only; no commands were run.
