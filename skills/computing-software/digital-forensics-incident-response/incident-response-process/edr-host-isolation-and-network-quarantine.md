---
id: computing-software.digital-forensics-incident-response.incident-response-process.edr-host-isolation-and-network-quarantine
name: edr-host-isolation-and-network-quarantine
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [host-isolation, network-quarantine, edr, containment, defender-for-endpoint, dfir]
level: practitioner
status: docs-checked
description: "Isolate or contain a compromised host with Defender for Endpoint: full vs selective isolation, proxy and VPN traps, 7-day auto-release, device containment, and force-release."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EDR host isolation and network quarantine (Defender for Endpoint)

**Goal:** cut a compromised host off from the attacker and the network while the response team
keeps what it needs for collection. This skill covers Microsoft Defender for Endpoint only, per
its Learn page "Take response actions on a device".

## Choose the action
- **Isolate device** disconnects the device from the network but keeps its connectivity to the
  Defender for Endpoint service, which keeps monitoring it. Aim: stop attacker control, data
  exfiltration and lateral movement.
- **Selective isolation** (Windows 10 1709+ per the page, also Windows 11, Server 2012 R2+,
  Azure Stack HCI 23H2+, macOS) gives control over the isolation level; you can allow Outlook
  and Microsoft Teams, and define exclusions for processes and destinations.
- **Contain device** is for an unmanaged or possibly compromised device: all onboarded devices
  block incoming and outgoing communication with it (Windows 10 and Server 2019+ onboarded
  devices). Up to 100 contained devices at once is the recommendation. A newly contained
  device can take up to 5 minutes to propagate; if the device changes IP the block follows to
  the new IP.
- **Contain IP** blocks the IP of undiscovered or non-onboarded devices (done automatically by
  automatic attack disruption).
- **Contain user** is only applied automatically by attack disruption; it blocks attack-related
  protocols (network logons, RPC, SMB, RDP) on onboarded devices at the endpoint layer and does
  not disable the account in the identity provider. Undo needs the Global Administrator role.

## Traps documented on the page
- With web proxies (PAC, WPAD, static proxies) devices might not recover from isolation; use
  selective isolation.
- A device behind a full VPN tunnel cannot reach the Defender cloud service after isolation;
  the page recommends split tunnelling for Defender traffic.
- Isolating a Hyper-V server blocks traffic to all its child virtual machines.
- Isolation is automatically lifted after seven days. If the device is offline when you submit
  the action, Defender retries for up to three days, then you must reissue it.
- On Linux an isolated device is released if an admin modifies or adds an iptables rule;
  exclusions are not supported for macOS or Linux isolation.
- Requires at least the Active remediation actions role and access to the device by device group.
- Containing a router acting as default gateway can break connectivity; the portal warns.
- Automatic attack disruption can isolate end-user workstations itself; exclude business
  critical devices by tag, and temporarily exclude during breach-and-attack simulations.

## Before and during
- Collect an investigation package (Windows: autoruns, network connections, DNS cache, prefetch,
  processes, scheduled tasks, security event log, services, SMB sessions and more). Collection
  can fail on low battery or metered connections. Start a live response session for remote
  shell collection; it can be restricted on high-value assets.
- Record the comment, time and actor from the Action center for the timeline; it lists device
  isolation with submitter and success or failure.
- Release with **Release from isolation** (or **Release from containment**) when remediation is
  done.
- If an isolated device is unresponsive, Admins can download a per-device force-release script
  from the device page (valid three days; Windows only, specific KB levels listed on the page).

## Verify
Device page shows isolated status, the Action center entry succeeded (not failed or pending),
and the release time is recorded in the master timeline.

## Checked
Checked 2026-11-08 against the cited Microsoft Learn page. Removed because it is not on that
page: CrowdStrike, SentinelOne and Carbon Black commands, the API call body, reboot persistence,
switch, VLAN and cloud security-group quarantine, memory-capture advice, and the Test-NetConnection
check. The NIST SP 800-61r3 landing page was dropped as a source (no readable content used).
Method: docs-only read of cited pages, 2026-11-08
