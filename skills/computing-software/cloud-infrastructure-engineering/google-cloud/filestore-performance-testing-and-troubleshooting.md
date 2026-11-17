---
id: computing-software.cloud-infrastructure-engineering.google-cloud.filestore-performance-testing-and-troubleshooting
name: filestore-performance-testing-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, filestore, filestore-performance, nfs-performance, fio, nconnect, throughput-limits]
level: practitioner
status: gated
description: "Benchmark and tune Filestore: expected throughput and IOPS per tier and capacity, fio tests, NFS client mount options like nconnect, client VM limits, and Filestore metrics."
sources: ["https://cloud.google.com/filestore/docs/performance", "https://cloud.google.com/filestore/docs/troubleshooting", "https://cloud.google.com/filestore/docs/monitoring-instances"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filestore performance testing and troubleshooting

## Know the ceiling
Filestore performance scales with tier and provisioned capacity (Basic HDD/SSD fixed-ish; Zonal
and Regional scale throughput/IOPS with capacity; Enterprise similar). Look up the table on the
performance page for your size; a 1 TiB Basic HDD will never do 1 GB/s.

## Client limits too
- VM network egress cap depends on machine type; a small VM bottlenecks before Filestore (the performance page recommends a machine type with at least 16 Gbps egress for cache-friendly workloads).
- Single NFS TCP connection limits throughput; use `nconnect` (Linux kernel 5.3+) on Zonal/Regional/Enterprise.

## Mount options
```bash
sudo mount -t nfs -o rw,hard,timeo=600,retrans=3,rsize=1048576,wsize=1048576,nconnect=7,noatime \
  10.0.0.2:/share1 /mnt/share1
```
`hard` (not `soft`) to avoid silent data corruption on timeouts.

## Benchmark with fio
```bash
fio --name=seqwrite --directory=/mnt/share1/fio --rw=write --bs=1M --size=10G --numjobs=8 --ioengine=libaio --direct=1 --group_reporting
fio --name=randread --directory=/mnt/share1/fio --rw=randread --bs=4k --size=4G --numjobs=16 --iodepth=64 --ioengine=libaio --direct=1 --group_reporting
```
Run from several clients in parallel to reach instance limits; one client measures client limits.

## Metrics
`file.googleapis.com/nfs/server/read_bytes_count`, `write_bytes_count`, `procedure_count` (gated: unconfirmed, source is paywalled or blocked),
`average_read_latency`, `free_bytes_percent`, and for Zonal/Regional/Enterprise `cpu_usage`.
Throttling shows as latency rising while throughput is flat at the tier limit.

## Common problems
| Symptom | Cause |
|---|---|
| Slow `ls` on big dirs, metadata-heavy workloads | small-file metadata ops; split directories, use Zonal/Regional tiers |
| Throughput flat at a low ceiling | Basic HDD at small capacity; scale or change tier |
| Stalls then recovers | client network cap or `soft` mount retries |
| Mount hangs | firewall: allow TCP 111, 2046, 2049, 2050, 4045 from clients to the reserved range |

## Verify
- [ ] Multi-client fio reaches within ~10% of the documented limit for the instance size.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the per-vCPU egress figure and the throughput ceiling in MB/s. Gated: the Filestore Cloud Monitoring metric names read_bytes_count, write_bytes_count and procedure_count were not found in the fetched pages.

Method: documentation only; no commands were run.
