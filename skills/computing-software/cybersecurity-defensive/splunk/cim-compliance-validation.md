---
id: computing-software.cybersecurity-defensive.splunk.cim-compliance-validation
name: cim-compliance-validation
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, cim-validation, cim, common-information-model, data-models, eventtypes, field-aliases, enterprise-security, data-onboarding]
level: practitioner
status: draft
description: "Validate that a new Splunk sourcetype is CIM-compliant using the CIM Validation (S.o.S.) datamodel audit, datamodel searches and required-field checks before ES uses it."
sources: ["https://docs.splunk.com/Documentation/CIM/latest/User/UsetheCIMtonormalizedataatsearchtime", "https://docs.splunk.com/Documentation/CIM/latest/User/UsetheCIMFiltersearch", "https://lantern.splunk.com/Splunk_Platform/Product_Tips/Data_Management/Validating_CIM_compliance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CIM compliance validation of a new sourcetype

Goal: prove a sourcetype populates the right data model with the fields ES correlation searches use,
before anyone relies on it.

## 1. Is it in the data model at all?
Data models select events by tag. Check tags first:
```
index=<idx> sourcetype=<st> | head 1000 | stats count by eventtype tag
```
Empty `tag` means eventtypes.conf/tags.conf in the TA are missing or the search head lacks the TA.
Then confirm the constraint matches:
```
| datamodel Authentication Authentication search | search sourcetype=<st> | head 10
```

## 2. Are required fields populated?
For each dataset, list the fields ES content needs (CIM manual, "fields for <model>" tables):
```
| datamodel Network_Traffic All_Traffic search | search sourcetype=<st>
| fieldsummary | search field IN ("All_Traffic.src","All_Traffic.dest","All_Traffic.dest_port","All_Traffic.action","All_Traffic.transport")
| table field count distinct_count values
```
- Values must match CIM's expected vocabulary: `action` in allowed/blocked/teardown for traffic,
  success/failure for Authentication. `Failed` or `DENY` breaks correlation searches.
- `unknown` is acceptable only when the source genuinely lacks the field.

## 3. Use the tooling
- The CIM add-on's **CIM Validation (S.o.S.)** dashboard / `cim_validation` searches score each field.
- ES **Data Model Audit** and the "Datamodel fields coverage" in ES content tools show acceleration and
  field coverage. Splunk Security Essentials "Data Inventory" maps sources to products.
- Restrict CIM data model index constraints (CIM Setup page, `cim_<model>_indexes` macros) to
  the indexes that hold the data; otherwise acceleration scans every index.

## 4. Fix at the TA, never in the search
Use FIELDALIAS, EVAL (`EVAL-action = case(...)`), LOOKUP and eventtype/tag stanzas in a local TA
layer. Keep the vendor TA untouched so upgrades do not wipe fixes.

## Verify
After the model rebuilds: `| tstats summariesonly=t count from datamodel=<Model> where sourcetype=<st> by <Model>.action`
returns the expected action values, and a test ES correlation search fires on a known sample.
