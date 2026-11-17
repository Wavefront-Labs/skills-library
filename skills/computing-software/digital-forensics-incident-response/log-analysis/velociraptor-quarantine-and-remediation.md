---
id: computing-software.digital-forensics-incident-response.log-analysis.velociraptor-quarantine-and-remediation
name: velociraptor-quarantine-and-remediation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-quarantine, velociraptor, host-isolation, remediation, containment, dfir]
level: practitioner
status: draft
description: "Quarantine hosts and run remediation with Velociraptor: Windows/Linux quarantine artifacts, allow-listing the server, unquarantine, and remediation artifacts with full logging."
sources: ["https://docs.velociraptor.app/artifact_references/pages/windows.remediation.quarantine/", "https://docs.velociraptor.app/artifact_references/pages/linux.remediation.quarantine/", "https://docs.velociraptor.app/docs/", "https://docs.velociraptor.app/artifact_references/pages/windows.remediation.scheduledtasks/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Velociraptor quarantine and remediation

Velociraptor can isolate a host from the network while keeping its own connection to the server, then run remediation steps, which is useful where there is no EDR with isolation, or as a second path when EDR is tampered with.

## Quarantine
- **Windows**: `Windows.Remediation.Quarantine` applies an IPsec policy that blocks all traffic except to the Velociraptor server (resolved from the client config) and any additional allowed entries (e.g. DNS server, a forensic share) passed as parameters. A message box can notify the user (configurable).
- **Linux**: `Linux.Remediation.Quarantine` uses nftables rules to the same effect.
- In the GUI, a client's toolbar has a quarantine button that runs the artifact; the client gets a `Quarantine` label, and you can search for quarantined hosts by label.
- **Unquarantine**: run the artifact again with the remove-policy option (`RemovePolicy`) or use the GUI unquarantine button. Confirm the label is gone and connectivity restored.

## Before you quarantine
1. Authority per the IR delegation table; tell the service owner.
2. Capture volatile data first if the host matters (memory via `Windows.Memory.Acquisition`, network connections via `Windows.Network.Netstat`); isolation changes network state.
3. Add DNS or proxy exceptions if the server is addressed by name and resolution is needed; test on a lab host.
4. Remember the policy survives reboot only if the artifact is designed so; verify on your version.

## Remediation artifacts
Examples in the built-in library (names vary by version): `Windows.Remediation.ScheduledTasks` (remove tasks matching a regex), `Windows.Remediation.Sinkhole` (hosts-file sinkhole), service/process kill via VQL `execve()` in a custom artifact, file deletion with `rm()` in a custom artifact. Many have a `ReallyDoIt` parameter: the first run reports what would change; rerun with it set to act.

Write remediation as custom artifacts so steps are reviewed, parameterised, and every execution is logged in the flow with results.

## Hunts for fleet-wide action
Run remediation as a hunt targeted by label (e.g. hosts tagged `Compromised`), not all clients; monitor per-client results and failures.

## Gotchas
- Quarantining the host that runs a critical service takes the service down; coordinate.
- If the client config uses multiple server URLs or a frontend behind a load balancer, include all addresses in the allow list or the client drops offline.
- IPsec policy conflicts with existing GPO-managed IPsec on some estates; test.

## Verify
After quarantine, the client still checks in and a connection test to another internal host fails; after remediation, a follow-up collection shows the targeted artefacts gone.
