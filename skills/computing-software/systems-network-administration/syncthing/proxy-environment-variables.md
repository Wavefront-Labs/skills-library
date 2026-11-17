---
id: computing-software.systems-network-administration.syncthing.proxy-environment-variables
name: proxy-environment-variables
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, proxy, all-proxy, socks5]
level: practitioner
status: docs-checked
description: "Run Syncthing behind a SOCKS5, HTTP or HTTPS proxy with all_proxy and disable direct fallback with ALL_PROXY_NO_FALLBACK."
sources: ["https://docs.syncthing.net/users/proxying.html", "https://docs.syncthing.net/users/syncthing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using a proxy

## Configuration
Proxy support was added in version 0.12.0. There is no graphical configuration. Set the `all_proxy` environment variable (or `ALL_PROXY`, which wins if both are set) to the proxy URL before starting Syncthing:

```sh
export all_proxy=socks5://10.20.30.40:5060
export all_proxy=http://10.20.30.40:8080
export all_proxy=https://user:password@proxy.example.com:8443
syncthing
```
The log prints `Proxy settings detected`. Support for HTTP and HTTPS proxies via `all_proxy` was added in 2.1.0. Basic-authentication credentials can be embedded in the proxy URL; a warning is logged when they are used over a cleartext HTTP proxy.

## Limits
- Only outbound connections go through the proxy. A proxied instance cannot accept incoming ones, though relays can still deliver inbound traffic.
- Through an HTTP or HTTPS proxy only outbound TCP works. Non-TCP transports and listening sockets are not supported.
- `http_proxy` and `https_proxy` are also honoured, and apply behind the `all_proxy` proxy. Unset them if you do not want that.

## Disable fallback
Added in version 0.13.0. By default Syncthing attempts a direct connection if a connection via the proxy fails. To force all connections through the proxy, for example a Tor proxy, set the variable with capital letters:

```sh
export ALL_PROXY_NO_FALLBACK=1
```
The log then prints `Proxy fallback disabled`.

## Checked
2026-11-04. Read Using Proxies and Command Line Operation (proxy section): `all_proxy`/`ALL_PROXY` precedence, example URLs, log messages, version notes (0.12.0, 0.13.0, 2.1.0), outbound-only limit with relay exception, HTTP/HTTPS TCP-only caveat, and the `http_proxy`/`https_proxy` interaction. Only wording was adjusted.
Method: documentation only; no commands were run.
