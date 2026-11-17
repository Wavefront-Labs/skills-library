---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-architecture-and-concepts
name: crowdsec-architecture-and-concepts
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [concepts, security-engine, log-processor, local-api, central-api, remediation-component, decisions]
level: intro
status: docs-checked
description: "CrowdSec components and data flow: Log Processor, Local API, Central API, bouncers, alerts versus decisions, and the path from a log line to a block."
sources: ["https://docs.crowdsec.net/docs/concepts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Security Engine is the IDS you install. It has two parts: the **Log Processor (LP)**, which detects, and the **Local API (LAPI)**, which stores alerts and decisions. It can run standalone (LP and LAPI on one host) or distributed, with several Log Processors sending alerts to one shared LAPI. In a distributed setup the detection content (collections, parsers, scenarios) runs on the Log Processor machines.

- **Log Processor**: acquires logs, parses and enriches events, matches them against scenarios; it also receives HTTP requests for the AppSec (WAF) component. A triggered scenario or AppSec rule sends an **alert** to LAPI.
- **Local API**: receives alerts, applies profiles to create **decisions** (for example `ban`), exposes decisions to bouncers, and talks to the Central API.
- **Remediation components (bouncers)**: external pieces that enforce decisions in a firewall, reverse proxy or web server. Some support remediations other than ban, such as captcha.
- **Central API (CAPI)**: receives attack signals and redistributes the Community Blocklist.
- **Console**: web interface for alerts, decisions and fleet management.

## Typical flow

1. Install a collection from the Hub with `cscli`.
2. An acquisition file tells the LP which logs to read, for example a tail of an auth log.
3. Parsers extract fields such as source IP; enrichers add GeoIP or ASN.
4. A scenario correlates events over time and raises an alert.
5. LAPI applies profiles and creates a decision.
6. A bouncer pulls the decision and blocks.

Alerts are records of detection, decisions are instructions to remediate; both can also be created manually with `cscli`.

## Checked
2026-11-08. Confirmed against the Concepts page: Security Engine split into Log Processor and Local API, standalone versus distributed, LP/LAPI/bouncer/CAPI/Console roles, the log-line-to-block flow and the alert/decision definitions. Nothing removed.
Method: documentation only; no commands were run.
