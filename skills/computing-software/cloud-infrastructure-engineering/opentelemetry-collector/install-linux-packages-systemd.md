---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.install-linux-packages-systemd
name: install-linux-packages-systemd
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, install, linux, deb, rpm, systemd]
level: intro
status: docs-checked
description: "Install the Collector on Linux from DEB or RPM packages and change its systemd options through OTELCOL_OPTIONS."
sources:
  - https://opentelemetry.io/docs/collector/install/binary/linux/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Collector release includes APK, DEB and RPM packaging for Linux amd64, arm64 and i386 systems. The default configuration is `/etc/otelcol/config.yaml` after installation. `systemd` is required for automatic service configuration.

DEB:

```sh
sudo apt-get update
sudo apt-get -y install wget
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v<version>/otelcol_<version>_linux_amd64.deb
sudo dpkg -i otelcol_<version>_linux_amd64.deb
```

RPM:

```sh
sudo yum update
sudo yum -y install wget systemctl
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v<version>/otelcol_<version>_linux_amd64.rpm
sudo rpm -ivh otelcol_<version>_linux_amd64.rpm
```

Manual installation downloads `otelcol_<version>_linux_amd64.tar.gz` with `curl --proto '=https' --tlsv1.2 -fOL` and unpacks it with `tar -xvf`; ppc64le is also available.

As a `systemd` service it starts with `/etc/otelcol/config.yaml`. To change that, edit the `OTELCOL_OPTIONS` variable in `/etc/otelcol/otelcol.conf`, which can also hold additional environment variables for the `otelcol` service. List options with `/usr/bin/otelcol --help`. After changing either file, run `sudo systemctl restart otelcol`, and read logs with `sudo journalctl -u otelcol`.

On Red Hat systems the page's commands install `wget` and `systemctl` first. For the DEB and RPM variants, i386 and arm64 files use the `_linux_386` and `_linux_arm64` names. Installing the package places the default configuration at `/etc/otelcol/config.yaml`.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/install/binary/linux/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
