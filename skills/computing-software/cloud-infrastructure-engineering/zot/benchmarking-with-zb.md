---
id: computing-software.cloud-infrastructure-engineering.zot.benchmarking-with-zb
name: benchmarking-with-zb
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, zb-benchmark, load-testing, concurrency, latency-percentiles, ci-cd-output]
level: practitioner
status: docs-checked
description: "Benchmark a Zot or any OCI registry with zb: build or run it, flags for concurrency, requests, source IPs and output format, and reading the results."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/benchmarking-with-zb.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`zb` benchmarks Zot or other OCI Distribution-compliant registries. Build from source: `make OS=os ARCH=architecture bench` (OS/ARCH: linux or darwin, amd64 or arm64). Syntax: `zb <url> [flags]`.

Flags:
- `-A, --auth-creds`: colon-separated BASIC credentials.
- `-c, --concurrency`: parallel requests (default 1).
- `-n, --requests`: number of requests (default 1).
- `-o, --output-format`: `stdout` (default), `json` or `ci-cd`.
- `-r, --repo`: repo on the remote registry for test data.
- `-s, --src-cidr` or `-i, --src-ips`: source IPs to send from; mutually exclusive.
- `-d, --working-dir`: where to store test data.
- `-v, --version`, `-h, --help`.

Example:

```
bin/zb -c 10 -s 127.0.10.0/24 -n 1000 http://localhost:8080
docker run --net=host -it ghcr.io/project-zot/zb:latest -c 10 -n 1000 -s 127.0.10.0/24 http://localhost:8080
```

Output: a header (Registry URL, Concurrency Level, Total requests, Working dir), then per test the test name, time taken, complete and failed requests, requests per second, `2xx responses`, and latency `min`, `max`, `p50`, `p75`, `p90`, `p99`.

## Checked

Method: docs-checked 2026-11-09 against the full zot benchmarking-with-zb article (raw markdown from project-zot.github.io). Dropped an unsourced tip about per-IP rate limits and ci-cd output.
