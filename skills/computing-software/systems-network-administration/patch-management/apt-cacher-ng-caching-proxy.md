---
id: computing-software.systems-network-administration.patch-management.apt-cacher-ng-caching-proxy
name: apt-cacher-ng-caching-proxy
category: computing-software
field: systems-network-administration
product: patch-management
tags: [apt-cacher-ng, apt-proxy, package-cache, patch-acquisition, debian, ubuntu]
level: practitioner
status: docs-checked
description: "Run apt-cacher-ng as a caching proxy for Debian/Ubuntu patching: install, client proxy config, HTTPS passthrough, cache expiry and troubleshooting stale metadata."
sources:
  - https://www.unix-ag.uni-kl.de/~bloch/acng/html/index.html
  - https://www.unix-ag.uni-kl.de/~bloch/acng/html/config-servquick.html
  - https://www.unix-ag.uni-kl.de/~bloch/acng/html/howtos.html
  - https://www.unix-ag.uni-kl.de/~bloch/acng/html/maint.html
  - https://manpages.debian.org/stable/apt-cacher-ng/apt-cacher-ng.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apt-cacher-ng caching proxy

Saves WAN bandwidth when many Debian/Ubuntu hosts patch from the same mirrors. It caches on demand; it is not a snapshot tool.

## Server
```sh
apt install apt-cacher-ng          # service port 3142
systemctl enable --now apt-cacher-ng
```
Key settings in `/etc/apt-cacher-ng/acng.conf`:
```text
Port: 3142
PassThroughPattern: <regex>         # lets clients tunnel HTTPS through the proxy (not cached)
```
`PassThroughPattern` takes a regular expression matched against the host and port; `.*` permits any host and port, so narrow it to limit access. The maintenance report page (statistics and the manual Expiration operation) is served by the daemon: browse to the server on port 3142 and follow the report link.

## Clients
```sh
echo 'Acquire::http::Proxy "http://acng.example.com:3142";' > /etc/apt/apt.conf.d/02proxy
```
The project manual suggests a file such as `/etc/apt/apt.conf.d/02proxy`; the alternative is to rewrite mirror hostnames in sources.list to `http://<acng-host>:3142/<mirror-host>/...`.
For HTTPS sources either set `PassThroughPattern` (works, no caching) or write the source with the `HTTPS///` marker between `http://` and the host name (for example `deb http://HTTPS///get.docker.com/ubuntu docker main` with the proxy configured in APT), so acng fetches upstream over HTTPS and caches the files.

## Expiry
Files no longer referenced by any index file are removed by the Expiration cleanup, which can be run manually from the report page or automatically (see the manual chapter on maintenance).

## Troubleshooting
- Stale index files ("volatile" files such as Release and Packages change under the same URL): run the Expiration task from the report page and check the server clock.
- Hosts that must be reachable through acng need a repository mapping (`Remap-...` lines) or a matching `PassThroughPattern`.
- Clients bypass the proxy if their proxy exceptions list the mirror.

## Gotchas
- Not appropriate for staged rings; every client gets latest upstream state.
- Single point of failure for patch windows; monitor port 3142 and disk.

## Verify
Second host's `apt-get update && apt-get -s upgrade` completes fast and the acng report page shows cache hits rising.

## Checked

Checked 2026-10-27 against the apt-cacher-ng user manual (quick start, how-tos, maintenance and server configuration chapters).
- Service port 3142; APT proxy line `Acquire::http::proxy` in `/etc/apt/apt.conf.d/02proxy`; rewriting sources.list as an alternative: confirmed.
- `PassThroughPattern` regex semantics for HTTPS CONNECT (no caching) and the `HTTPS///` URL marker (cached): confirmed.
- Volatile versus package files, Expiration cleanup (manual from the report page or automatic), `Remap-...` mapping: confirmed.
- Removed unconfirmed: cache directory default, `ExThreshold` meaning, report page file name, log file path, the 503 explanation, auto-detection helper packages.
Method: documentation only; no commands were run.
