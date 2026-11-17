---
id: computing-software.email-administration.mailcow.mailcow-local-mta-coexistence
name: mailcow-local-mta-coexistence
category: computing-software
field: email-administration
product: mailcow
tags: [local-mta, relayhost, port-25-conflict, mynetworks, docker-gateway, myhostname]
level: practitioner
status: docs-checked
description: "Run a local host MTA beside dockerized mailcow by disabling its port 25 listener and relaying through the Docker gateway."
sources: ["https://docs.mailcow.email/post_installation/firststeps-local_mta/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Coexisting with a local MTA

Port 25 on the host can only be used by one program. The simplest option is to disable the local MTA's listener on 25/tcp. For a local Postfix, comment out the line beginning `smtp` or `25` in `/etc/postfix/master.cf`.

To relay local mail through mailcow, set the relayhost to the mailcow-created Docker network gateway `172.22.1.1`: `postconf -e 'relayhost = 172.22.1.1'`, `mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128`, `inet_interfaces = loopback-only`, `relay_transport = relay` and `default_transport = smtp`. Relaying over this internal address (rather than the public hostname) is what makes mailcow treat it as a known internal network.

The local MTA's `myhostname` must differ from the FQDN used for dockerized mailcow, for example `local.my.fqdn.tld`. Restart the local MTA after the changes. Note that the docs describe the Postfix commands of the host system, not of the Postfix inside mailcow.

## Checked

2026-11-09. Confirmed on the local MTA page: port 25 listener, master.cf smtp line, relayhost 172.22.1.1 with the postconf settings, myhostname must differ from the mailcow FQDN, gateway explanation and restart. No changes needed.

Method: docs-checked 2026-11-09 against the full local MTA page (firststeps-local_mta.en.md in mailcow-dockerized-docs).
