---
id: computing-software.systems-network-administration.netbird.posture-checks
name: posture-checks
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, posture-checks, zero-trust, geo-restriction, os-version-check, process-check]
level: practitioner
status: docs-checked
description: "Use NetBird posture checks (client version, location, network range, OS, process, certificate) attached to policies, when they evaluate, and known caveats."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/access-control/posture-checks/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Posture checks make policy access depend on a peer's security state.

Types:
- NetBird client version.
- Country and region: Allow (blocks all other locations) or Block (blocks only the listed).
- Peer network range: matches the peer's local interface subnets and public IP. A /32 rule will not match a NIC on a /24.
- Operating system: OS version on Android, macOS, iOS; kernel version on Linux, Windows. Client 0.26.0+.
- Process: required running applications such as endpoint protection.
- Certificate: see device-certificate-check. 0.81.0+.

Create: Access Control > Posture Checks > Create Posture Check; configure Checks tab, name on Name & Description. A gray dot means inactive until linked to a policy. Attach in a policy's Posture Checks tab (Browse Checks or New Posture Check); several checks per policy are allowed.

Evaluated at connection or login, and mid-session when a peer reports changed metadata (management server 0.74.0+; older servers apply on reconnect).

Caveats:
- Behind a reverse proxy, forward the real client IP (PROXY protocol or `X-Forwarded-For`) or public-IP range checks fail.
- Android below 0.77.1 does not report local NIC addresses: Allow rules fail, Deny rules silently do not apply.
- iOS below 0.69.0 had the same local-range limitation as old Android clients.

## Checked

2026-11-04. Confirmed against the NetBird posture checks page: check types, Allow and Block semantics, network range matching, OS check and 0.26.0, certificate check and 0.81.0, creation and policy steps, gray and green dot, evaluation timing and 0.74.0, proxy note, Android 0.77.1 and iOS 0.69.0 limitations. Reworded the iOS caveat to match the page.
Method: documentation only; no commands were run.
