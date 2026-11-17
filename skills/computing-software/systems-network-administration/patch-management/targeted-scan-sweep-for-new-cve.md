---
id: computing-software.systems-network-administration.patch-management.targeted-scan-sweep-for-new-cve
name: targeted-scan-sweep-for-new-cve
category: computing-software
field: systems-network-administration
product: patch-management
tags: [targeted-scan, nuclei, nmap, vulnerability-scanning, emergency-patching, patch-management]
level: practitioner
status: draft
description: "Run a targeted scan sweep for one new CVE: pick the right check (scanner plugin, Nuclei template, nmap NSE, version query), scope internet and internal ranges and track results."
sources:
  - https://github.com/projectdiscovery/nuclei-templates
  - https://nmap.org/book/nse-usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeted scan sweep for a new CVE

A full scan takes days; for an emergency you want one check across every relevant address within hours.

## Choose the check
1. **Commercial scanner plugin** for the CVE (Tenable plugin ID, Qualys QID): create a scan policy with only that plugin family/ID; credentialed if local check.
2. **Nuclei template** (`nuclei-templates/http/cves/2026/CVE-2026-XXXX.yaml`) for web-exposed flaws.
3. **nmap service/version detection + NSE** where a script exists.
4. **Inventory query** for local-only flaws (agent-based scanners, EDR software inventory, `Get-Package`, `rpm -q`).

## Run
```sh
# discover the service first, then check
nmap -p 443,8443 --open -sV -oG - 10.0.0.0/16 | awk '/open/{print $2}' > targets.txt
nuclei -l targets.txt -id CVE-2026-XXXX -rl 50 -o hits.txt -jsonl
nmap -p 445 --script smb-vuln-ms17-010 -iL targets.txt -oX ms17.xml
```
Tenable: Advanced Scan > Plugins: disable all, enable only the plugin ID and its dependencies (service detection).

## Scope
- External: all public IP ranges and domains (from ASM tool, DNS, cloud accounts), including forgotten ones.
- Internal: all subnets including DMZ, VPN, lab, OT (with OT-safe settings or passive only).
- Cloud: run from inside each VPC/vNet or use agent results.

## Track
Feed hits into the remediation tracker with asset owner; rescan the hit list after each patch wave until zero.

## Gotchas
- Early Nuclei templates and NSE scripts for fresh CVEs can be unsafe (trigger crashes) or wrong; read the template before running, test on one host.
- Version-only checks overcount backported fixes.
- Rate-limit; IPS may block the scanner and you get false "clean".

## Verify
Scan coverage (addresses scanned vs in scope) recorded, hit list goes to zero on rescan, and scan configs saved for reuse.
