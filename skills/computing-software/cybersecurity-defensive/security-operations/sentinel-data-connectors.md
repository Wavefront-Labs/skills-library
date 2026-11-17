---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-data-connectors
name: sentinel-data-connectors
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-data-connectors, data-collection-rules, dcr, azure-monitor-agent, log-analytics, content-hub, siem-onboarding]
level: practitioner
status: docs-checked
description: "Onboard data to Microsoft Sentinel: content hub solutions, service-to-service connectors, Azure Monitor Agent with data collection rules, and ingestion-time transforms."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/connect-data-sources", "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-overview", "https://learn.microsoft.com/en-us/azure/sentinel/data-transformation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel data connectors and DCR-based ingestion

**Goal:** get the right logs into the Sentinel Log Analytics workspace, in the right
tables, with filtering chosen on purpose.

## Connector families
- **Service-to-service:** out-of-the-box connectors for Microsoft services that integrate
  in real time; for example the Microsoft Defender XDR connector brings in data from
  Office 365, Microsoft Entra ID, Defender for Identity and Defender for Cloud Apps. Amazon Web
  Services is also supported service-to-service.
- **Agent-based (Azure Monitor Agent, AMA):** Syslog and Common Event Format (CEF) from
  Linux-based, Syslog-supporting devices; the agent runs on the device or on a dedicated Linux
  log forwarder. Windows Security Events via AMA and Windows Forwarded Events are also AMA-based.
- **Custom logs:** file-based logs collected on Windows or Linux, landing in custom tables.
- **Custom connectors:** the Codeless Connector Framework, or the Logs Ingestion API from an
  Azure Function or Logic App; AMA or Logstash can also be used.
- Connectors come with **solutions**: install the solution from the Content Hub to add its
  connector, then use the Data connectors page, which lists installed or in-use connectors.

## Syslog and CEF
The AMA receives plain Syslog or CEF from the Syslog daemon over UDP; the daemon forwards to
the agent internally over TCP or UDS depending on version. After successful configuration,
Syslog messages appear in the `Syslog` table and CEF messages in `CommonSecurityLog`.

## Data collection rules (DCRs)
A DCR defines the data to collect, the schema of incoming data, the transformations to apply,
and the destination. A DCR association (DCRA) links a resource to a DCR; the relationship is
many-to-many and you can associate up to 30 DCRs with a single resource. AMA connectors use DCRs
associated with the agent; direct Logs Ingestion API calls specify the DCR in the call; a
workspace transformation DCR is applied directly to the workspace and covers workflows that do
not otherwise use DCRs (for example diagnostic-settings connections and service-to-service
connectors for tables that support transformations). After creating or updating a workspace
transformation DCR, allow some time before it takes effect.

## Ingestion-time transformations
Transformations are KQL queries in a DCR that run against each record before it is stored, to
filter rows or columns, mask sensitive data, normalise to ASIM or enrich. Legacy codeless and
Azure Functions-based API connectors are listed as not currently supported for transformations.
With Sentinel enabled, transformations on Analytics tables are not subject to Azure Monitor's
filtering ingestion charge; Basic tables incur it when a transformation drops more than 50% of
incoming data.

## Gotchas
- The legacy Log Analytics agent is replaced by AMA, and the legacy HTTP Data Collector API is replaced by the Logs Ingestion API. The connectors page says the Data Collector API stops being supported after September 14, 2026; migrate to the Logs Ingestion API or the Codeless Connector Framework.
- Microsoft Sentinel in the Azure portal is supported only until March 31, 2027; after that it is available only in the Defender portal.
- Each connector has a support type (Microsoft-supported, partner-supported, community-supported) shown on its page; check it before relying on a connector.
- The Sentinel data lake tier is not affected by analytics-tier Purge; plan retention and GDPR handling accordingly.

## Verify
Query the destination table (`Syslog` or `CommonSecurityLog`) in Logs after configuring the
connector and confirm recent rows arrive.

## Checked
Date: 2026-11-07. Read in full: "Microsoft Sentinel data connectors" (connector families, Syslog/CEF flow, support types, Data Collector API and portal dates), "Data collection rules in Azure Monitor" (DCR contents, DCRA, 30 DCR limit, scenarios, transformations) and "Custom data ingestion and transformation in Microsoft Sentinel" (connector-type DCR support table, filtering charge note). The DCR page now resolves at the data-collection URL, so the source link was updated. Removed as unconfirmed by these pages: Windows event-set options and the XPath sample, event IDs, the `SecurityEvent` and `Event` table names, Okta/GitHub/SQS connectors, free-or-cheap and cost claims, Azure Arc and Azure Policy auto-association, the `transformKql` property and sample, port 514 and rsyslog/syslog-ng, the "Connected status" claim and the "do not double-collect" and "MMA retired" statements. The linked DCR structure and Syslog/CEF via AMA pages were not read.
Method: documentation only; no commands were run.
