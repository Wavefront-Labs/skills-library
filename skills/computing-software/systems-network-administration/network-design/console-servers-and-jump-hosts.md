---
id: computing-software.systems-network-administration.network-design.console-servers-and-jump-hosts
name: console-servers-and-jump-hosts
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, remote-management, console-server, serial-console, out-of-band, oob, jump-box, bastion, lte-oob, opengear, rollover-cable, usb-console, ssh-proxyjump, session-recording, privileged-access]
level: practitioner
status: docs-checked
description: "Design out-of-band and privileged access to network gear: console servers with LTE backup, serial settings, hardened jump hosts with ProxyJump, MFA, session logging."
sources:
  - https://www.comptia.org/certifications/network
  - https://man.openbsd.org/ssh_config#ProxyJump
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Console servers and jump hosts

## Out-of-band console access
When the production network fails (bad change, routing loop, firmware upgrade), SSH dies with
it. A console server gives serial access independent of the data network.
- One console server per rack/site; ports cabled to every switch/router/firewall console.
- Independent uplink: separate management switch/ISP, plus **LTE/5G cellular** failover.
- Cabling: check each device's console port type (RJ45 or USB) and pinout against the console server's
  port documentation; gear with USB consoles may need USB console ports or adapters.
- Serial settings: match each device's documented baud rate and framing. Name ports after the
  device so the console server's menu or web UI lands on the right box.
- Security: MFA/AAA to the console server, per-port authorisation, logging of console sessions,
  and an idle timeout on device console lines so sessions are not left logged in.

## Jump hosts (bastions)
All in-band management SSH/HTTPS goes **only** from jump hosts (or a PAM tool); device VTY
ACLs/management-plane ACLs allow only those sources.
- Hardened, patched, minimal software; MFA at login; no internet browsing from it.
- Users authenticate individually (no shared accounts); device access via TACACS+/RADIUS with
  per-user accounting.
- Session recording/logging (PAM products, or `script`/tlog on Linux) for audit.
- SSH config for engineers:
  ```
  Host jump
      HostName jump01.mgmt.example
      User alice
  Host 10.0.*
      ProxyJump jump
      User alice
  ```
  ProxyJump connects through the jump host by TCP forwarding, so agent forwarding is not needed
  (the ssh_config man page advises enabling agent forwarding with caution).
- Two jump hosts in different sites; they live in the management zone with OOB reachability.

## Verify
- [ ] Every critical device reachable on its console from the console server over LTE with the primary WAN down.
- [ ] Device VTY ACLs permit only jump hosts; direct SSH from a user subnet fails.
- [ ] Jump host sessions are logged with user identity.

## Checked

2026-10-28: Confirmed in the ssh_config man page: ProxyJump connects to the target by first making an ssh connection to the jump host and then forwarding TCP to the target, and agent forwarding should be enabled with caution. Removed: the Opengear docs source (no content returned), rollover/auto-sensing pinout claims, the 9600 8N1 and 115200 defaults, the ssh admin:port5 syntax, the exec-timeout command and vendor names.
Method: documentation only; no commands were run.
