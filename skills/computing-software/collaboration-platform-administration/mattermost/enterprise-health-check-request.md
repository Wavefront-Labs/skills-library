---
id: computing-software.collaboration-platform-administration.mattermost.enterprise-health-check-request
name: enterprise-health-check-request
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [health-check, support-packet, enterprise-support, health-report]
level: intro
status: docs-checked
description: "Request a Mattermost Enterprise Health Check by submitting a Support Packet and receive the report within two weeks."
sources: ["https://docs.mattermost.com/administration-guide/manage/request-server-health-check.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Requesting an Enterprise Health Check

The Mattermost Health Check is an evaluation of a system's operational health offered to Enterprise customers. It draws on your configuration, user activity and log events to help you find issues early, improve collaboration security, optimise resource use and scale, and reduce downtime.

Regular assessment helps keep performance optimal with minimal delay, keeps user experience reliable (no missed messages or slow loads), keeps security and compliance settings current, and ensures capacity matches growing usage.

Three steps:
1. Generate a Support Packet. It contains logs, configuration and usage data about your environment.
2. Submit it through the Mattermost support system as a standard support request, and include "Health Check Provided" in the subject line.
3. Receive the Health Check report within two weeks of submission. It contains a detailed analysis of current health, actionable recommendations for performance, reliability and security, and best-practice guidance for future maintenance.

If you only want your own automated liveness checks for a self-hosted deployment, configure server health check probes instead, which is a separate documented task. For questions, contact your Customer Success Manager or Technical Account Manager, the Mattermost Support Team, or the Help Center. Review the Support Packet contents before sending, because it includes configuration data about your deployment.

## Checked

Confirmed against the Request a server Health Check page: Enterprise availability, the three steps, the "Health Check Provided" subject line, the two-week report, report contents and contact routes. The closing review advice is the author's.

Method: docs-checked 2026-11-09 against the full administration-guide/manage/request-server-health-check page (source rst from the mattermost/docs repo).
