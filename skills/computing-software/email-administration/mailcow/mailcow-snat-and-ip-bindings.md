---
id: computing-software.email-administration.mailcow.mailcow-snat-and-ip-bindings
name: mailcow-snat-and-ip-bindings
category: computing-software
field: email-administration
product: mailcow
tags: [snat, outgoing-ip, ip-binding, ipv6-binding, docker-compose-override, netfilter-mailcow]
level: advanced
status: docs-checked
description: "Choose the outgoing IP with SNAT_TO_SOURCE and bind mailcow services to specific IPv4 or IPv6 addresses using mailcow.conf and a compose override."
sources: ["https://docs.mailcow.email/post_installation/firststeps-snat/", "https://docs.mailcow.email/post_installation/firststeps-ip_bindings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow SNAT and IP bindings

Source NAT changes the source address of packets mailcow sends, which selects the outgoing IP on hosts with several addresses. In `mailcow.conf` set `SNAT_TO_SOURCE=1.2.3.4` and/or `SNAT6_TO_SOURCE=<ipv6>`, then recreate the containers. netfilter-mailcow reads the values and keeps its post-routing rules at position 1 of the netfilter table, recreating them if they move.  Check with `docker compose logs --tail=200 netfilter-mailcow` that the SNAT settings were applied.

Changing a binding does not affect source NAT; the two are configured separately.

IPv4 bindings: edit `HTTP_PORT`/`HTTP_BIND`, `HTTPS_PORT`/`HTTPS_BIND`, and the other service variables as `SMTP_PORT=1.2.3.4:25`. Specifying an IPv4 address skips all IPv6 bindings since Docker 20.x. `DOVEADM_PORT`, `SQL_PORT` and `SOLR_PORT` default to local ports (`127.0.0.1:19991`, `127.0.0.1:13306`, `127.0.0.1:18983`) and are bound to local ports only; the config comment says not to change that unless you know what you are doing. Apply IPv4 changes with `docker compose down` then `docker compose up -d`.

IPv6 bindings are done in `docker-compose.override.yml` so updates do not overwrite them. Under `dovecot-mailcow`, `postfix-mailcow` and `nginx-mailcow` add `ports` entries like `'[2001:db8:dead:beef::123]:993:993'`. The first port is external; the second is the container port and must not change. Apply with `docker compose down` then `docker compose up -d`.

## Checked

2026-11-04. Confirmed on the SNAT and IP bindings pages: SNAT_TO_SOURCE and SNAT6_TO_SOURCE in mailcow.conf, netfilter-mailcow keeping post-routing rules at position 1, the log check command, the HTTP/HTTPS and other service port variables, the IPv4 skips-IPv6 note since Docker 20.x, the local-only DOVEADM/SQL/SOLR defaults, the docker-compose.override.yml IPv6 ports for dovecot, postfix and nginx, and the external:container port rule. Fixed: apply step is down then up, not just up. Removed: "set both if needed" and "should not be changed lightly" paraphrases.

Method: documentation only; no commands were run.
