---
id: computing-software.database-administration.influxdb.go-runtime-profiling-with-pprof
name: go-runtime-profiling-with-pprof
category: computing-software
field: database-administration
product: influxdb
tags: [pprof, profiling, go-tool-pprof, performance, debug]
level: advanced
status: docs-checked
description: "Pull Go runtime profiles from InfluxDB /debug/pprof endpoints, including the /all tarball with cpu sampling, for memory and CPU investigations."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/runtime/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

InfluxDB exposes Go runtime profiles for blocks, CPU, memory allocation, mutexes and OS thread creation under `/debug/pprof`. The default format is compressed profile.proto, readable by `go tool pprof`; some profiles also have plain text with `debug=1`.

Download everything at once (go tool pprof cannot read `/debug/pprof/all` directly):

```sh
curl "http://localhost:8086/debug/pprof/all?cpu=10s" | tar -xz
go tool pprof profiles/heap.pb.gz
```

The tarball holds `profiles/allocs.pb.gz`, `block.pb.gz`, `cpu.pb.gz` (only if you pass `cpu`), `goroutine.pb.gz`, `heap.pb.gz`, `mutex.pb.gz` and `threadcreate.pb.gz`.

Single profiles can be analysed live, for example `go tool pprof http://localhost:8086/debug/pprof/allocs`, then `top10` at the prompt. Sample length uses the `seconds` query parameter; `debug=1` is mutually exclusive with `seconds`.

The CPU profile alone is at `/debug/pprof/profile` (`seconds` defaults to 30); go tool pprof cannot fetch it directly, so save it first with `curl http://localhost:8086/debug/pprof/profile -o cpu`, then run `go tool pprof ./cpu`. Execution traces come from `/debug/pprof/trace`.

## Checked

Method: docs-checked 2026-11-09 against the Runtime profiling (reference/internals/runtime) page, introduction through the trace endpoint. Dropped the unconfirmed `pprof-disabled` sentence.
