---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cryptomining-detection
name: cryptomining-detection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-anomaly-detection, cryptomining-detection, cost-as-security-signal, compromised-account, guardduty-cryptocurrency]
level: practitioner
status: docs-checked
description: "Treat cost anomalies as security signals: detect cryptomining and abuse from compromised credentials via spend spikes, unusual regions/GPU usage and threat findings."
sources:
  - https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-ec2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost anomalies as security signals

## Signals
- Sudden spend in **regions you never use**, especially GPU or large compute families.
- Many instances launched in minutes; new accounts/projects with spend.
- Spikes in data transfer out (exfiltration) or in AI/model API usage (stolen API keys).
- Threat findings: AWS GuardDuty EC2 findings such as `CryptoCurrency:EC2/BitcoinTool.B!DNS`
  and `Impact:EC2/BitcoinDomainRequest.Reputation`. GuardDuty advises that if the activity is
  unexpected you should assume the instance is compromised and follow its remediation guide.
  Other providers have equivalents (check their current threat-detection docs).

## Controls
1. **Prevent**: SCP/org policy deny on unused regions and GPU families outside approved accounts;
   quotas kept low for expensive instance types; no long-lived access keys.
2. **Detect fast**: usage-based alerts (instance count, vCPU-hours, GPU hours) in addition to daily
   cost anomaly monitors; route to security and FinOps together.
3. **Respond**: follow the leaked credential playbook - contain identity, terminate resources,
   preserve evidence (snapshots, logs), check persistence.
4. **Recover**: open a provider support case for billing adjustment with incident evidence.

## Gotchas
- Cost data lags hours; attackers spend thousands meanwhile. Usage/API event alerts are faster.
- Anomaly alerts sent only to FinOps, who don't treat them as security incidents.

## Verify
- [ ] Test: launching a GPU instance in a disallowed region is denied and alerts.

## Checked
Method: docs-checked 2026-11-09 against the AWS GuardDuty EC2 finding types page (read via summarising fetch plus search of the saved page text). The Azure Defender alerts index lists no crypto-mining alert and the GCP Security Command Center URL returned 404, so those sources and claims were dropped. General control advice is practitioner guidance, not from the cited page.
