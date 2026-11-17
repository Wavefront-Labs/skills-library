---
id: computing-software.collaboration-platform-administration.nextcloud.trusted-proxies-and-forwarded-headers
name: trusted-proxies-and-forwarded-headers
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [reverse-proxy, trusted-proxies, forwarded-for-headers, client-ip, config-php]
level: practitioner
status: docs-checked
description: "Define trusted_proxies and forwarded_for_headers in Nextcloud so the real client IP reaches access control and logging without allowing IP spoofing."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/reverse_proxy_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let Nextcloud see the real client address behind a reverse proxy.

Nextcloud can run behind a reverse proxy that caches static assets, terminates HTTPS or load balances across servers. You must explicitly name which proxies to trust in `config/config.php`. Connections from them are treated specially to recover real client information, used for access control and logging.

`trusted_proxies` is an array of:
- IPv4 addresses
- IPv4 ranges in CIDR notation
- IPv6 addresses
- IPv6 ranges in CIDR notation

```
'trusted_proxies' => ['192.0.2.10', '198.51.100.0/24'],
```

This protects against client spoofing, so secure those servers as you would the Nextcloud server itself.

`forwarded_for_headers` names the HTTP headers carrying the original client IP. The default is `X-Forwarded-For`. The value is an array of PHP lookup strings, so `X-Forwarded-For` becomes `HTTP_X_FORWARDED_FOR`.

```
'forwarded_for_headers' => ['HTTP_X_FORWARDED_FOR'],
```

Warning from the docs: setting `forwarded_for_headers` wrongly can let clients spoof the IP Nextcloud sees, even through a trusted proxy. The right value depends on your proxy software.

Consequence of getting it wrong: brute force protection may start throttling all traffic from the proxy itself (see brute-force-protection-behaviour).

Check: the log and the brute-force whitelist page show a client address, not the proxy address.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/reverse_proxy_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
