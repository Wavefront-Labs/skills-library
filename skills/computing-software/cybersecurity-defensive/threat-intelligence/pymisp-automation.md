---
id: computing-software.cybersecurity-defensive.threat-intelligence.pymisp-automation
name: pymisp-automation
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [misp, pymisp, misp-api, ioc-automation, misp-objects, to-ids, threat-intel-platform]
level: practitioner
status: draft
description: "Automate MISP with PyMISP: create events with attributes and objects, set to_ids and tags correctly, search and export IOCs for controls, sightings, and API key hygiene."
sources: ["https://pymisp.readthedocs.io/en/latest/", "https://www.circl.lu/doc/misp/automation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PyMISP automation

## Connect
```python
from pymisp import PyMISP, MISPEvent, MISPObject
misp = PyMISP("https://misp.example.org", key=os.environ["MISP_KEY"], ssl=True)
```
Use a dedicated automation user per integration with the least role (e.g. "User" for creating events in
your org, "Read Only" for exporters); keys in a secret store.

## Create an event
```python
ev = MISPEvent()
ev.info = "Phishing campaign targeting finance - 2026-10-18"
ev.distribution = 0          # set deliberately; see the distribution options in your MISP
ev.threat_level_id = 2       # 1 high .. 4 undefined
ev.analysis = 1
ev.add_tag("tlp:amber")
ev.add_tag('misp-galaxy:mitre-attack-pattern="Phishing - T1566"')
ev.add_attribute("domain", "invoice-portal.example", to_ids=True, comment="credential phishing landing")
ev.add_attribute("ip-dst", "203.0.113.50", to_ids=True)
ev.add_attribute("email-subject", "Overdue invoice", to_ids=False)   # context, not for blocking
obj = MISPObject("file")
obj.add_attribute("filename", value="invoice.html")
obj.add_attribute("sha256", value="9f86d08...", to_ids=True)
ev.add_object(obj)
created = misp.add_event(ev, pythonify=True)
misp.publish(created)        # triggers sync/feeds to consumers
```
- `to_ids=True` means "safe to use for detection/blocking"; set False for context (victim names, generic
  strings, shared hosting IPs).
- Objects group related attributes (file, url, domain-ip, email) for better correlation and STIX export.

## Search and export for controls
```python
attrs = misp.search(controller="attributes", type_attribute=["ip-dst","domain"], to_ids=True,
                    tags=["tlp:clear","tlp:green","tlp:amber"], publish_timestamp="30d", enforce_warninglist=True,
                    pythonify=True)
```
`enforce_warninglist=True` drops values on warninglists (cloud ranges, top domains). Other outputs:
`return_format="csv" | "suricata" | "text"` (restSearch returnFormat also allows json, snort, rpz, yara, xml and others). Feed consumers (firewall EDLs, DNS RPZ) can pull
`/attributes/restSearch` directly with the same filters.

## Sightings
Report when an indicator is seen (or is a false positive) so analysts and confidence scoring benefit:
`misp.add_sighting({"value": "203.0.113.50", "type": "0"})` (type 1 = false positive, 2 = expiration).

## Gotchas
- Publishing sends emails/sync to all connected instances per distribution: check distribution before publishing.
- Large searches without `limit`/`page` time out; paginate.
- Event-level vs attribute-level tags both apply; TLP tag missing = unclear sharing rules.

## Verify
Create a test event in a test org with distribution 0, search it back via restSearch with your exporter
filters, then delete it; confirm warninglisted values are excluded from the export.

## Checked
2026-10-28. Partial; status stays draft. Confirmed in the MISP automation guide: restSearch filters (`publish_timestamp`, `to_ids`, `enforceWarninglist`, `limit`, `page`, `tags`), returnFormat values, threat level ids (1 high to 4 undefined), sighting types (0 sighting, 1 false-positive, 2 expiration). Fixed: removed `stix2` (not a returnFormat), replaced deprecated `last` with `publish_timestamp`, removed unconfirmed distribution and analysis value lists. Not confirmed: PyMISP method names and kwarg spellings (API reference not fetched).
Method: documentation only; no commands were run.
