---
id: computing-software.cloud-infrastructure-engineering.aws.spot-placement-score-and-price-history
name: spot-placement-score-and-price-history
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, spot-instances, spot-placement-score, spot-price-history, capacity-planning]
level: practitioner
status: docs-checked
description: "Pick Regions and AZs for Spot with get-spot-placement-scores (target capacity, instance types or attributes, limits, how to act on a score) and view Spot price history."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-placement-score.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/how-sps-works.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/work-with-spot-placement-score.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances-history.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spot placement score and price history

## 1. Spot placement score
A recommendation of how likely a Spot request is to succeed in a Region or Availability Zone (Local Zones optional). It is
not a guarantee of capacity or of freedom from interruption. No extra charge.
- Scale 1 to 10 (10 highly likely, not guaranteed; 1 not likely). EC2 returns the top 10 Regions or top 10 AZs. The same
  score can appear for several results, and the same request can score differently at different times.
- Inputs: target capacity in instances (default), `vcpu` or `memory-mib` via `TargetCapacityUnitType`; and either instance
  types or instance attributes, never both. Instance types: give at least three different ones or you get a low score
  (the minimum does not apply to P, G, Trn and Inf families).
- Output scope: Regions by default; `SingleAvailabilityZone` true returns scored AZs, useful when all capacity must go in one AZ.
  `RegionNames` filters (with one Region you get all its AZs). Local Zones are ignored unless `IncludeLocalZones` is true.
```bash
aws ec2 get-spot-placement-scores --region us-east-1 --cli-input-json file://config.json
```
```json
{"TargetCapacity": 1000, "TargetCapacityUnitType": "vcpu", "SingleAvailabilityZone": true,
 "InstanceRequirementsWithMetadata": {"ArchitectureTypes": ["arm64"], "VirtualizationTypes": ["hvm"],
   "InstanceRequirements": {"VCpuCount": {"Min": 1, "Max": 12}, "MemoryMiB": {"Min": 512}}}}
```
(This config is the page's example. The page text says to provide `VCpuCount`, `MemoryMiB` and `CpuManufacturers`, yet its own
example omits the last, so test the call; `--generate-cli-skeleton` lists all fields.)
- Limits: the target capacity limit follows your recent Spot usage (low default if none); new request configurations can be
  limited within 24 hours if usage looks unlike the intended purpose; retrying configurations already used is still allowed.
- Using the score: it applies only if your Auto Scaling group, EC2 Fleet or Spot Fleet request uses exactly the same
  configuration (target capacity, unit, types or attributes) with the capacity-optimized allocation strategy. Act on a score
  immediately and get a fresh one for each capacity attempt. If scores are low, change the requirements or retry at another time.

## 2. Price history
Spot prices are set by EC2 and adjust gradually with long-term supply and demand. Instances launch at the current Spot price,
not above On-Demand. History covers the last 90 days, filterable by instance type, operating system and AZ.
```bash
aws ec2 describe-spot-price-history --instance-types c6i.xlarge --product-descriptions "Linux/UNIX" \
  --start-time 2025-04-01T00:00:00 --end-time 2025-04-02T00:00:00
```
Console: Spot Requests, Pricing history, with a comparison by AZ or instance type and optional normalized (per vCPU) prices.
Price history shows cost, not interruption risk.

## Gotchas
- A high score does not raise your Spot quota; the pages read do not cover quotas.
- Data residency or latency may rule out the best-scoring Region.
- The Spot Instance Advisor was not usable as a source (the page text returned is a JS shell with marketing text). Its marketing
  text recommends diversifying instance types and AZs and mentions attribute-based selection.

## Verify
- [ ] A score was taken for the exact configuration the fleet will use, immediately before launch.

## Checked
Date: 2026-11-07. Read in full: "Spot placement score" (limitations, costs), "How Spot placement score works" (steps 1 to 4),
"Calculate the Spot placement score" (CLI section and all example configs; console steps skimmed), and "View Spot Instance
pricing history". The "Required permissions" page was not opened. Botocore `GetSpotPlacementScores` checked for field names.
Removed: the Spot Instance Advisor source and its interruption buckets and savings text (page not readable), the
>=7 score threshold, the drop->15% interruption rule, the `price-capacity-optimized` recommendation (the pages say
capacity-optimized), the Service Quotas code `L-34B43A08`, the shell sort/head recipe, and "more types give higher scores".
Method: documentation only; no commands were run.
