---
id: computing-software.cloud-infrastructure-engineering.aws.shield-advanced-health-based-detection-and-auto-mitigation
name: shield-advanced-health-based-detection-and-auto-mitigation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, shield-advanced, health-based-detection, automatic-application-layer-mitigation, ddos, route53-health-checks]
level: advanced
status: docs-checked
description: "Associate Route 53 health checks with Shield Advanced protections for health-based detection, and enable automatic application layer DDoS mitigation with its caveats."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-health-checks.html", "https://docs.aws.amazon.com/waf/latest/developerguide/ddos-automatic-app-layer-response.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shield Advanced health-based detection and automatic mitigation

## 1. Health-based detection
Works for any protected resource type except Route 53 hosted zones. You define a Route 53 health check, verify it reports healthy, then associate it with the Shield Advanced protection.
```bash
aws shield associate-health-check --protection-id <PROTECTION_ID> \
  --health-check-arn arn:aws:route53:::healthcheck/<HC_ID>
aws shield describe-protection --protection-id <PROTECTION_ID>
```
- Layers 3/4 (Network Load Balancers, Elastic IPs, Global Accelerator standard accelerators): detection is more accurate, and while the check is unhealthy Shield can mitigate faster and at lower thresholds, including smaller attacks.
- Layer 7 (CloudFront distributions, Application Load Balancers): web request flood alerts need a statistically significant traffic deviation plus changes in traffic patterns. With an unhealthy check, smaller deviations alert and events are reported sooner; with a healthy check, larger deviations are needed.
- Requirements: the check must report healthy at association, be relevant to the resource's health, and stay in place (do not delete a check in use). Shield Advanced does not manage the check; you maintain it. It works best when it reports healthy only when the app is within acceptable parameters.
- Health checks are required for Shield Response Team (SRT) proactive engagement.

## 2. Automatic application layer DDoS mitigation
```bash
aws shield enable-application-layer-automatic-response --resource-arn <RESOURCE_ARN> --action Count={}
aws shield update-application-layer-automatic-response --resource-arn <RESOURCE_ARN> --action Block={}
```
`Action` is `Block` or `Count`; the configuration `Status` is `ENABLED` or `DISABLED` (Shield API model).
- Shield maintains a rule group in the resource's web ACL (protection pack). It has a rate-based rule tracking request volume from IPs known as DDoS sources, and Shield adds custom rules during detected attacks after comparing traffic to historic baselines.
- Legacy status: the page notes that from March 26, 2026 the Anti-DDoS managed rule group for AWS WAF is the default solution for HTTP request floods and supersedes this Layer 7 auto-mitigation feature. Existing Shield Advanced customers can keep using the legacy feature; new customers who need it must contact AWS Support.
- Caveats: only web ACLs created with AWS WAF v2; baseline takes between 24 hours and 30 days after associating a web ACL; the rule group uses 150 WCUs of the web ACL's capacity; its metrics are not viewable; for a web ACL protecting several resources, only mitigations that do not harm any of them are deployed; some attacks end before custom rules deploy.
- For an ALB receiving traffic through a CDN such as CloudFront, mitigation is reduced because client attributes may be lost; enable it on the CloudFront distribution instead.
- It does not interact with protection groups; mitigation is per resource.

## Method
Rewritten from the two cited WAF Developer Guide pages plus the Shield API model for CLI names and enum values. Advice on rule group naming, starting in Count mode and health-check design was not on the pages and was dropped.

## Checked
Checked 2026-11-08 against the two cited pages and the Shield API model (botocore).
Method: docs-only read of cited pages, 2026-11-08
