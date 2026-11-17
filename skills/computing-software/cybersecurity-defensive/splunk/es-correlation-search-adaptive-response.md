---
id: computing-software.cybersecurity-defensive.splunk.es-correlation-search-adaptive-response
name: es-correlation-search-adaptive-response
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-enterprise-security, adaptive-response, correlation-searches, risk-modifier, notable-action, send-to-soar, detection-engineering]
level: practitioner
status: draft
description: "Build Splunk ES correlation searches with adaptive response actions: notable fields, risk analysis objects, drilldowns, SOAR send, and testing actions safely."
sources: ["https://docs.splunk.com/Documentation/ES/latest/Admin/Configurecorrelationsearches", "https://docs.splunk.com/Documentation/ES/latest/Admin/Setupadaptiveresponse", "https://docs.splunk.com/Documentation/ES/latest/Admin/Includedadaptiveresponseactions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Correlation searches with adaptive response

## Create
Content > Content Management > Create New Content > Correlation Search.
- App: your own app (not `SplunkEnterpriseSecuritySuite`) so upgrades do not overwrite it.
- Search: prefer tstats on CIM data models; output one row per entity with the fields the
  analyst needs (`src`, `dest`, `user`, `signature`, counts, first/last time).
- Schedule: real-time vs continuous; use continuous with a cron and a time range that overlaps
  the schedule slightly (`-65m` to `-5m` every hour) to absorb indexing lag.

## Adaptive response actions
- **Notable**: title with tokens (`Brute force from $src$ against $user$`), description, security
  domain, severity, drilldown search (`index=auth src=$src$ earliest=$info_min_time$`), next steps,
  recommended actions.
- **Risk Analysis**: risk object field (`user` or `src`), type (user/system/other), score, and
  in ES 7+ threat object fields. For RBA, use risk actions instead of notables on low-fidelity rules.
- **Send to SOAR / Run Playbook**: forwards the event to Splunk SOAR with the container label.
- **Webhook, Run Script, Stream capture, Ping**: built-ins; plus actions from add-ons (e.g. EDR isolate).
Actions run per result row.

## Field and token rules
- Tokens are `$field$` from the search output; a missing field renders as literal text.
- Keep `orig_*` fields if you rename, so drilldowns still work.
- Severity can be set dynamically with an output field named `severity`.

## Testing safely
1. Run the SPL ad hoc over the last 7 days; count expected rows.
2. Save disabled, then enable with only the Notable action.
3. Add automated actions (isolate, disable account) only after a period of review and with
   SOAR guardrails, not directly from the correlation search.
4. Ad hoc test: in Incident Review, run an adaptive response action manually on one notable.

## Monitoring actions
`index=cim_modactions` holds action results; filter `action_status=failure`.
`index=_internal sourcetype=scheduler savedsearch_name="<rule>"` shows run status and skips.

## Gotchas
- High-cardinality output (one row per event) floods notables; aggregate with stats first.
- Changing the rule name changes `source` on notables; suppressions and dashboards referencing
  the old name break.
- Throttling fields must exist in the output.

## Verify
The notable renders with populated title tokens, the drilldown returns events, and the risk
event appears in `index=risk` with the correct object.
