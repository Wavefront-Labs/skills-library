---
id: computing-software.cybersecurity-defensive.splunk.splunk-uba-integration
name: splunk-uba-integration
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-uba, ueba, enterprise-security, anomaly-detection, insider-threat, identity-resolution]
level: advanced
status: draft
description: "Integrate Splunk User Behavior Analytics with Enterprise Security: data sources, sending UBA threats/anomalies to ES, threat review, and pulling ES identities into UBA."
sources: ["https://docs.splunk.com/Documentation/UBA/latest/Install/About", "https://docs.splunk.com/Documentation/UBA/latest/Integration/SendthreatstoES", "https://docs.splunk.com/Documentation/UBA/latest/GetDataIn/AddData"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Splunk UBA integration

Splunk UBA is an ML appliance cluster that models users/devices from Splunk data and outputs
**anomalies** (single behaviours) and **threats** (chained anomalies). ES receives them.

## Data in
- UBA pulls from Splunk via data sources defined in UBA (Splunk direct, raw events) using CIM-mapped
  searches: AD/Windows auth, VPN, proxy, firewall, DNS, DHCP, endpoint. HR data (identity, manager,
  termination dates) improves peer grouping.
- Identity resolution: UBA maps IP -> host -> user using DHCP, VPN and AD logon events. Bad DHCP
  data is the most common cause of anomalies on the wrong user.
- Pull ES assets/identities into UBA so entities carry the same priority and categories.

## Output to ES
- Configure Splunk ES output connector in UBA (Manage > Output Connectors): threats become ES
  notables (source "UBA"), anomalies can go to the `ueba` index and to ES risk framework.
- In ES, the UEBA content (Threat Review, Anomalies) and risk modifiers show UBA results.
- Feed threat feedback back: closing a UBA threat as not-malicious tunes future scoring.

## Operating it
- Size the cluster by event rate and entity count (1, 3, 5, 7, 10, 20 node deployments).
- Review anomaly rules: disable noisy models (e.g. unusual machine access for jump hosts) by
  scoping with whitelists rather than deleting models.
- Expect a learning period (days to weeks) before models are stable after onboarding new data.

## Gotchas
- UBA does not see data that is not CIM-mapped; check data source health in UBA after TA upgrades.
- Service accounts dominate anomalies; tag them in identities so UBA treats them separately.
- UBA reached end of sale; for new builds evaluate ES 8 behavioural analytics or alternatives.

## Verify
A planted test (e.g. a test account logging in from a new country and accessing many hosts) yields
anomalies within the model window and a notable in ES with the UBA threat link.
