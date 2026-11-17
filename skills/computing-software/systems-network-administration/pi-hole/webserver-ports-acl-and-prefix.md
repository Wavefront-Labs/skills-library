---
id: computing-software.systems-network-administration.pi-hole.webserver-ports-acl-and-prefix
name: webserver-ports-acl-and-prefix
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [webserver-port, webserver-acl, reverse-proxy-prefix]
level: advanced
status: docs-checked
description: "Configure the Pi-hole web server: ports with the o, r and s flags, access control list, threads and a reverse proxy prefix."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Web server ports, ACL and prefix

**Ports.** `webserver.port` is a comma-separated list, default `80o,443os,[::]:80o,[::]:443os`.

- `s` marks a TLS port: `80,443s`.
- `r` redirects an unencrypted port to the first SSL port: `80r,443s`.
- `o` makes a port optional so failure to bind is not an error.
- Prefix an IP and colon to bind to one address: `127.0.0.1:80,8080`.
- `+80` opens one socket for IPv4 and IPv6; if it fails use `80,[::]:80`.
- An empty value means the web server (and therefore the API) does not start.

**ACL.** `webserver.acl` is a list of subnets each with `+` (allow) or `-` (deny). If empty, all access is allowed. Otherwise the default is deny, and the last matching entry wins. Examples: `+127.0.0.1,+[::1]` or `+192.168.0.0/16`.

**Other options**

- `webserver.threads` (default `50`): concurrent connections; extra ones queue. `0` means 50.
- `webserver.domain` (default `pi.hole`).
- `webserver.paths.prefix` (default empty): for a reverse proxy serving the interface at, for example, `/pihole/admin/` (prefix `/pihole`); the proxy must strip the prefix, as in the reference's Traefik `stripprefix` example. A wrong value can make the interface unreachable. This, `webroot` and `webhome` cannot be set via the API.

**Other files.** If `webserver.serve_all` is `false` (default), only files under `webserver.paths.webhome` (default `/admin/`) and `/api` are served; `true` serves everything under `webserver.paths.webroot` (default `/var/www/html`).

**Checklist**

1. The default keeps `443os` for HTTPS.
2. The ACL's last matching entry wins, so order entries deliberately.

## Checked

2026-11-03. Read the `[webserver]` (domain, acl, port, threads, serve_all) and `[webserver.paths]` (webroot, webhome, prefix) sections of the FTL configuration reference. Removed the Lua Server Pages claim (not on the page) and the restart item.

Method: documentation only; no commands were run.
