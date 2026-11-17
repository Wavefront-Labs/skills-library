---
id: computing-software.systems-network-administration.netbird.peer-session-expiration
name: peer-session-expiration
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, session-expiration, login-required, reauthentication, per-peer-exemption]
level: practitioner
status: docs-checked
description: "Configure NetBird peer session expiration: default 24 hours, period range, setup key exemption, require login after disconnect, desktop warnings and per-peer exemptions."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/settings/enforce-periodic-user-authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Peer session expiration forces periodic re-authentication. It is on by default for new accounts with a 24-hour period.

- Scope: only peers added by interactive SSO login. Setup-key peers are exempt.
- Expired peers show "Login required" in Peers until the user signs in.
- Configure in Settings > Authentication: account-wide on/off and a period from one hour to 180 days.
- Enabling or changing the period disconnects some SSO peers, which must re-authenticate.
- Require login after disconnect: SSO peers disconnected from management for 10 minutes must re-authenticate before reconnecting. Needs expiration enabled; also settable per peer in its detail view.
- Desktop warnings (client v0.75+): notification 10 minutes before and a final dialog 2 minutes before expiry.
- Per-peer exemption: turn off the Session Expiration toggle for a peer in the Peers section; exempt peers show a timer icon.

## Checked

2026-11-04. Confirmed against the NetBird peer session expiration page: 24-hour default, SSO-only scope, Login required status, one hour to 180 days, disconnect warning, 10-minute require login after disconnect, v0.75 desktop warnings at 10 and 2 minutes, per-peer toggle and timer icon. Removed the closing advice on setup keys and ephemeral peers, which the page does not give.
Method: documentation only; no commands were run.
