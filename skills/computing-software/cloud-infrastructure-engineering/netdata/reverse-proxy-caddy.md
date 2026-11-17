---
id: computing-software.cloud-infrastructure-engineering.netdata.reverse-proxy-caddy
name: reverse-proxy-caddy
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, reverse-proxy, caddy, caddyfile]
level: intro
status: docs-checked
description: "Front a Netdata Agent with Caddy using a Caddyfile for a domain or a subfolder with handle_path, and bind Netdata to localhost so Caddy cannot be bypassed."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/running-the-netdata-agent-behind-a-reverse-proxy/Running-behind-caddy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Domain:

```
netdata.domain.tld {
    reverse_proxy localhost:19999
}
```

Subfolder (use `handle_path`, not `handle`):

```
netdata.domain.tld {
    handle_path /netdata/* {
        reverse_proxy localhost:19999
    }
}
```

Restrict Netdata to localhost in `/etc/netdata/netdata.conf`:

```
bind socket to IP = 127.0.0.1
```

or `bind socket to IP = ::1`, so Netdata listens only on localhost.

Gotchas:
- Caddy authentication is separate from the basic config; see Caddy's `basic_auth` directive.
- With Netdata Cloud, bearer token protection replaces the need for Caddy auth.
- Other directives can go inside the braces as needed.

## Checked

2026-11-04. Confirmed against the Netdata Running behind Caddy page: the domain Caddyfile, the handle_path subfolder form, other directives inside the braces, the bearer token alternative with Netdata Cloud, the basic_auth pointer, and the bind socket to IP setting in /etc/netdata/netdata.conf. Removed the restart instruction, the claim about bypassing auth, and the closing Verify step, which the page does not state.

Method: documentation only; no commands were run.
