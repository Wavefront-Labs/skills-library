---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.mount-over-internet-mtls
name: mount-over-internet-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [filerproxy, volumeserveraccess, grpc-tls, mtls, remote-mount]
level: advanced
status: docs-checked
description: "Run weed mount or the CSI driver across the internet with mTLS: expose only the filer (filerProxy) or volume servers too, never the master."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Mount-over-the-Internet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mount over internet mtls

A VPN (WireGuard, Tailscale) is simplest and safest. Otherwise use mTLS. The mount needs only filer gRPC (HTTP port + 10000, e.g. 18888) for metadata and volume server HTTP for data; it never talks to the master, which must stay private.

Option A, expose only the filer: reads and writes proxy through the filer.
Server `security.toml`: `[grpc] ca`, `[grpc.filer]` cert/key, `[grpc.client]` cert/key, and `[https.filer]` cert/key/ca (a `ca` makes the port require client certs).
Client `security.toml`: `[grpc] ca`, `[grpc.client]` cert/key, `[https.client] enabled = true` with cert/key/ca.
```bash
weed mount -filer=filer.example.com:8888 -dir=/mnt/weed -volumeServerAccess=filerProxy
```
(CSI parameter `volumeServerAccess: "filerProxy"`.) Trade-off: filer bandwidth becomes the throughput ceiling.

Option B, direct volume access: better throughput, but every volume server exposes HTTPS. Replace `[https.filer]` with `[https.volume]` on servers, and run the filer with `-disableHttp` so its HTTP port serves only static assets.

Verify: from the remote host, `weed mount` succeeds and `ls` works; a client without a certificate is refused.

## Checked
Checked 2026-11-09: the filer gRPC port rule, the never-expose-the-master rule, the VPN recommendation, both security.toml layouts, the filerProxy command and CSI parameter, the throughput trade-off and the `-disableHttp` behaviour in option B match the Mount-over-the-Internet page. Dropped the Security-Overview source (not needed for these claims).
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Mount-over-the-Internet, read in full from a local clone of the wiki.
