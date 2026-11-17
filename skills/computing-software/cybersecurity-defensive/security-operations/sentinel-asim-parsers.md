---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-asim-parsers
name: sentinel-asim-parsers
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, asim, normalization, kql, unifying-parsers, imauthentication, imnetworksession, parser-development]
level: advanced
status: docs-checked
description: "Use and extend Microsoft Sentinel ASIM: unifying vs source parsers, parameterised filtering for performance, writing a custom source parser, and testing schema compliance."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/normalization", "https://learn.microsoft.com/en-us/azure/sentinel/normalization-develop-parsers", "https://learn.microsoft.com/en-us/azure/sentinel/normalization-parsers-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASIM normalisation parsers in Sentinel

ASIM (Advanced Security Information Model) lets one rule query many sources through a common
schema (Authentication, NetworkSession, DnsActivity, ProcessEvent, FileEvent, WebSession,
AuditEvent, RegistryEvent, UserManagement, DhcpEvent).

## Using parsers
```
_Im_Authentication(starttime=ago(1h), endtime=now(), eventresult='Failure')
| summarize Failures=count() by SrcIpAddr, TargetUsername
| where Failures > 20
```
- `_Im_<Schema>` = built-in unifying parser (deployed in every workspace).
- `im<Schema>` = workspace-deployed unifying parser that also includes your custom parsers.
- Individual source parsers exist per schema and source (see the ASIM parsers list for the names).
- **Pass filter parameters** (`starttime`, `srcipaddr_has_any_prefix`, `eventtype` etc.) instead of
  `where` after the call: parameters are pushed into every source parser before parsing, which is
  far cheaper.
- `pack=true` keeps unparsed fields in `AdditionalFields`.

## Writing a source parser
1. Start from a similar parser in the Azure-Sentinel GitHub repo (`Parsers/ASim<Schema>`).
2. Filtering version (`vim...`) with the schema's standard parameters, and a no-filter wrapper.
3. Map mandatory fields: `EventCount`, `EventStartTime`, `EventEndTime`, `EventType`,
   `EventResult`, `EventProduct`, `EventVendor`, `EventSchema`, `EventSchemaVersion`, `Dvc`,
   plus schema-specific ones (`TargetUsername`, `SrcIpAddr`...). Use the schema's allowed values
   (EventResult is one of Success, Partial, Failure, NA).
4. Save as a workspace function (or deploy via ARM template from the repo format).
5. Add it to the workspace unifying parser `im<Schema>` (edit the union list) so content picks it up.

## Testing
- ASIM schema tester and data tester (in the repo, `ASimSchemaTester`/`ASimDataTester` functions):
  ```
  vimAuthenticationMyApp | getschema | invoke ASimSchemaTester('Authentication')
  vimAuthenticationMyApp | invoke ASimDataTester('Authentication')
  ```
  Fix every "mandatory missing" and "invalid value" line.

## Gotchas
- Built-in `_Im_` parsers update automatically; editing them is not possible. Customise through
  `im` workspace parsers.
- Filtering after the parser call scans and parses everything first: slow and costly on big tables.
- Disable source parsers for sources you do not ingest to cut query time (see the ASIM documentation for how).

## Checked
2026-10-28. Confirmed in the ASIM parser development and schema pages: `_Im_<schema>` unifying parser naming, the `pack` parameter that puts extra data in `AdditionalFields`, EventResult allowed values, the `ASimSchemaTester` invoke pattern. Removed: the `_ASim_`/`vim` name pattern and the `ASimDisabledParsers` watchlist name.
Method: documentation only; no commands were run.

## Verify
Run an ASIM-based analytics rule query for 24h and confirm events from your custom source appear
with populated mandatory fields.
