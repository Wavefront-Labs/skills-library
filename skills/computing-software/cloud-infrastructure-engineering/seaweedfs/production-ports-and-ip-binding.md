---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.production-ports-and-ip-binding
name: production-ports-and-ip-binding
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [firewall, weed-server, ip-bind, weed-volume, multi-disk, max-volumes]
level: practitioner
status: docs-checked
description: "Open the right ports and set -ip / -ip.bind for multi-homed SeaweedFS hosts; single-node weed server -filer -s3 with a smaller volume size."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Production-Setup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# production ports and ip binding

Default ports (HTTP / gRPC): master 9333 / 19333, volume 8080 / 18080, filer 8888 / 18888, S3 8333.

Multi-homed hosts: `-ip=xx.xx.xx.xx` sets the address used for cluster communication; `-ip.bind=yy.yy.yy.yy` sets a different user-facing bind. Without `-ip.bind`, each service binds to the `-ip` address and also listens on the same ports on localhost. With `-ip.bind`, each port binds to exactly that address with no extra localhost listener; `-ip.bind=0.0.0.0` listens on all interfaces, loopback included.

Single node:
```bash
weed server -filer -s3 -ip=xx.xx.xx.xx -volume.max=0 -master.volumeSizeLimitMB=1024
```
That is one master, volume server, filer and S3 server. Run several volumes per machine so reads and writes continue while one compacts; the 30GB default needs several free 30GB spaces, so shrink it on small disks.

Masters: one master is fine, even for large clusters: the load is very light, it is unlikely to go down, and it can be restarted because it only holds soft state collected from volume servers. With two machines consensus is not possible, so do not set up multiple masters there. For production the page suggests adding `-metrics.address=<Prometheus gateway address>`.

Verify: open http://ip:9333/ and check that the free volume count is not zero.

## Checked

2026-11-08. Confirmed against the Production Setup wiki page: ports, -ip and -ip.bind behaviour, single-node command, master advice. Removed the unsupported `-ip.bind.localhost=false` flag and the "volume servers are listed" check; replaced with the page's free volume count check.

Method: documentation only; no commands were run.
