---
id: computing-software.collaboration-platform-administration.matrix-synapse.security-hardening-domain-and-firewall
name: security-hardening-domain-and-firewall
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, security, xss, content-repository, firewall, ports, public-baseurl, registered-domain]
level: practitioner
status: docs-checked
description: "Host Synapse on a separate registered domain from web clients and set firewall rules for client port 443 and federation port 8448 or 443, inbound and outbound."
sources:
  - https://element-hq.github.io/synapse/latest/setup/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Matrix serves raw user-supplied data through the content repository endpoints. Synapse makes a reasonable effort against XSS (for example with a Content Security Policy), but a homeserver should not be hosted on a domain that also hosts other web applications. This especially means Matrix web clients and sensitive apps such as webmail.

Ideally Synapse is not just on a different subdomain but on a different registered domain (eTLD+1), because some attacks remain possible while the two applications share a registered domain. The page's example: if Element Web is at `A.example1.com`, host Synapse on `example2.com`. Hosting it at `B.example1.com` gives some protection and is acceptable in some scenarios, but never put Synapse on `A.example1.com`. This concerns only the domain in `public_baseurl`, not the domain in MXIDs. The aim is that an XSS found in Synapse has minimal impact on other applications.

Firewall rules serve two purposes. Client access uses TCP 443 by default and must be allowed inbound. Federation uses TCP 8448 by default, or 443 when run with delegation or behind a reverse proxy, and the federation port must be allowed inbound. If outbound traffic is allowlisted, allow both 443 and 8448 outbound, since both ports are usually used for federation.

| Direction | Port | Description |
|---|---|---|
| Inbound | 443 | Client access |
| Inbound | 8448 and/or 443 | Federation, depending on the port used |
| Outbound | 8448 and 443 | Federation outbound |

## Checked

2026-11-04. Confirmed against the Synapse Security page: content repository domain advice, eTLD+1 example, public_baseurl scope, firewall ports and table. Removed the cookie-attack detail and a closing tip not on the page.
Method: documentation only; no commands were run.
