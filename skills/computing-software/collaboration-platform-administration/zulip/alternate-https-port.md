---
id: computing-software.collaboration-platform-administration.zulip.alternate-https-port
name: alternate-https-port
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [alternate-port, nginx-listen-port, external-host]
level: practitioner
status: docs-checked
description: "Serve Zulip on an HTTPS port other than 443 by changing EXTERNAL_HOST, setting nginx_listen_port in zulip.conf and re-applying Puppet."
sources: ["https://zulip.readthedocs.io/en/latest/production/deployment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using an alternate HTTPS port

To serve Zulip on a port other than 443:

1. Edit `EXTERNAL_HOST` in `/etc/zulip/settings.py` to match the new port. This setting controls how the server reports its own URL. Then restart with `~zulip/deployments/current/scripts/restart-server`.
2. Add this block to `/etc/zulip/zulip.conf`:

```
[application_server]
nginx_listen_port = 12345
```

3. As root run `~zulip/deployments/current/scripts/zulip-puppet-apply`. This regenerates Zulip's main nginx configuration to listen on the new port.

A related setting: if Zulip sits behind a proxy that terminates TLS and talks plain HTTP to Zulip, the `http_only = true` option in the same `[application_server]` section applies instead; that is documented with reverse proxies.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/deployment.html (zulip.readthedocs.io, latest). Removed: the example EXTERNAL_HOST value with a port, the both-halves-required explanation and the firewall advice.

Method: documentation only; no commands were run.
