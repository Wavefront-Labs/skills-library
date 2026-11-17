---
id: computing-software.digital-forensics-incident-response.incident-response-process.building-a-forensic-analysis-workstation
name: building-a-forensic-analysis-workstation
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [forensic-workstation, sift-workstation, ir-preparation, remnux, eric-zimmerman-tools, dfir]
level: practitioner
status: docs-checked
description: "Build a forensic analysis workstation: SIFT on Ubuntu via Cast or the VM appliance, a Windows VM with Eric Zimmerman tools, evidence layout, isolation and tool validation."
sources: ["https://www.sans.org/tools/sift-workstation", "https://ericzimmerman.github.io/", "https://github.com/teamdfir/sift-cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a forensic analysis workstation

**Goal:** a repeatable analysis environment that can mount evidence read-only, run the
standard toolchain, and is never contaminated by or connected to the case network.

## Linux side: SIFT
The SANS SIFT page offers three routes. It is an open source, free project.
- **VM appliance:** download the SIFT Workstation OVA from the SANS portal.
- **Native Ubuntu:** the page calls for Ubuntu 22.04 (its feature list still says 20.04 LTS base),
  install the Cast binary, then `sudo cast install teamdfir/sift`.
- **Windows host:** install WSL with Ubuntu 22.04, then
  `sudo cast install --mode=server teamdfir/sift-saltstack`.

The older `sift-cli` installer (`sift install`, modes `desktop` (default), `server`) is archived
and read-only since 2023 and its README says it is replaced by Cast; do not build new
workstations on it. The SIFT page lists Plaso/log2timeline, Rekall, Volatility, bulk_extractor,
ClamAV, dc3dd, The Sleuth Kit, RegRipper and libewf among hundreds of tools.

## Windows side: analysis VM
- Keep the VM off the case network and not joined to a domain (practice).
- Get the Eric Zimmerman tools with `Get-ZimmermanTools.ps1`, which discovers and updates the
  whole set: MFTECmd ($MFT, $J and similar), PECmd (Prefetch), EvtxECmd (event logs), RECmd and
  Registry Explorer, Timeline Explorer, LECmd (LNK), JLECmd (Jump Lists), SBECmd (ShellBags),
  AmcacheParser. Use `-Dest` to pick the folder. `-NetVersion` selects the build: 4 (.NET 4.7.2),
  10 (.NET 10, the default and recommended) or 0 (all). .NET 10 builds need the .NET 10 runtime
  (Desktop runtime for GUI tools).
- Run malware analysis in separate VMs from case analysis; never mix live malware with case work.

## Layout and hygiene (practice, not from the cited pages)
```
/cases/<case-id>/evidence   (read-only, original images + hashes)
/cases/<case-id>/export     (tool outputs)
/cases/<case-id>/notes
```
- Mount evidence read-only. Snapshot the clean VM; revert between unrelated cases.
- Record tool versions per case for the report.

## Validation
Run new tool versions against a reference image and compare output with the previous version
before using them on casework.

## Verify
Rebuild from scratch using your notes on a spare machine; anything missing goes into the
build script.

## Checked
Date: 2026-11-08. Confirmed on the SANS SIFT page (install routes, Ubuntu 22.04 and Cast commands,
included tools, free and open source), the sift-cli README (archived, replaced by Cast, modes) and the
Eric Zimmerman page (tool list, Get-ZimmermanTools.ps1, -Dest, -NetVersion, .NET requirements).
Removed: the snap install and sift-cli download line, hardware sizing, Defender and KAPE and
Autopsy and Hayabusa and Chainsaw lists, REMnux and FLARE-VM naming, NIST CFReDS and mount
flags (marked as practice where kept).
Method: documentation only; no commands were run.
