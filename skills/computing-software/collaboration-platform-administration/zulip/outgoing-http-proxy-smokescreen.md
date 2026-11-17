---
id: computing-software.collaboration-platform-administration.zulip.outgoing-http-proxy-smokescreen
name: outgoing-http-proxy-smokescreen
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [smokescreen, http-proxy, ssrf, allow-addresses]
level: advanced
status: docs-checked
description: "Control Zulip's outgoing HTTP proxy Smokescreen: allow internal webhook addresses, swap in a custom proxy, Camo and S3 behaviour, and a separate Smokescreen host."
sources: ["https://zulip.readthedocs.io/en/latest/production/deployment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip's outgoing HTTP proxy (Smokescreen)

To block server-side request forgery, Zulip sends all outgoing HTTP and HTTPS traffic through Smokescreen, a `CONNECT` proxy. This covers outgoing webhooks, website previews and push notifications. By default it denies every non-public address, including 127.0.0.1, and allows public hosts.

To permit an internal target such as a webhook at `http://10.17.17.17:80/`, add to `/etc/zulip/zulip.conf`:

```
[http_proxy]
allow_addresses = 10.17.17.17
```

To use your own proxy instead, set `host` and `port` in the same `[http_proxy]` section (for example 127.0.0.1 and 4750). An empty `host` disables proxying; the docs warn against it, since it lets attackers reach internal resources through the server.

After any change run `~zulip/deployments/current/scripts/zulip-puppet-apply`, which reconfigures and restarts the service.

Camo, the image proxy, uses a custom outgoing proxy if one is configured but not Smokescreen, because it filters private subnets itself; the `proxy.enable_for_camo` option overrides this in either direction.

The S3 uploads backend bypasses Smokescreen by default, since EC2 instance metadata at 169.254.169.254 would be blocked. Set `S3_SKIP_PROXY = False` in `/etc/zulip/settings.py` if your storage needs the proxy.

With several frontends, apply `zulip::profile::smokescreen` on a separate host and point `[http_proxy]` at it.

## Checked

Confirmed against the Customizing the outgoing HTTP proxy section of the deployment page (IP address rules, custom proxy host and port, empty host warning, Camo behaviour, S3_SKIP_PROXY, separate Smokescreen host). Nothing removed.

Method: docs-checked 2026-11-09 against docs/production/deployment.md in the zulip/zulip repository (main), the source of the cited page.
