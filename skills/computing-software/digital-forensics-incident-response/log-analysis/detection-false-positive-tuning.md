---
id: computing-software.digital-forensics-incident-response.log-analysis.detection-false-positive-tuning
name: detection-false-positive-tuning
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [detection-tuning, detection-engineering, sigma-rules, siem, dfir]
level: advanced
status: draft
description: "Tune noisy detections without blinding them: measure FP rate, scoped exclusions, allow-list hygiene, threshold and enrichment changes, and regression testing."
sources: ["https://github.com/SigmaHQ/sigma-specification", "https://github.com/palantir/alerting-detection-strategy-framework", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detection false-positive tuning

**Goal:** reduce alert noise so analysts trust the detection, while keeping it able to catch the
technique. Bad tuning (broad exclusions) is how real intrusions go unseen.

## Measure first
- Per rule over 30 days: alert count, true positives, benign true positives (real activity, authorised),
  false positives (logic wrong), time to triage. Track in the detection repository or SOAR.

## Tuning options, best to worst
1. **Fix the logic** (FP = rule matches things that are not the technique): tighten field conditions, use
   parent/child, command-line structure, or signature status rather than names.
2. **Enrich** instead of excluding: add asset role, user group, signer, prevalence so triage is instant and severity can vary.
3. **Scoped exclusion** for benign true positives: exclude the *specific* combination
   (host group + signed binary path + parent + account), never just a process name.
   ```yaml
   filter_backup_agent:
     Image|endswith: '\VendorBackup\agent.exe'
     ParentImage|endswith: '\services.exe'
     User: 'NT AUTHORITY\SYSTEM'
   condition: selection and not filter_backup_agent
   ```
4. **Thresholds/aggregation**: alert on rare combos (stacking) or counts over time.
5. **Lower severity / route to hunting queue** rather than disable.
Disabling a rule is a decision for the detection owner with a recorded reason.

## Hygiene
- Every exclusion has an owner, reason, ticket and review/expiry date.
- Avoid exclusions on user-writable paths, wildcards matching attacker-controllable names, or whole hosts (attackers live on those hosts too).

## Regression test
- Re-run the rule against the positive test cases (Atomic Red Team, recorded incident data) after each change.
- Re-check FP volume after a week.

## Gotchas
- Excluding "admin tools" excludes attackers using the same admin tools.
- Tuning by ignoring an entire log source field that went null after a parser change - check data quality first.

## Verify
Positive tests still fire, FP count dropped, and every exclusion is documented with an expiry.
