---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-ngfw-and-cloud-ids
name: cloud-ngfw-and-cloud-ids
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-ngfw, ngfw, cloud-ids, intrusion-detection, intrusion-prevention, ips, firewall-endpoint, security-profiles, threat-prevention, tls-inspection, fqdn-firewall-rules, geo-firewall-rules, address-groups, threat-intelligence-firewall, packet-mirroring, palo-alto, network-security]
level: advanced
status: docs-checked
description: "Add L7 threat detection to a VPC: Cloud NGFW Standard rules (FQDN, geo, threat intel), NGFW Enterprise endpoints with security profiles and TLS inspection, and Cloud IDS."
sources: ["https://cloud.google.com/firewall/docs/about-firewalls", "https://cloud.google.com/firewall/docs/about-intrusion-prevention", "https://cloud.google.com/firewall/docs/configure-intrusion-prevention", "https://cloud.google.com/intrusion-detection-system/docs/overview", "https://cloud.google.com/firewall/docs/firewall-policies-rule-details"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cloud NGFW and Cloud IDS

**Goal:** east-west and egress traffic inspected for exploits and malware by Palo Alto-powered
signatures, with blocking where you choose and detection everywhere, without deploying appliance VMs.

## 1. The three tiers
| Tier | What | Where it lives |
|---|---|---|
| **Cloud NGFW Essentials** | VPC firewall rules + network/hierarchical firewall policies, tags, IAM-governed | every VPC |
| **Cloud NGFW Standard** | Essentials + rules on **FQDN**, **geolocation**, **Threat Intelligence lists**, **address groups** | firewall policy rules |
| **Cloud NGFW Enterprise** | Standard + **intrusion prevention (IPS)** and **TLS inspection** via zonal *firewall endpoints* | zonal firewall endpoints |
**Cloud IDS** is the detection-only sibling: packet mirroring to a managed inspection endpoint using Palo Alto Networks threat technologies; detection only, no blocking.

## 2. Standard-tier rules
```bash
gcloud compute network-firewall-policies rules create 1000 --firewall-policy=prod-policy --global-firewall-policy \
  --direction=EGRESS --action=deny --layer4-configs=all \
  --dest-threat-intelligence=iplist-known-malicious-ips,iplist-tor-exit-nodes --enable-logging
gcloud compute network-firewall-policies rules create 1100 --firewall-policy=prod-policy --global-firewall-policy \
  --direction=EGRESS --action=allow --layer4-configs=tcp:443 --dest-fqdns=api.stripe.com,*.githubusercontent.com --target-secure-tags=<ORG>/env/prod
gcloud compute network-firewall-policies rules create 1200 --firewall-policy=prod-policy --global-firewall-policy \
  --direction=INGRESS --action=deny --layer4-configs=all --src-region-codes=KP,IR --enable-logging
gcloud network-security address-groups create partners --type=IPV4 --capacity=100 --location=global --items=203.0.113.0/24
```
- Threat Intelligence feed names such as `iplist-tor-exit-nodes` are listed in the Google Threat Intelligence documentation for firewall rules; check the current list there.

## 3. Enterprise: IPS with firewall endpoints
```bash
gcloud network-security firewall-endpoints create fe-ew1b --zone=europe-west1-b --organization=<ORG_ID> --billing-project=<P>
gcloud network-security firewall-endpoint-associations create fe-ew1b-prod --zone=europe-west1-b \
  --network=projects/<P>/global/networks/prod-vpc --endpoint=organizations/<ORG_ID>/locations/europe-west1-b/firewallEndpoints/fe-ew1b
gcloud network-security security-profiles threat-prevention create tp-prod --organization=<ORG_ID> --location=global
gcloud network-security security-profiles threat-prevention add-override tp-prod --organization=<ORG_ID> --location=global \
  --severities=CRITICAL,HIGH --action=DENY
gcloud network-security security-profile-groups create spg-prod --organization=<ORG_ID> --location=global \
  --threat-prevention-profile=organizations/<ORG_ID>/locations/global/securityProfiles/tp-prod
gcloud compute network-firewall-policies rules create 2000 --firewall-policy=prod-policy --global-firewall-policy \
  --direction=INGRESS --action=apply_security_profile_group --security-profile-group=//networksecurity.googleapis.com/organizations/<ORG_ID>/locations/global/securityProfileGroups/spg-prod \
  --layer4-configs=all --src-ip-ranges=0.0.0.0/0 --enable-logging
```
- A firewall endpoint is a **zonal** resource configured at organization or project level; associate it with each network that needs inspection.
- Rules with the `apply_security_profile_group` action intercept matched traffic and send it to the firewall endpoint for Layer 7 inspection.
- Override a signature by its threat ID, or by severity, in the threat prevention profile.
- **TLS inspection**: create a CA pool (Certificate Authority Service) and a trust config and add them to a TLS inspection policy (`gcloud network-security tls-inspection-policies import`); see the Cloud NGFW TLS inspection docs.

## 4. Cloud IDS (detection only)
```bash
gcloud ids endpoints create ids-ew1 --network=prod-vpc --zone=europe-west1-b --severity=INFORMATIONAL --async
# needs private services access on the VPC; returns an endpoint forwarding rule
gcloud compute packet-mirrorings create mirror-prod --region=europe-west1 --network=prod-vpc \
  --mirrored-subnets=prod-apps --collector-ilb=<IDS_ENDPOINT_FORWARDING_RULE> --filter-direction=both
```
- `--severity` sets the minimum alert severity level of the IDS endpoint. After creating an endpoint you attach a packet mirroring policy to it.

## 5. Which to use
- Everyone: Standard-tier threat-intel + geo denies on egress and ingress.
- Compliance needs IDS evidence, you do not want blocking risk: Cloud IDS.
- You want **blocking** of exploits/malware inline and TLS decryption: NGFW Enterprise.

## Gotchas
- Inspecting egress traffic from serverless workloads is not supported by Cloud NGFW intrusion prevention.
- Cloud IDS needs private services access on the VPC.

## Verify
- [ ] `curl` to a Tor exit IP from a prod VM is dropped and the firewall log shows the threat-intel rule.
- [ ] IPS: a known test signature from a protected VM is blocked and appears in the threat logs.
- [ ] Cloud IDS: a scan from a mirrored VM produces threat findings.

## Checked
2026-10-28. Confirmed on the Cloud NGFW about-firewalls, intrusion prevention, configure-intrusion-prevention and rule-details pages and the Cloud IDS overview: Palo Alto Networks technologies, zonal firewall endpoints at org or project level, `apply_security_profile_group` action, threat ID and severity overrides, CRITICAL severity, CA pool plus trust config for TLS inspection, serverless egress limitation, Cloud IDS packet mirroring, private services access and minimum alert severity. gcloud commands and flags passed check_commands. Removed: pricing statements, most threat-intel feed names, FQDN and geo semantics, SCC and log source names, default override actions, bandwidth and gotcha claims not found in the pages.
Method: documentation only; no commands were run.
