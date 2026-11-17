---
id: computing-software.systems-network-administration.varnish-cache.install-debian-ubuntu
name: install-debian-ubuntu
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [install-packages, package-repo, debian-ubuntu, apt]
level: intro
status: docs-checked
description: "Install Varnish Cache on Debian or Ubuntu from the Varnish package repository, add the optional extra VMOD packages and find the systemd unit."
sources:
  - https://www.varnish.org/docs/install-guide/install-debian-ubuntu/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# install debian ubuntu

Register the Varnish package repository first, otherwise Debian installs its own (different) version.

```bash
sudo apt-get install -y apt-transport-https curl gpg
sudo mkdir -p /etc/apt/keyrings/
# import the signing key from packages.varnish-software.com into /etc/apt/keyrings/varnish.gpg
source /etc/os-release
sudo apt-get update
sudo apt-get install varnish
```

The repository line has the form `deb [signed-by=/etc/apt/keyrings/varnish.gpg] https://packages.varnish-software.com/varnish/$ID $VERSION_CODENAME main`.

Optional extra VMODs: `varnish-modules`, `vmod-cfg`, `vmod-digest`, `vmod-fileserver`, `vmod-geoip2`, `vmod-jq`, `vmod-querystring`, `vmod-redis`, `vmod-reqwest`, `vmod-rers`, `vmod-uuid`.

varnishd runs under systemd; the unit file is `/lib/systemd/system/varnish.service`.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the generic Verify tip.

Method: documentation only; no commands were run.
