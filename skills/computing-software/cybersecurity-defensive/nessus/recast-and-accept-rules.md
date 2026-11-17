---
id: computing-software.cybersecurity-defensive.nessus.recast-and-accept-rules
name: recast-and-accept-rules
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-reporting, recast-rules, accept-risk, severity-modification, tenable-vulnerability-management, tenable-sc, risk-acceptance, audit-trail]
level: practitioner
status: docs-checked
description: "Use recast and accept rules in Nessus/Tenable to change severity or accept risk for specific findings, with scope, expiry and an audit trail."
sources: ["https://docs.tenable.com/nessus/Content/PluginRules.htm", "https://docs.tenable.com/nessus/Content/manage-vulnerabilities.htm", "https://docs.tenable.com/vulnerability-management/Content/recast/about-recast-rules.htm", "https://docs.tenable.com/vulnerability-management/Content/recast/about-accept-rules.htm", "https://docs.tenable.com/vulnerability-management/Content/recast/add-recast-rules.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recast and accept rules

**Goal:** reflect real risk in reports (a finding mitigated by a control, or a severity that is wrong in your context) without altering scan data and with a record of why.

## Rule types
| Platform | Rule | Effect (per Tenable docs) |
|---|---|---|
| Nessus | Plugin Rules | Change the severity of a plugin, or hide it, in scan results after a scan completes; scoped by host and plugin ID with an optional expiration date. Presentation only: the plugin still runs and generates traffic. Cannot be applied to PCI templates. |
| Tenable Vulnerability Management | Recast | Modifies the severity of all findings matching a criteria query; does not modify scan results; can expire, after which findings revert to original severity. |
| Tenable Vulnerability Management | Accept | Accepts the risk and hides matching findings from Explore > Findings; the record stays in the system; can expire, after which findings reappear. |
| Tenable Vulnerability Management | Change Result | Host audits only: changes the Original Result of audit findings (for example Failed to Passed). |
Tenable Security Center has its own accept-risk and recast-risk features; see the Security Center user guide.

## Example scenarios from Tenable
- Recast down: a Critical finding on a legacy server on an isolated network with no internet access, changed to Low.
- Accept: a vulnerability on a business-critical legacy application that cannot be patched without breaking it, with a documented sign-off for a fixed period such as six months.

## Writing a rule
- Nessus plugin rule example in the docs: host, plugin ID, expiration date and new severity.
- Tenable Vulnerability Management: Recast page > Add Rule; choose Accept or Recast, name it, describe it and build the criteria query (filters include IPv4 address, plugin ID, FQDN and tags). The query bar shows how many assets and findings currently match, so check the scope before saving.
- Set an expiry so the decision is revisited, and put the exception ticket in the description.

## Gotchas
- Raw `.nessus` exports from Nessus bypass plugin rules and keep original severities.
- In Tenable Vulnerability Management, rules are eventually consistent: new findings can appear before a rule is applied, and the Explore > Findings view can lag by up to 60 minutes after evaluation.
- VPR is never changed by recast or accept rules. Rules count against a shared limit of 25,000 per container.
- Recast changes the severity counts used in exposure scoring (Tenable One/Lumin licences); accept rules do not.

## Verify
- [ ] Every active rule has an owner, ticket reference and expiry.
- [ ] The affected-findings view for each rule matches the findings you intended.

## Checked
2026-11-02. Confirmed from Tenable Nessus 10.12 "Plugin Rules" and "Manage Vulnerabilities", and Tenable Vulnerability Management "About Recast Rules", "About Accept Rules" and "Add Recast, Change Result, and Accept Rules". Removed (not stated there): the recommended 90-180 day expiry, the Security Center row details, IP-versus-asset-UUID advice, plugin supersession advice, "when legitimate" policy rules presented as Tenable guidance, recasting info-to-critical dashboard advice, audit-log spot-check.

Method: documentation only; no commands were run.
