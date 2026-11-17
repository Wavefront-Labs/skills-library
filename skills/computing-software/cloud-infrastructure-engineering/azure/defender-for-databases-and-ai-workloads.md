---
id: computing-software.cloud-infrastructure-engineering.azure.defender-for-databases-and-ai-workloads
name: defender-for-databases-and-ai-workloads
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, defender-for-databases, defender-for-ai, defender-for-sql, threat-protection]
level: advanced
status: draft
description: "Enable and tune Defender for Databases (Azure SQL, SQL on machines, open-source DBs, Cosmos DB) and Defender for AI services, and triage their alerts."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/quickstart-enable-database-protections", "https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-sql-introduction", "https://learn.microsoft.com/azure/defender-for-cloud/alerts-reference"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defender for Databases and Defender for AI

**Goal:** threat detection and vulnerability assessment for data stores and AI endpoints.

## Defender for Databases (plan bundle)
| Sub-plan | Covers | Signals |
|---|---|---|
| Azure SQL Databases | SQL DB, MI, Synapse dedicated pools | SQL injection, anomalous logins, brute force, unusual export |
| SQL servers on machines | SQL Server on VMs, Arc, on-prem | Same, via the Defender for SQL agent (AMA-based) |
| Open-source relational | PostgreSQL / MySQL flexible, MariaDB | Brute force, anomalous access |
| Azure Cosmos DB | NoSQL API | SQL injection patterns, anomalous access, data exfiltration |
```bash
az security pricing create -n SqlServers --tier Standard
az security pricing create -n SqlServerVirtualMachines --tier Standard
az security pricing create -n OpenSourceRelationalDatabases --tier Standard
az security pricing create -n CosmosDbs --tier Standard
```
- **Vulnerability assessment** for Azure SQL uses the express configuration (no storage account needed); findings under recommendations "SQL databases should have vulnerability findings resolved". Set baselines to suppress accepted findings.
- SQL on machines needs AMA plus the Defender for SQL extension; policy-based auto-provisioning.

## Defender for AI services
- Threat protection for Azure OpenAI / AI Foundry deployments: detects jailbreak attempts, prompt injection, sensitive data exposure, credential theft attempts and anomalous usage, using Azure AI Content Safety Prompt Shields signals.
```bash
az security pricing create -n AI --tier Standard
```
- Enable **user prompt evidence** to include prompt/response snippets in alerts (privacy review first).
- Pass end-user context (user ID, IP, application name) in requests via the `user_security_context` parameter so alerts identify the actual user behind an app.

## Triage
- Alerts flow to Defender for Cloud, Defender XDR incidents and Sentinel. Example SQL alerts: "Potential SQL injection", "Login from a suspicious IP", "Unusual export location". AI: "Jailbreak attempt blocked", "Access from suspicious IP", "Anomalous tool invocation".
- Investigate with SQL auditing logs (`SQLSecurityAuditEvents`) and AI diagnostic logs; tune with suppression rules for known scanners.

## Verify
- [ ] `az security pricing list --query "value[?pricingTier=='Standard'].name"` includes the plans.
- [ ] Simulated alert (for example SQL injection test string from a lab client) appears in Defender for Cloud.
