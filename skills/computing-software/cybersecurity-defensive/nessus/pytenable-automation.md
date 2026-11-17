---
id: computing-software.cybersecurity-defensive.nessus.pytenable-automation
name: pytenable-automation
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-reporting, pytenable, tenable-api, api-keys, tenable-vulnerability-management, tenable-sc, export-api, automation]
level: practitioner
status: docs-checked
description: "Automate Tenable scanning and data exports with pyTenable: API keys, launching scans, bulk vulnerability exports and pushing results to ticketing or a SIEM."
sources: ["https://pytenable.readthedocs.io/en/stable/", "https://pytenable.readthedocs.io/en/stable/api/io/exports.html", "https://pytenable.readthedocs.io/en/stable/api/io/scans.html", "https://pytenable.readthedocs.io/en/stable/api/sc/index.html", "https://pytenable.readthedocs.io/en/stable/api/sc/analysis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automation with pyTenable

**Goal:** stop exporting by hand; pull vulnerability data and drive scans from code with Tenable's Python library.

## Setup
```
pip install pytenable
```
pyTenable is described in its docs as a pythonic interface to the Tenable application APIs, with a common structure across products. Use API keys for a dedicated service user with the least privilege that works, read from environment variables or a secrets manager, never from source.

## Tenable Vulnerability Management
```python
import os, time
from tenable.io import TenableIO
tio = TenableIO(access_key=os.environ["TIO_ACCESS_KEY"], secret_key=os.environ["TIO_SECRET_KEY"])

# bulk vulnerability export; the call returns an iterator over exported chunks
week_ago = int(time.time()) - 7 * 86400
for finding in tio.exports.vulns(severity=["high", "critical"],
                                 state=["open", "reopened"],
                                 last_found=week_ago):
    handle(finding)          # your code

tio.scans.launch(scan_id)                        # launch a scan
tio.scans.launch(scan_id, targets=["127.0.0.1"]) # or override targets
```
`vulns()` filters documented in pyTenable include `severity`, `state`, `first_found`, `last_found`, `last_fixed` (applies to fixed data only) and `since` (cannot be combined with `last_found`, `first_found` or `last_fixed`); `num_assets` sets how many assets' findings go in each chunk (default 500). `tio.exports.assets()` exports assets (default `chunk_size` 1000). Pass `iterator=None` to get the export UUID instead of an iterator, and `tio.exports.download_chunk(...)` downloads one chunk (3 retries by default).

## Tenable Security Center
```python
from tenable.sc import TenableSC
sc = TenableSC(url="https://sc.example.internal",
               access_key=os.environ["SC_ACCESS_KEY"], secret_key=os.environ["SC_SECRET_KEY"])
for vuln in sc.analysis.vulns():
    handle(vuln)
```
`sc.analysis.vulns()` takes filter tuples such as `('exploitAvailable', '=', 'true')` and a `tool` argument (the default is `vulndetails`; `sumip` returns an IP summary).

## Patterns
- Run a recurring export with a time window (`last_found` or `since`) and upsert into your own store, rather than re-exporting everything.
- Close tickets on the finding state, not on the host being absent from a scan.

## Gotchas
- API keys carry the permissions of the user that created them; treat an admin key as a high-value secret.
- Check the pyTenable release notes when upgrading: some methods are deprecated (for example `initiate_export` since 1.9.0) and the `host` parameter of `TenableSC` is being replaced by `url`.

## Verify
- [ ] The script runs unattended with a least-privilege key and logs counts per run.
- [ ] Counts for the same filter match the platform for the same time window.

## Checked
2026-11-02. Confirmed from the pyTenable documentation (home page, `tenable.io` exports and scans, `tenable.sc` index and analysis). Removed (not stated there): the UI path for creating API keys, `v["asset"]["hostname"]`-style finding field names, `TioExportsError`, HTTP 429 and automatic-retry claims, the standalone Nessus API section, the `("severity", "=", "3,4")` filter example, and ticketing advice about owners per plugin.

Method: documentation only; no commands were run.
