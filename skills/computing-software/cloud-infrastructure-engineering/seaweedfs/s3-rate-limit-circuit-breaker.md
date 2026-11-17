---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-rate-limit-circuit-breaker
name: s3-rate-limit-circuit-breaker
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [circuit-breaker, concurrent-uploads, backpressure, rate-limit]
level: advanced
status: docs-checked
description: "Throttle the S3 gateway with upload limits (-concurrentUploadLimitMB) and the s3.circuitBreaker command by action, bucket, count or MB."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Rate-Limiting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 rate limit circuit breaker

Upload limits (queue, never reject):
```bash
weed s3 -filer=localhost:8888 -concurrentUploadLimitMB=256 -concurrentFileUploadLimit=100
```
Defaults: 128 MB total in flight and 0 (unlimited) files. They apply to PUT/POST and apply backpressure. Prometheus metrics: `seaweedfs_s3_inflight_upload_count`, `seaweedfs_s3_inflight_upload_bytes`.

Circuit breaker: stored in the filer at `/etc/s3/circuit_breaker.json` and reloaded dynamically. Actions: `Read`, `Write`, `List`, `Tagging`, `Admin`. Types: `count` (simultaneous requests) and `MB` (simultaneous content size).
```
> s3.circuitBreaker -global -type count -actions Read,Write -values 500,200 -apply
> s3.circuitBreaker -global -type MB -actions Write -values 1024 -apply
> s3.circuitBreaker -buckets mybucket,otherbucket -type count -actions Read,Write -values 200,100 -apply
> s3.circuitBreaker                                          # view
> s3.circuitBreaker -buckets mybucket -disable -apply
> s3.circuitBreaker -buckets mybucket -delete -apply
```
Run `s3.circuitBreaker` without `-apply` to view the current configuration. Changes apply dynamically without restarting the S3 server.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 Rate Limiting: flags and defaults (128, 0 = unlimited), queueing not rejecting, metric names, circuit breaker storage path, actions, types and command examples. Removed the claim about what omitting `-apply` does (the page only says view without it) and the Verify line.
Method: documentation only; no commands were run.
