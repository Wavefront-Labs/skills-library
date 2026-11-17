---
id: computing-software.systems-network-administration.linux.oscap-compliance-reports
name: oscap-compliance-reports
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, openscap, oscap-report, compliance-report, arf, xccdf-results, html-report, fleet-compliance, evidence, audit, security, sysadmin]
level: practitioner
status: docs-checked
description: "Produce compliance evidence from OpenSCAP: ARF vs XCCDF results, HTML reports and guides, extracting pass/fail counts and scores, fleet roll-ups, and archiving reports auditors accept."
sources:
  - https://github.com/OpenSCAP/openscap/blob/main/docs/manual/manual.adoc
  - https://github.com/OpenSCAP/openscap/blob/main/utils/oscap.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSCAP compliance reports

**Goal:** turn scans into evidence: a human-readable report per host, a machine-readable
result for trending, and a fleet summary showing who is out of compliance.

## 1. Produce the right artefacts in one run
```bash
DS=/usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
H=$(hostname -s); D=$(date +%F)
oscap xccdf eval --profile cis_server_l1 \
  --results-arf /var/lib/compliance/$H-$D-arf.xml \
  --report      /var/lib/compliance/$H-$D.html \
  $DS
```
- **ARF** (Asset Reporting Format, the SCAP result data stream): the format the oscap man page recommends over `--results` when scanning data streams.
- `--results` writes XCCDF results only.
- HTML report: score, per-rule results with rationale and remediation information (a report can also be generated during the scan with `--report`).

## 2. Regenerate or extract later
```bash
oscap xccdf generate report $H-$D-arf.xml > report.html
oscap xccdf generate guide --profile cis_server_l1 $DS > policy-guide.html     # the policy itself, no results
# counts
python3 - "$H-$D-arf.xml" <<'EOF'
import sys, collections, xml.etree.ElementTree as ET
ns={'x':'http://checklists.nist.gov/xccdf/1.2'}
r=ET.parse(sys.argv[1]).getroot()
print(collections.Counter(e.findtext('x:result',namespaces=ns) for e in r.iter('{%s}rule-result'%ns['x'])))
s=next(r.iter('{%s}score'%ns['x'])); print('score', s.text, 'max', s.get('maximum'))
EOF
```

## 3. Fleet roll-up
- Small fleets: collect ARF/XCCDF files centrally (Ansible `fetch` after scanning), parse counts per host into CSV, chart failures by rule to find systemic gaps.
- Track per-rule trends — the same rule failing on 80 % of hosts means fix the image/automation, not hosts.

## 4. What auditors want
Report per host with date, content name + version (from `oscap info $DS`),
profile ID, tailoring file (and the reason for each unselected rule), plus the remediation
record for each previous failure. Store read-only (object storage with retention lock or signed tarballs).

## Gotchas
- Archive the ARF and regenerate HTML on demand (`oscap xccdf generate report`) rather than storing every HTML report.
- Quote both the XCCDF score from the results and the per-result counts; do not treat the score as a plain pass percentage.
- Results from different content versions aren't comparable rule-for-rule; note version changes in trend charts.

## Verify
- [ ] Each scanned host has an ARF and HTML report for the period, with profile and content version recorded.
- [ ] The fleet summary's fail counts match a spot-check of individual reports.

## Checked

Checked 2026-10-26 against OpenSCAP/openscap (last commit 2026-10-22): docs/manual/manual.adoc (ARF results, report and guide generation, oscap info on ARF) and utils/oscap.8 (--results-arf recommendation for data streams). Confirmed: oscap xccdf eval --results-arf and --report, oscap xccdf generate report from ARF, generate guide --profile. Removed: the Satellite/Foreman and Insights claims, the 5-20 MB report size, the Satellite import claim and the oscap info grep, none of which appear in the OpenSCAP documentation.

Method: documentation only; no commands were run.
