---
id: computing-software.software-engineering.pnpm.network-proxy-settings
name: network-proxy-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [https-proxy, http-proxy, no-proxy, network-concurrency, fetch-retries, fetch-timeout, strict-ssl, max-tarball-unpacked-size, git-shallow-hosts]
level: practitioner
status: docs-checked
description: "Tune pnpm networking: proxy fallbacks and encoded credentials, noProxy, maxsockets, networkConcurrency, fetch retry and timeout settings, strictSsl and maxTarballUnpackedSize."
sources:
  - https://pnpm.io/settings/network
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxies:
- `httpsProxy` falls back to legacy `proxy`, then `HTTPS_PROXY`/`https_proxy`. `httpProxy` falls back to the resolved https proxy, then `HTTP_PROXY`, then `PROXY`/`proxy`. `noProxy` falls back to `noproxy`, then `NO_PROXY`; `npmjs.org` and `.npmjs.org` both cover the domain and subdomains.
- URL-encode credentials but not the colon: `httpsProxy: "https://use%21r:pas%2As@my.proxy:1234/foo"`.
- Empty, `false` and `null` in config files read as unset; to turn proxying off set `proxy` to `false`. On the command line `false` and `null` are host names.

Connections:
- `maxsockets` (alias `maxSockets`): per-origin limit; unset means 50 through a proxy, otherwise bounded by `networkConcurrency`; `0` removes the proxied limit.
- `networkConcurrency`: default is clamp(workers x 3, 64, 96). After a timeout with other requests in flight to the same host, that host drops to one request for the rest of the command. Per-registry limit lives in the `registries` entry.
- `localAddress`, `strictSsl` (true; `--no-strict-ssl` disables validation), `userAgent`.

Retries and timeouts:
- `fetchRetries` 2, `fetchRetryFactor` 10, `fetchRetryMintimeout` 10000 ms, `fetchRetryMaxtimeout` 60000 ms.
- `fetchTimeout` 60000 ms resets on every received chunk (per-request total before v12.4.0).
- `fetchWarnTimeoutMs` 10000, `fetchMinSpeedKiBps` 50 warn only.

Other:
- `gitShallowHosts`: hosts cloned shallow (github.com, gitlab.com, bitbucket...).
- `maxTarballUnpackedSize` (v12.15.0) default 4 GiB, checked while decoding.

## Checked

2026-11-04. Confirmed every default, fallback order, alias and version note against pnpm.io/settings/network. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
