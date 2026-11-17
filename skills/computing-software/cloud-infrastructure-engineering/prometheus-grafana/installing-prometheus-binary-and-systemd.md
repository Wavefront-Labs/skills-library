---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.installing-prometheus-binary-and-systemd
name: installing-prometheus-binary-and-systemd
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-installation, prometheus-systemd-unit, prometheus, promtool, linux]
level: intro
status: docs-checked
description: "Install Prometheus from the release tarball with a dedicated user, systemd unit, data directory and validated config; container alternative included."
sources: ["https://prometheus.io/docs/prometheus/latest/installation/", "https://prometheus.io/docs/prometheus/latest/getting_started/", "https://github.com/prometheus/prometheus/releases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Prometheus (binary + systemd)

```bash
VER=<VERSION>   # pick one from https://github.com/prometheus/prometheus/releases
curl -LO https://github.com/prometheus/prometheus/releases/download/v$VER/prometheus-$VER.linux-amd64.tar.gz
sha256sum prometheus-$VER.linux-amd64.tar.gz   # compare with the sha256 digest GitHub lists for that release asset
tar xzf prometheus-$VER.linux-amd64.tar.gz
sudo useradd --system --no-create-home --shell /usr/sbin/nologin prometheus
sudo install -m 0755 prometheus-$VER.linux-amd64/{prometheus,promtool} /usr/local/bin/
sudo install -d -o prometheus -g prometheus /etc/prometheus /var/lib/prometheus
sudo cp prometheus.yml /etc/prometheus/ && promtool check config /etc/prometheus/prometheus.yml
```

`/etc/systemd/system/prometheus.service`:
```ini
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target
[Service]
User=prometheus
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --storage.tsdb.retention.time=15d \
  --web.enable-lifecycle
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
LimitNOFILE=65536
[Install]
WantedBy=multi-user.target
```
`sudo systemctl daemon-reload && sudo systemctl enable --now prometheus`

## Container
`docker run -d -p 9090:9090 -v ./prometheus.yml:/etc/prometheus/prometheus.yml -v prom-data:/prometheus prom/prometheus` (the image runs as `nobody` and declares `/prometheus` as a volume, so the volume must be writable by that user; extra command line flags replace the image's default arguments, so re-add them).

## Gotchas
- Use a local POSIX filesystem for the TSDB; NFS (including AWS EFS) is not supported.
- `--web.enable-lifecycle` (default false) enables `/-/reload` and `/-/quit`; protect them with `--web.config.file` (experimental) or a proxy.
- A reload can also be triggered with SIGHUP, which is what the unit's `ExecReload` does.
- Default retention is 15d; set size-based retention too if disk is fixed.

## Checked
2026-10-28. Confirmed: Prometheus installation and getting started pages (precompiled binaries, `tar xvfz`, `prometheus.yml`),
release list on GitHub (tarball naming `prometheus-<version>.<os>-<arch>.tar.gz`, per-asset sha256 digests), command-line page
(`--web.enable-lifecycle` default false, `--web.config.file`), management API page (`/-/ready`, `/-/reload`, SIGHUP), HTTP API page
(`reloadConfigSuccess`), storage page (15d default retention, NFS unsupported) and the Dockerfile (`USER nobody`, `VOLUME /prometheus`).
Removed: pinned 3.5.0 version, `sha256sums.txt` asset name, uid 65534. The `useradd`, `install` and systemd directives are standard
Linux usage not documented by Prometheus and were not checked against Prometheus sources.
Method: documentation only; no commands were run.

## Verify
- [ ] `curl -s localhost:9090/-/ready` returns 200 once Prometheus can serve queries; `up{job="prometheus"} == 1`.
- [ ] `systemctl reload prometheus` applies a config change (`reloadConfigSuccess` in `/api/v1/status/runtimeinfo` is true).
