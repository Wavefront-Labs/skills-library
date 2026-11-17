---
id: computing-software.systems-network-administration.windows-server.nps-radius-proxy-and-remote-server-groups
name: nps-radius-proxy-and-remote-server-groups
category: computing-software
field: systems-network-administration
product: windows-server
tags: [nps, radius-proxy, remote-radius-server-groups, connection-request-policy, radius-clients]
level: advanced
status: docs-checked
description: "Configure NPS as a RADIUS proxy: remote RADIUS server groups, connection request policies by realm, load balancing, failover thresholds and accounting forwarding."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-proxy-lb
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-crp-rrsg-configure
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-crp-realm-names
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-crp-crpolicies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPS RADIUS proxy and remote RADIUS server groups

An NPS configured as a proxy forwards connection requests to other RADIUS servers (other NPS servers or third-party RADIUS)
according to connection request policies: realm-based routing to other domains or partners, or load balancing across a group.

## Remote RADIUS server group
NPS console > RADIUS Clients and Servers > Remote RADIUS Server Groups > New:
- Add each member with the shared secret on the Authentication/Accounting tab (the proxy must be registered as a RADIUS client on that server with the same secret) and check the authentication and accounting ports.
- **Priority**: integer, lower number is higher priority (1 is primary).
- **Weight**: 1 to 100, a percentage of requests among members of equal priority.
- **Advanced** failover settings: seconds to wait for a response before a request is considered dropped, maximum dropped requests before the server is marked unavailable, and seconds between requests before it is marked unavailable.
- Best practice from the docs: have RADIUS clients send to two NPS proxies, and let the proxies load balance across the RADIUS servers.

## Connection request policy
Policies > Connection Request Policies > New:
- Conditions: for example NAS Port Type, Calling Station ID, and User Name (match the realm).
- Settings > Authentication: forward requests to a remote RADIUS server group.
- Attribute manipulation: find-and-replace rules on User-Name, for example realm stripping (`user1@example.com` becomes `user1`).
- Accounting: forward accounting to a remote RADIUS server group; this works independently of local accounting.
- Policies are evaluated in order and the first matching policy applies. A pure proxy deletes (or does not rely on) the default policy, which processes requests locally.

## Gotchas
- The downstream server sees the proxy as its RADIUS client, so register the proxy there.
- If you do not use EAP, the group setting "Request must contain the message authenticator attribute" can be enabled.

## Verify
- [ ] The back-end server logs requests from the proxy's address; the proxy forwards matching realms and handles failover when one member is stopped.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed priority and weight semantics (priority lowest first, weight 1 to 100), the three advanced failover settings, the two-proxies best practice, realm stripping through User-Name attribute manipulation, first-matching connection request policy behaviour, independent accounting forwarding, and the message authenticator option. Removed the unconfirmed netsh add remoteserver example, the default timeout figures and the chain-timeout rule.

Method: documentation only; no commands were run.
