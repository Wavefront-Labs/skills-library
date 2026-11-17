---
id: computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody
name: forensic-acquisition-and-chain-of-custody
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [evidence-handling, chain-of-custody, order-of-volatility, rfc-3227, forensic-acquisition, imaging, write-blocker, hashing, sha256, md5, e01, ewfacquire, ftk-imager, dc3dd, dd, winpmem, avml, lime, memory-acquisition, cloud-snapshot, evidence-integrity, documentation, iso-27037, dfir]
level: practitioner
status: draft
description: "Acquire digital evidence soundly: order of volatility, memory then disk, write-blocking, E01/raw imaging with hashes, cloud snapshots, and a chain-of-custody record that holds up."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://www.iso.org/standard/44381.html", "https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forensic acquisition and chain of custody

**Goal:** collect evidence in an order and manner that preserves the most information,
proves it hasn't changed since collection, and documents every hand-off — so findings
survive scrutiny from a court, regulator, insurer or opposing expert.

Legal note: rules of evidence differ by jurisdiction. If litigation or law enforcement
is likely, involve counsel before collecting and follow their direction.

## Order of volatility (RFC 3227)
Collect the most short-lived first:
1. CPU registers/cache (practically: skip) → **RAM**, running processes, network
   connections, logged-on users
2. Temporary filesystems, swap/pagefile
3. **Disk**
4. Remote logs and monitoring data (SIEM, firewall, cloud audit logs — check retention *now*)
5. Physical configuration, topology; archival media/backups

**Don't power off a running suspect machine** by reflex: you lose memory, and with full-disk
encryption you may lose access to the disk entirely. Isolate it from the network
instead (pull the cable/EDR isolation, keep power).

## Memory
- Windows: WinPmem (`winpmem_mini_x64.exe memory.raw`), Magnet RAM Capture, or your EDR's
  memory collection. Linux: AVML (`avml memory.lime`) or LiME (kernel module, must match
  the kernel). Write output to **external media or a network share**, never the
  suspect's own disk.
- Run from your own trusted tools on removable media; note that any tool you run changes
  memory slightly — record exactly what you ran and when.
- Hash the output immediately.

## Disk
- Physical drive removed: attach through a **hardware write-blocker** (tested,
  documented model), then image.
- Linux CLI:
  ```bash
  ewfacquire /dev/sdX            # interactive: case number, examiner, evidence number, E01 output, MD5/SHA
  dc3dd if=/dev/sdX of=disk.raw hash=sha256 log=acq.log
  ```
  FTK Imager (Windows) does the same with a GUI: create image › physical drive › E01,
  fill in case details, verify after create.
- **E01** stores metadata and embedded hashes and compresses; **raw** is universal.
  Either is fine — be consistent and record which.
- Live/logical imaging (encrypted volumes that are mounted, servers that can't go
  down) is acceptable when justified; write down the justification.
- Make a **working copy** and verify its hash matches; analysts never touch the master.

## Cloud
- Take a provider snapshot of disks (e.g. AWS EBS snapshot, Azure managed-disk
  snapshot) and tag it with the case number; copy to an isolated forensic account.
- Export audit logs (CloudTrail, Azure Activity/Entra sign-in, Google Workspace) before
  they age out — default retention can be as short as 90 days or less.
- Record instance metadata (IDs, IPs, attached roles) at collection time.

## Hashing and integrity
- SHA-256 as primary; many labs also record MD5 because older tools and some courts
  expect it. Hash at acquisition, on every copy, and before analysis.
- A mismatch is not the end of the world if explained (e.g. a failing drive with bad
  sectors gives different reads — the imager logs them); an *unexplained* mismatch is.

## Chain of custody record (one per item)
Minimum fields:
- Item number, description, make/model/serial, where and from whom collected
- Date/time (UTC) and collector's name
- Acquisition method/tool and version, hashes
- Every transfer: from, to, date/time, purpose, signature
- Storage location (sealed evidence bag number, locked storage, access-controlled share)
Photograph the device and its connections in place before unplugging anything.

## Gotchas
- Imaging a drive while booted from it alters it; boot a forensic live OS or remove the drive.
- SSDs: TRIM and wear levelling keep changing data even behind a write-blocker if
  powered; image promptly and note it.
- Investigators logging in to the suspect machine "to have a look" create artefacts that
  contaminate the timeline. Record any such access.

## Verify
- [ ] Collection followed order of volatility, or the deviation is written down.
- [ ] Every item has hashes at acquisition and a matching hash on the working copy.
- [ ] Tool names, versions and commands recorded.
- [ ] Chain-of-custody form complete with every hand-off.
- [ ] Master copies stored read-only with restricted access.
