---
id: computing-software.cybersecurity-defensive.cloud-security.steampipe-powerpipe
name: steampipe-powerpipe
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [steampipe, powerpipe, cloud-inventory-sql, compliance-benchmarks, multi-cloud-queries, cspm]
level: practitioner
status: draft
description: "Query cloud posture with Steampipe SQL and run Powerpipe compliance benchmarks across AWS, Azure, GCP and SaaS: plugins, connections, aggregators and scheduled reports."
sources: ["https://steampipe.io/docs", "https://powerpipe.io/docs", "https://hub.powerpipe.io/mods/turbot/aws_compliance", "https://hub.steampipe.io/plugins"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Steampipe and Powerpipe

Steampipe exposes cloud and SaaS APIs as Postgres tables; Powerpipe runs benchmark/dashboard "mods"
(CIS, NIST, PCI, etc.) on top. Read-only, open source, good for ad hoc posture questions and custom checks.

## Setup
```
steampipe plugin install aws azure gcp github
# ~/.steampipe/config/aws.spc
connection "aws_all" { type = "aggregator"  plugin = "aws"  connections = ["aws_*"] }
connection "aws_prod" { plugin = "aws"  profile = "prod-audit"  regions = ["*"] }
```
Use read-only audit roles (SecurityAudit/ViewOnlyAccess, Reader) per account; aggregators query many accounts in parallel.

## Queries
```sql
-- security groups open to the world on admin ports
select account_id, group_id, ip_protocol, from_port, to_port
from aws_vpc_security_group_rule
where type = 'ingress' and cidr_ipv4 = '0.0.0.0/0' and (from_port <= 22 and to_port >= 22 or from_port <= 3389 and to_port >= 3389);

-- IAM access keys older than 90 days
select user_name, access_key_id, create_date from aws_iam_access_key
where status = 'Active' and create_date < now() - interval '90 days';
```

## Benchmarks
```
powerpipe mod install github.com/turbot/steampipe-mod-aws-compliance
powerpipe benchmark run aws_compliance.benchmark.cis_v300 --export results.json --export results.html
powerpipe server      # dashboards in a browser
```

## Operations
- Schedule benchmark runs (CI job/cron) and store results; diff between runs for new failures.
- Cache settings (`cache_ttl`) trade freshness vs API load; throttling on large estates.

## Gotchas
- Queries hit live APIs: big org-wide queries can be slow or throttled.
- It is a point-in-time scanner, not continuous monitoring or prevention.

## Verify
- [ ] Benchmark runs successfully across all accounts with the audit role.
- [ ] Custom queries for org-specific policies saved in the repo.
