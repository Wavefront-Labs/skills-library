---
id: computing-software.cybersecurity-defensive.zitadel.production-checklist
name: production-checklist
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, production, checklist, high-availability, hardening]
level: advanced
status: docs-checked
description: "Walk through ZITADEL's production checklist covering infrastructure, high availability, networking, setup and security items."
sources:
  - https://zitadel.com/docs/self-hosting/manage/productionchecklist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The checklist groups items by area.

Infrastructure: provision everything with infrastructure as code such as Terraform, use a secrets manager, and minimize manual steps.

High availability:

- ZITADEL containers on an orchestrator such as Kubernetes, or a serverless platform such as Knative or Cloud Run; split `zitadel init` and `zitadel setup` for fast start-up.
- A highly available PostgreSQL with logging, timeouts and regular backups, restore scenarios tested before go-live, and connections secured from outside your network.
- Highly available load balancer, reverse proxies and web application firewall.

Networking: a Layer 7 firewall supporting HTTP/2, IP limits if needed, rate limiting for specific endpoints such as API versus frontend, bot detection, and filtering of IPv6 traffic too.

ZITADEL setup: a tested SMTP server, custom branding, an SMS service such as Twilio if needed, privacy policy, terms of service and help link, the masterkey in secure storage, and settings declared through the ZITADEL Terraform provider.

Security: no default, example or easy-to-guess credentials, a fully qualified domain name with a trusted certificate for external TLS, service accounts for applications that call the APIs, and instance administrators plus the login client isolated in a dedicated organization.

Monitoring: watch CPU and memory of ZITADEL and the database, open database connections, running instances, request latency, requests per second and per endpoint, TLS certificate lifetime, logs and ZITADEL metrics. Also on the list: a CDN for static assets and a security scanner against your deployment.

## Checked

2026-11-08. Read the production checklist page in full; replaced an invented closing line with the monitoring section.

Method: documentation only; no commands were run.
