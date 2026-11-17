---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-ids-endpoints-packet-mirroring-and-ngfw-tiers
name: cloud-ids-endpoints-packet-mirroring-and-ngfw-tiers
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-ids, cloud-ids-endpoint, ids-setup, packet-mirroring-setup, mirror-policy, ids-threat-logs, ids-alerts, ngfw-tiers, ngfw-enterprise-setup]
level: advanced
status: docs-checked
description: "Deploy Cloud IDS endpoints fed by packet mirroring, alert on threat logs, and choose Cloud NGFW Essentials, Standard or Enterprise (inline IPS via firewall endpoints)."
sources: ["https://cloud.google.com/intrusion-detection-system/docs/configuring-ids", "https://cloud.google.com/vpc/docs/using-packet-mirroring", "https://cloud.google.com/intrusion-detection-system/docs/logging", "https://cloud.google.com/firewall/docs/about-firewalls", "https://cloud.google.com/firewall/docs/configure-intrusion-prevention"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud IDS endpoints, packet mirroring and NGFW tiers

## 1. Cloud IDS (detect, out of band)
Setup needs IAM permissions, private services access on the VPC (allocate a separate, unique IP range for Cloud IDS even if you already use private services access for another service), endpoints, and packet mirroring.
```bash
gcloud ids endpoints create ids-euw2a --network=prod --zone=europe-west2-a --severity=INFORMATIONAL --enable-traffic-logs --async
gcloud ids endpoints describe ids-euw2a --zone=europe-west2-a
```
`--severity` is the minimum alert severity the endpoint reports (INFORMATIONAL, LOW, MEDIUM, HIGH or CRITICAL) and is required. The describe output includes `endpoint_forwarding_rule`, the URL to which Packet Mirroring sends traffic.

## 2. Feed it with packet mirroring
```bash
gcloud compute packet-mirrorings create mirror-app --region=europe-west2 --network=prod \
  --collector-ilb=<ENDPOINT_FORWARDING_RULE> \
  --mirrored-subnets=app-subnet --mirrored-tags=pci \
  --filter-cidr-ranges=0.0.0.0/0 --filter-protocols=tcp,udp,icmp --filter-direction=BOTH
```
The collector is an internal passthrough Network Load Balancer forwarding rule with Packet Mirroring enabled when it was created (this cannot be changed afterwards). Mirror only the sensitive subnets or tags.

## 3. Threat logs and alerts
```
resource.type="ids.googleapis.com/Endpoint"
logName="projects/<P>/logs/ids.googleapis.com%2Fthreat"
jsonPayload.alert_severity=("HIGH" OR "CRITICAL")
```
Create a log-based alert on that filter (route to the SOC) and export threat logs to the SIEM sink. Fields under `jsonPayload` include `threat_id`, `name`, `category`, `alert_severity`, `source_ip_address`, `destination_ip_address`, `direction`, `cves`. Behind a Google load balancer the source address is the Google Front End range, not the client. Logs go to the `_Default` bucket (30-day default retention) unless you route them elsewhere.

## 4. Cloud NGFW tiers
| Tier | Capabilities |
|---|---|
| Essentials | rules on IP ranges, ports and protocols; hierarchical, global and regional policies; secure tags |
| Standard | adds FQDN objects and threat intelligence |
| Enterprise | adds Layer 7 security: intrusion detection and prevention (inline IPS via firewall endpoints), URL filtering, malware sandbox, TLS inspection |
Enterprise setup:
```bash
gcloud network-security firewall-endpoints create fw-ep-euw2a --zone=europe-west2-a --organization=<ORG_ID> --billing-project=<P>
gcloud network-security firewall-endpoint-associations create assoc-prod --zone=europe-west2-a \
  --network=prod --endpoint=organizations/<ORG_ID>/locations/europe-west2-a/firewallEndpoints/fw-ep-euw2a --project=<P>
gcloud network-security security-profiles threat-prevention create ips-default --organization=<ORG_ID> --location=global
gcloud network-security security-profile-groups create spg-ips --organization=<ORG_ID> --location=global \
  --threat-prevention-profile=organizations/<ORG_ID>/locations/global/securityProfiles/ips-default
# firewall policy rule: --action=apply_security_profile_group --security-profile-group=//networksecurity.googleapis.com/organizations/<ORG_ID>/locations/global/securityProfileGroups/spg-ips
```
Create the firewall endpoint in the same zone as the workloads, and keep the workloads in that zone. A firewall endpoint does not inspect a network whose MTU is above its limit (8,500 bytes with jumbo frame support, 1,460 without). With TLS inspection you also create a CA pool and trust config for the TLS inspection policy, add it to the endpoint association, and use `--tls-inspect` on the rule. IDS detects; NGFW Enterprise blocks inline.

## Verify
- [ ] A test signature (from the vendor docs) produces a threat log entry.
- [ ] The alert routes HIGH/CRITICAL threats to the SOC channel.

## Checked
2026-10-31. Confirmed against the Cloud IDS configure and logging pages, the packet mirroring page, "About Cloud NGFW" and "Configure intrusion prevention": setup prerequisites, `--severity` values, `endpoint_forwarding_rule`, the collector requirement, log name, resource type, field names, retention default, tier descriptions, firewall endpoint zone and MTU limits, CA pool and trust config, `--tls-inspect`. All gcloud commands and flags checked against the gcloud reference. Removed: geolocation from the Standard tier, per-hour/per-GB billing remark, the "one endpoint per zone mirrored" and mirrored-VM bandwidth remarks (not on the pages read).
Method: documentation only; no commands were run.
