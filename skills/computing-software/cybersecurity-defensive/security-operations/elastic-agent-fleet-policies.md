---
id: computing-software.cybersecurity-defensive.security-operations.elastic-agent-fleet-policies
name: elastic-agent-fleet-policies
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [elastic-security, elastic-agent-fleet, fleet-server, agent-policies, integrations, elastic-defend, enrollment-tokens]
level: practitioner
status: docs-checked
description: "Deploy Elastic Agent with Fleet: Fleet Server, agent policies and integrations, enrollment tokens, Elastic Defend, upgrades and health monitoring."
sources: ["https://www.elastic.co/guide/en/fleet/current/fleet-overview.html", "https://www.elastic.co/guide/en/fleet/current/install-fleet-managed-elastic-agent.html", "https://www.elastic.co/guide/en/security/current/install-endpoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Agent and Fleet policies

**Goal:** one agent per host, centrally managed, collecting logs and running Elastic Defend
with policies you can change from Kibana.

## Architecture
- **Fleet** (Kibana UI) manages **agent policies**; each policy is a set of
  **integrations** (System, Windows, Elastic Defend, Auditd Manager, network packet capture).
- **Fleet Server** is the control plane agents check in to (included in Elastic Cloud;
  self-managed: run it on a dedicated host).
- Agents ship data straight to Elasticsearch (or Logstash/Kafka outputs).

## Rollout
1. Create policies by role: `windows-workstations`, `windows-servers`, `linux-servers`,
   `domain-controllers`. Different log sets and Defend settings per role.
2. Add integrations: System, Windows (Security, Sysmon, PowerShell channels), Elastic Defend
   (start in Detect mode, move to Prevent per policy after a tuning period).
3. Enrollment token per policy (Fleet > Enrollment tokens). Install:
   ```
   elastic-agent install --url=https://fleet.example.internal:8220 --enrollment-token=<token>
   ```
   Windows MSI/Intune and Linux packages accept the same flags; use the CA flag
   (`--certificate-authorities`) for private PKI.
4. Tags and namespaces: set a `namespace` per environment (prod/dev) so data streams split
   (`logs-system.auth-prod`) and retention/permissions can differ.

## Operations
- **Upgrades:** select agents > Upgrade, with a rollout period to stagger; upgrade Fleet
  Server first.
- **Health:** Fleet > Agents shows Healthy/Unhealthy/Offline; drill into integration
  errors. Offline for days usually means decommissioned or network blocked.
- Agent diagnostics: `elastic-agent status`, `elastic-agent diagnostics` for support bundles.

## Gotchas
- Changing an integration in a policy pushes to every agent on it; test on a canary policy.
- Elastic Defend conflicts with other EDR/AV unless exclusions are set both ways.
- Port 8220 (Fleet Server) and 443/9200 (Elasticsearch) must be reachable from every agent.
- Unenrolled agents keep running local config; uninstall properly.

## Checked
2026-10-28. Confirmed in the Elastic Agent command reference and agent policy pages: `elastic-agent install` enrolment flags, `elastic-agent status` and `diagnostics`. Removed: the 2+ Fleet Server HA figure and the per-policy uninstall token claim (not found in the fetched pages). Policy and namespace names are examples.
Method: documentation only; no commands were run.

## Verify
```
GET _cat/indices/logs-*,metrics-*?v&s=index
```
In Kibana, Fleet shows all expected hosts Healthy, and Security > Hosts lists them with recent events.
