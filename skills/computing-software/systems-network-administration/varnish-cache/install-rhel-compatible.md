---
id: computing-software.systems-network-administration.varnish-cache.install-rhel-compatible
name: install-rhel-compatible
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [install-packages, package-repo, rhel-dnf, epel]
level: intro
status: docs-checked
description: "Install Varnish Cache on RHEL-compatible systems with dnf from the Varnish repo, enable EPEL for extra VMODs, then set port, cache size and backend and restart."
sources:
  - https://www.varnish.org/docs/install-guide/install-rhel-compatible/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# install rhel compatible

Covers RHEL and compatible distributions such as Alma Linux and Rocky Linux. Register the repository by writing `/etc/yum.repos.d/varnish.repo`:

```ini
[varnish]
name=varnish
baseurl=https://packages.varnish-software.com/varnish/el/$releasever/$basearch
repo_gpgcheck=1
enabled=1
gpgcheck=0
gpgkey=https://packages.varnish-software.com/varnish/varnish.pub.asc
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
```

Then `sudo dnf install varnish`. On Amazon Linux replace `el` with `amazonlinux` in the baseurl.

Optional extra VMODs (`varnish-modules`, `vmod-cfg`, `vmod-digest`, `vmod-fileserver`, `vmod-geoip2`, `vmod-jq`, `vmod-querystring`, `vmod-redis`, `vmod-reqwest`, `vmod-rers`, `vmod-uuid`): some depend on libraries missing from the base repositories and shipped through EPEL, so first run `sudo dnf install epel-release`. `vmod-digest` cannot currently be installed on AlmaLinux 10 or Amazon Linux 2023 (its mhash library is in neither base nor EPEL there); omit it and the rest install normally.

Configure:

- The packaged unit is `/lib/systemd/system/varnish.service`. Its default `ExecStart` listens on `:6081` (conservative, to avoid clashing with other services), plus `localhost:8443,PROXY`, with `-s malloc,256m`, `-p feature=+http2` and `ExecReload=/usr/sbin/varnishreload`.
- Change parameters with `sudo systemctl edit --full varnish`, which writes `/etc/systemd/system/varnish.service`; or copy the unit there and edit it, then `sudo systemctl daemon-reload`. The page's example changes `-a :80` and `-s malloc,2g`.
- The default `/etc/varnish/default.vcl` has a backend at 127.0.0.1 port 8080; adjust for your web server. Hostnames in VCL are resolved once, at VCL compile time, so DNS changes are not noticed until the VCL is reloaded.
- `sudo systemctl restart varnish` is required for systemd parameter changes; it also reloads the VCL.

## Checked

Method: 2026-11-08 docs-only read of the cited install guide. Removed the earlier `varnishd -V` / `systemctl status` verify step, which the page does not give; added the page's configuration section and the vmod-digest exception (the earlier text listed it without the caveat).
