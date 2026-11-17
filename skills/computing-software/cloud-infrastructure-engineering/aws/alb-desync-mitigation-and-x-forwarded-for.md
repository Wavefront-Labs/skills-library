---
id: computing-software.cloud-infrastructure-engineering.aws.alb-desync-mitigation-and-x-forwarded-for
name: alb-desync-mitigation-and-x-forwarded-for
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, alb, desync-mitigation, x-forwarded-for, http-request-smuggling, client-ip]
level: advanced
status: docs-checked
description: "Configure ALB desync mitigation mode against HTTP request smuggling and control X-Forwarded-For processing so backends log the real client IP safely."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-load-balancer-attributes.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/x-forwarded-headers.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALB desync mitigation and X-Forwarded-For

## 1. Desync mitigation mode
```bash
aws elbv2 modify-load-balancer-attributes --load-balancer-arn <ALB_ARN> --attributes \
  Key=routing.http.desync_mitigation_mode,Value=defensive \
  Key=routing.http.drop_invalid_header_fields.enabled,Value=true
```
| Mode | Behaviour |
|---|---|
| `monitor` | allows everything, only classifies |
| `defensive` (default) | blocks Severe requests (400 and connection close); routes Ambiguous requests but closes the client and target connections |
| `strictest` | blocks Acceptable, Ambiguous and Severe: only Compliant requests pass |
Classifications (Compliant, Acceptable, Ambiguous, Severe) appear in access logs
(`classification`, `classification_reason`). Metric: `DesyncMitigationMode_NonCompliant_Request_Count`.
Move to `strictest` once logs show no legitimate Acceptable or Ambiguous traffic. Many Ambiguous requests in defensive mode raise new-connection counts and can add LCU charges.

## 2. X-Forwarded-For processing
```bash
aws elbv2 modify-load-balancer-attributes --load-balancer-arn <ALB_ARN> --attributes \
  Key=routing.http.xff_header_processing.mode,Value=append \
  Key=routing.http.xff_client_port.enabled,Value=false
```
- `append` (default): ALB adds the client IP to the existing header.
- `preserve`: passes the header unchanged (only when a trusted proxy in front sets it).
- `remove`: strips it.
- Clients can forge leading entries. Trust only the **rightmost** IP added by your ALB (or the Nth from
  the right if you have N trusted proxies). Configure the app framework accordingly
  (nginx `real_ip_recursive`, Express `trust proxy` hop count).
- `X-Forwarded-Proto` and `X-Forwarded-Port` tell the app the original scheme for redirects.

## 3. NLB difference
NLB does not add headers; use client IP preservation or Proxy Protocol v2.

## Verify
- [ ] Access logs show `classification` field populated; non-compliant count reviewed.
- [ ] A request with a forged `X-Forwarded-For: 1.2.3.4` is logged by the app with the real client IP.

## Checked

Checked 2026-10-27 against the Elastic Load Balancing documentation for Application Load Balancers (load balancer attributes, HTTP headers).
- Corrected: `strictest` blocks Acceptable, Ambiguous and Severe requests; in `defensive` mode Ambiguous requests are routed but connections are closed (possible LCU cost) and Severe requests get a 400.
- Confirmed: default mode `defensive`, modes `monitor`/`defensive`/`strictest`, metric `DesyncMitigationMode_NonCompliant_Request_Count`, `routing.http.xff_header_processing.mode` values `append`/`preserve`/`remove` (default `append`), `routing.http.xff_client_port.enabled`, `routing.http.drop_invalid_header_fields.enabled`.

Method: documentation only; no commands were run.
