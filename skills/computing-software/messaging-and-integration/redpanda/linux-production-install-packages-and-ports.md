---
id: computing-software.messaging-and-integration.redpanda.linux-production-install-packages-and-ports
name: linux-production-install-packages-and-ports
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [linux, install, packages, rpm, apt, fips, ports, production-mode]
level: practitioner
status: docs-checked
description: "Install Redpanda on Linux from package repositories, pick redpanda, redpanda-rpk, redpanda-tuner or FIPS packages, know the default ports, and apply production mode and tuning."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/production/production-deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Default ports:** 9092 Kafka API, 8082 HTTP Proxy, 8081 Schema Registry, 9644 Admin API and Prometheus, 33145 internal RPC.

**Packages** (Debian and Red Hat families)
- `redpanda`: the application and libraries; depends on `redpanda-tuner` and `redpanda-rpk` or `redpanda-rpk-fips`.
- `redpanda-rpk`: the Go `rpk` binary; the only package needed if you want rpk alone.
- `redpanda-tuner`: files used to run the tuners.
- FIPS mode (enterprise license): `redpanda-fips` plus `redpanda-rpk-fips`.

**Install**
```bash
curl -1sLf 'https://linux.pkg.redpanda.com/setup-redpanda.rpm.sh' | \
sudo -E bash && sudo yum install redpanda -y
```
Debian and Ubuntu use `setup-redpanda.deb.sh` and `sudo apt install redpanda -y`. The page notes the package repositories are moving from `dl.redpanda.com` to `linux.pkg.redpanda.com` with a new GPG key, and the legacy repository shuts down on September 28, 2026.

To install an older version you must pin every dependency, for example `yum install redpanda-tuner=24.3.1~rc1-1 redpanda-rpk=24.3.1~rc1-1 redpanda=24.3.1~rc1-1`.

**Production mode.** Redpanda installs in development mode with hardware optimization off. As root:
```bash
sudo rpk redpanda mode production
sudo rpk redpanda tune all
```
Kernel changes are not persisted across reboots; enable the `redpanda-tuner` service. The autotuner does not change open file limits.

**I/O config.** `sudo rpk iotune` (about 10 minutes) benchmarks the disk and writes `io-config.yaml`, which Redpanda reads at startup. It can be reused across nodes with the same hardware; a local NVMe SSD should give around 1 GB/s sustained writes.

## Checked

2026-11-04. Ports, package roles, install commands, the repository move notice, version pinning, production mode, tuner service and iotune were confirmed on the Deploy for Production page.

Method: documentation only; no commands were run.
