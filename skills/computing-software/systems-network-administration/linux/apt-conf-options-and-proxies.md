---
id: computing-software.systems-network-administration.linux.apt-conf-options-and-proxies
name: apt-conf-options-and-proxies
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apt, apt-conf, apt-proxy, apt-conf-d, acquire-http-proxy, apt-config-dump, install-recommends]
level: practitioner
status: docs-checked
description: "Configure apt via /etc/apt/apt.conf.d: HTTP/HTTPS proxies per host, Install-Recommends, retries and timeouts, dpkg options for unattended config prompts, and apt-config dump."
sources:
  - https://manpages.debian.org/bookworm/apt/apt.conf.5.en.html
  - https://manpages.debian.org/bookworm/apt/apt-config.8.en.html
  - https://manpages.debian.org/bookworm/apt/apt-transport-http.1.en.html
  - https://manpages.debian.org/bookworm/apt/apt-get.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apt.conf.d options and proxies

Files in `/etc/apt/apt.conf.d/` are read in lexical order; later files override. Syntax is `Group::Option "value";`.
Show the effective config: `apt-config dump | grep -i proxy`.

## Proxies
```
// /etc/apt/apt.conf.d/80proxy
Acquire::http::Proxy  "http://proxy.corp:3128/";
Acquire::https::Proxy "http://proxy.corp:3128/";
Acquire::http::Proxy::deb.internal.corp "DIRECT";      // bypass for an internal repo
Acquire::http::Proxy-Auto-Detect "/usr/local/bin/detect-proxy";   // script prints proxy URL or DIRECT
```
One-off: `apt -o Acquire::http::Proxy=http://p:3128 update`. The `http_proxy` environment variable is also supported system wide (apt-transport-http(1)).

## Common options
```
APT::Install-Recommends "false";          // lean servers/containers
APT::Install-Suggests "false";
Acquire::Retries "3";
Acquire::http::Timeout "20";
Acquire::Languages "none";                 // download/use no Translation files
APT::Periodic::Update-Package-Lists "1";   // read by /usr/lib/apt/apt.systemd.daily (see apt.conf(5), Periodic and Archives options)
Dpkg::Options { "--force-confdef"; "--force-confold"; };   // keep existing configs without prompting
```
Non-interactive runs: `DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::=--force-confold upgrade`.

## Gotchas
- A missing `;` or quote in a file under `apt.conf.d` breaks every apt command; check the file named in the error.
- `--force-confold` silently keeps old configs — new mandatory options in the package's version may be missed; review `.dpkg-dist` files.

## Verify
- [ ] `apt-config dump` shows the settings; `apt update` succeeds through the proxy (watch the proxy log).

## Checked

Checked against the apt source documentation (Debian/apt doc/, latest commit 2025-11-10, apt 3.x) and dpkg(1) from the dpkg repository.
Confirmed: `Acquire::http::Proxy`, per-host `Proxy::<host> "DIRECT"` and `Proxy-Auto-Detect` and `Acquire::http::Timeout` (apt-transport-http(1)); `Acquire::Retries`; `Acquire::Languages=none`; `APT::Install-Recommends` and `Install-Suggests` (apt-get(8)); `APT::Periodic` is handled by apt.systemd.daily (apt.conf(5)); `--force-confdef`/`--force-confold` semantics (dpkg(1)); `apt-config dump`.
Removed as unconfirmed: the `Dpkg::Progress-Fancy` option, the sudo/`http_proxy` remark, the apt-cacher-ng remark, the exact syntax-error text and the intercepting-proxy remark.

Method: documentation only; no commands were run.
