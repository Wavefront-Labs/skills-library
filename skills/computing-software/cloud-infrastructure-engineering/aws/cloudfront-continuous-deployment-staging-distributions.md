---
id: computing-software.cloud-infrastructure-engineering.aws.cloudfront-continuous-deployment-staging-distributions
name: cloudfront-continuous-deployment-staging-distributions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudfront, continuous-deployment, staging-distribution, canary-cdn-config, header-based-routing, weight-based-routing]
level: advanced
status: docs-checked
description: "Test CloudFront config changes safely with continuous deployment: staging distributions, header or weight-based traffic policies, monitoring, and promote or roll back."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/continuous-deployment.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/continuous-deployment-workflow.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/continuous-deployment-quotas-considerations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFront continuous deployment

**Problem:** a CloudFront config change (cache policy, function, origin, headers) deploys
to every edge at once. Continuous deployment lets you route a slice of real traffic to a
**staging distribution** with the new config, watch it, then promote.

## 1. Create the staging distribution
```bash
ETAG=$(aws cloudfront get-distribution --id E1PRIMARY --query ETag --output text)
aws cloudfront copy-distribution --primary-distribution-id E1PRIMARY --if-match $ETAG \
  --staging --caller-reference staging-$(date +%s)
```
The copy is a staging distribution. Modify it with the change you want to test (`get-distribution-config` / `update-distribution` on the staging ID).

## 2. Continuous deployment policy
Header-based (testers only):
```json
{"StagingDistributionDnsNames": {"Quantity": 1, "Items": ["d111staging.cloudfront.net"]},
 "Enabled": true,
 "TrafficConfig": {"Type": "SingleHeader",
   "SingleHeaderConfig": {"Header": "<HEADER_NAME>", "Value": "true"}}}
```
Check the CloudFront guide for header naming rules. The policy `Type` is `SingleHeader` or `SingleWeight` (API model). Weight-based (canary of real users):
```json
"TrafficConfig": {"Type": "SingleWeight",
  "SingleWeightConfig": {"Weight": 0.05,
    "SessionStickinessConfig": {"IdleTTL": 300, "MaximumTTL": 600}}}
```
Maximum weight is 15% (0.15); session stickiness idle duration must be 300-3600 seconds (quotas and considerations page, read 2026-10-27). Create and attach:
```bash
aws cloudfront create-continuous-deployment-policy --continuous-deployment-policy-config file://cdp.json
# then set ContinuousDeploymentPolicyId on the PRIMARY distribution config and update it
```

## 3. Monitor
Compare the staging and primary distributions with standard or real-time logs and the CloudFront metrics for each distribution ID before promoting. For header-based tests send the configured header with your test requests.

## 4. Promote or roll back
- Promote: `aws cloudfront update-distribution-with-staging-config --id E1PRIMARY --staging-distribution-id E2STAGING --if-match <etag>`; the CLI reference describes the ETag format to pass for the primary and staging distributions.
- Roll back: disable the continuous deployment policy (`Enabled: false`) or detach it from the primary distribution.

## 5. Limits worth knowing
- Quotas: 20 staging distributions and 20 continuous deployment policies per account.
- CloudFront may send all requests to the primary distribution during peak CloudFront traffic hours, whatever the policy says, so treat weighted canaries as best effort.
- You cannot use continuous deployment with a distribution that supports HTTP/3.
- AWS WAF: you cannot associate a web ACL for the first time, or disassociate one, while continuous deployment is enabled; delete the policy first (this also deletes the staging distribution).
- With an S3 origin using OAC, update the bucket policy to allow the staging distribution.
- Check the continuous deployment documentation for other unsupported changes before relying on a test.

## Verify
- [ ] Header-based requests are visible in the staging distribution's logs.
- [ ] Weighted canary shows roughly the configured share in logs.
- [ ] Rollback by disabling the policy has been tested.

## Checked
2026-10-27. Documentation: Amazon CloudFront Developer Guide (continuous deployment, workflow, quotas and other considerations), read this date. Confirmed: quotas of 20 staging distributions and 20 policies, 15% maximum weight, stickiness idle 300-3600 s, peak-traffic behaviour, no continuous deployment with HTTP/3 (the draft said HTTP/3 requests go to primary), WAF ACL association restrictions, OAC bucket policy note. Confirmed from the CloudFront API model (botocore 2020-05-31): CopyDistribution parameters (Staging, PrimaryDistributionId, IfMatch, CallerReference), SingleWeight/SingleHeader types, UpdateDistributionWithStagingConfig parameters. Removed unconfirmed header-prefix rule, cookie stickiness, metric names, rollback timing, overwrite and IaC claims.
Method: documentation only; no commands were run.
