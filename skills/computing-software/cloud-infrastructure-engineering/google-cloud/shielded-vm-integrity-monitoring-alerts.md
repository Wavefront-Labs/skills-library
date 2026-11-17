---
id: computing-software.cloud-infrastructure-engineering.google-cloud.shielded-vm-integrity-monitoring-alerts
name: shielded-vm-integrity-monitoring-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shielded-confidential-vms, integrity-monitoring-alerts, late-boot-validation, measured-boot, log-based-alerts]
level: advanced
status: docs-checked
description: "Act on Shielded VM integrity monitoring: early and late boot validation events, log-based alerts on failures, updating the integrity policy baseline after legitimate changes."
sources: ["https://cloud.google.com/compute/shielded-vm/docs/integrity-monitoring", "https://cloud.google.com/compute/shielded-vm/docs/automating-responses-integrity-failures", "https://cloud.google.com/compute/shielded-vm/docs/modifying-shielded-vm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shielded VM integrity monitoring alerts

Integrity monitoring compares each boot's measurements to a baseline policy. Results are logged as **earlyBootReportEvent** and **lateBootReportEvent**.

## 1. Find failures
```
resource.type="gce_instance"
logName:"projects/<PROJECT_ID>/logs/compute.googleapis.com/shielded_vm_integrity"
jsonPayload.lateBootReportEvent.policyEvaluationPassed="false"
```
Both event types are reported; read `policyEvaluationPassed` on each.

## 2. Alert
Create a log-based metric on that filter (counter, label `instance_id`) and an alert policy on it > 0.
For automated response, route the same filter via a log sink to Pub/Sub and a function that responds (the automating-responses page has a sample).

## 3. Legit change → update baseline
Legitimate changes to the boot chain alter measurements and can fail validation. After
confirming the change was yours:
```bash
gcloud compute instances update web-1 --zone=<Z> --shielded-learn-integrity-policy
```
This updates the integrity policy baseline. Do it in patch automation right after
a planned reboot, never blindly on every failure.

## Gotchas
- Legitimate boot-chain changes can fail validation until the baseline is updated: expect noise after patching and correlate with patch jobs.
- Disabling the vTPM disables integrity monitoring.
- `--shielded-learn-integrity-policy` on a compromised VM bakes the compromise in.

## Verify
- [ ] After a deliberate kernel update in test, the alert fires; after learning the policy and rebooting, `policyEvaluationPassed=true`.

## Checked

2026-10-28. Confirmed against: Shielded VM integrity-monitoring pages: earlyBootReportEvent and lateBootReportEvent fields, policyEvaluationPassed, the shielded_vm_integrity log name, --shielded-learn-integrity-policy, vTPM dependency.

Removed or rewritten: the early/late boot scope descriptions, PCR wording, the exact log_id filter form (replaced with the documented logName form) and the claim that every kernel patch fails once.

Method: documentation only; no commands were run.
