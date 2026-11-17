---
id: computing-software.cybersecurity-defensive.splunk.es-content-update-management
name: es-content-update-management
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-enterprise-security, es-content-update, escu, content-management, correlation-searches, analytic-stories, detection-engineering]
level: advanced
status: draft
description: "Manage Splunk ES detection content: install and update ESCU, enable analytic stories selectively, clone before tuning, and track what is actually running."
sources: ["https://docs.splunk.com/Documentation/ES/latest/Admin/Usecasecontent", "https://research.splunk.com/", "https://splunkbase.splunk.com/app/3449"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ES content management and ESCU

**Goal:** use Splunk's shipped detections (ES Content Update, ESCU) without enabling
hundreds of noisy searches or losing your tuning on the next update.

## 1. Install and update
- ESCU is a Splunkbase app (DA-ESS-ContentUpdate). In ES 7 it updates through
  Configure > Content > Content Management or the content library; otherwise install the
  new version on the search head (SHC: via the deployer).
- Read the release notes; new versions add, change and deprecate detections.
- Content is browsable at research.splunk.com with data requirements and ATT&CK mapping.

## 2. Enable selectively
1. List detections whose data you actually have: each has required data models and
   sourcetypes. Check with `| tstats count from datamodel=Endpoint.Processes by sourcetype`.
2. Enable by analytic story aligned to threats in your threat profile (ransomware, credential
   dumping, cloud account takeover), not "enable all".
3. Many ESCU searches are written for risk-based alerting (they write risk events, not
   notables). Plan whether you run RBA; if not, convert the key ones to notables.

## 3. Tune without losing changes
- Never edit the shipped search in place: updates overwrite it. **Clone** into your own app
  (e.g. `SA-org-detections`), disable the original, and tune the clone.
- Better: use the macro hooks. Most ESCU searches end with a `<name>_filter` macro that is
  empty by default; put allowlists there. Updates leave filter macros alone.
- Keep your tuned content in version control (detection-as-code) and deploy it as an app.

## 4. Track what runs
```
| rest /servicesNS/-/-/saved/searches splunk_server=local
| search action.correlationsearch.enabled=1 disabled=0
| table title eai:acl.app cron_schedule action.notable action.risk
```
Review monthly: searches with zero results for 90 days may be blind (data missing) or
irrelevant; searches with high volume and low true-positive rate need tuning.

## Gotchas
- Enabling many searches on the same cron minute overloads the scheduler; stagger schedules
  and watch skipped searches in the Monitoring Console.
- Detections depend on accelerated data models; if acceleration is behind, they miss events.

## Verify
Run Atomic Red Team or Splunk Attack Range tests for an enabled story and confirm the
expected notable or risk event appears.
