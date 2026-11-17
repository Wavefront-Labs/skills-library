---
id: computing-software.systems-network-administration.patch-management.cpe-and-swid-software-identification
name: cpe-and-swid-software-identification
category: computing-software
field: systems-network-administration
product: patch-management
tags: [cpe, swid, software-identification, nvd, software-inventory, patch-management]
level: practitioner
status: docs-checked
description: "Match installed software to vulnerabilities with CPE 2.3 names and SWID tags: build CPEs from inventory, query the NVD CPE API, and handle vendor/product naming drift."
sources:
  - https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/cpe
  - https://nvd.nist.gov/developers/products
  - https://csrc.nist.gov/projects/Software-Identification-SWID
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPE and SWID identifiers for vulnerability matching

**Goal:** turn "Adobe Acrobat Reader DC 23.008" in an inventory into an identifier a CVE feed can match, so findings are not missed or double-counted.

## CPE 2.3 formatted string
```
cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other
cpe:2.3:a:adobe:acrobat_reader_dc:23.008.20470:*:*:*:continuous:*:*:*
```
- `part`: `a` application, `o` operating system, `h` hardware.
- `*` = ANY, `-` = NA (not applicable). Lowercase, spaces become `_`, special characters escaped with `\`.
- NVD CVE records carry `configurations` with `cpeMatch` entries using `versionStartIncluding`/`versionEndExcluding` ranges; you match your exact CPE against those ranges, not string equality.

## Look up the right CPE
```sh
curl -s "https://services.nvd.nist.gov/rest/json/cpes/2.0?keywordSearch=acrobat%20reader&resultsPerPage=20" \
  -H "apiKey: $NVD_API_KEY" | jq -r '.products[].cpe.cpeName'
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:a:7-zip:7-zip:23.01:*:*:*:*:*:*:*" | jq '.totalResults'
```
NVD publishes request rate limits (lower without an API key) on its API start-here page: read the current numbers there and cache the dictionary locally. Responses carry `products[].cpe` with `cpeName`, `cpeNameId` and `deprecated`; CVE responses carry `totalResults` and `configurations[].nodes[].cpeMatch[]` with `criteria` and `versionEndExcluding`.

## Build a mapping table
Keep a reviewed table `inventory DisplayName regex -> cpe vendor:product`, because Add/Remove Programs names never match NVD names directly ("Mozilla Firefox (x64 en-US)" -> `mozilla:firefox`). Normalise versions (strip build suffixes the vendor does not use in advisories).

## SWID tags (ISO/IEC 19770-2)
- XML tag files that installers add to an endpoint as part of installation; the standard (ISO/IEC 19770-2:2015) defines the tag lifecycle. Locations vary by product: check each vendor's documentation.
- Fields: `name`, `version`, `tagId`, `Entity` with `regid` (e.g. `regid.1991-06.com.microsoft`).
- More reliable than display names when present; coverage is patchy, so use as a preferred source and fall back to CPE mapping.

## Gotchas
- NVD CPE assignment lags new CVEs ; vendor advisories and OSV/purl data fill the gap for open source.
- Distro packages carry backported fixes: `openssl 1.1.1k-12.el8` is fixed even though upstream CPE ranges say vulnerable. Use distro OVAL/advisories for OS packages, CPE for third-party apps.
- Deprecated CPEs: the dictionary marks them with `deprecated: true`; map to the current entry rather than keeping both.

## Verify
Pick five known-vulnerable apps in inventory; confirm each maps to one CPE and returns the expected CVEs from the NVD API.

## Checked
Date: 2026-10-27. Documentation: NIST CPE page (CPE 2.3 current, CPE 3.0 not yet specified), NIST SWID page, NVD CPE and CVE API 2.0 responses read live. Confirmed: eleven-attribute CPE 2.3 string layout, the adobe acrobat_reader_dc example exists in the dictionary, endpoint names and field names (`cpeName`, `deprecated`, `cpeMatch`, `versionEndExcluding`), ISO/IEC 19770-2:2015 for SWID. Removed unconfirmed rate-limit numbers, SWID file paths and the deprecatedBy field name.
Method: documentation only; no commands were run.
