---
id: computing-software.cybersecurity-defensive.falco.rules-adoption-phases
name: rules-adoption-phases
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [rules-maturity, maturity-stable, rules-adoption, tuning, incubating]
level: intro
status: docs-checked
description: "Roll out Falco rules in phases using the Rules Maturity Framework: stable defaults first, tune, then incubating and custom rules."
sources:
  - https://falco.org/docs/concepts/rules/adoption-rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Falco Project's Rules Maturity Framework labels rules `maturity_stable`, `maturity_incubating` or `maturity_sandbox` to guide adoption.

Phases:
1. Newcomers start with the introductory default rules, tagged `maturity_stable`, based on syscall and container events, in the established `falco_rules.yaml`.
2. As you learn your environment, tune the default rules to your needs, which goes together with assessing performance overhead and adjusting.
3. Once the stable rules run consistently with low false positives and acceptable performance, add a next set of rules, which may be `maturity_incubating` or `maturity_sandbox`, offering more specific detections.
4. Alongside each phase, creating custom rules early often makes sense, for example for sensitive files unique to your environment or for crown-jewel services with known execution patterns (alert on deviations).
5. Explore the plugins system and plugin rules for sources beyond syscalls and containers.

Start by assessing the top cyber threats for your organization and begin with stable rules covering them. A maturity level does not predict noise, because every environment differs, particularly in cloud settings.

Operationalise with 24/7 detection triage by analysts and predefined runbooks in incident response. For each Falco release, set time aside to review new features, and revisit rules as your infrastructure changes.

Also test the pipeline end to end: Falco logging events, transport to the data lake or SIEM working, and triage and response in place. Stable rules target universal system-level threats aligned with Mitre Attack, such as remote code execution, container escapes, privilege escalation and credential theft.

Gotcha: incubating and sandbox rules usually need more engineering effort to evaluate and tune than stable ones, so add them only after the stable set is consistent.

## Checked

2026-11-08. Read the Adoption of Falco Rules page in full. Corrected phase 4 (custom rules alongside each phase), added end-to-end testing, replaced an unsupported gotcha.

Method: documentation only; no commands were run.
