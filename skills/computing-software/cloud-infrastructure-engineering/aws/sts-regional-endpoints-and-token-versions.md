---
id: computing-software.cloud-infrastructure-engineering.aws.sts-regional-endpoints-and-token-versions
name: sts-regional-endpoints-and-token-versions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sts, sts-regional-endpoints, global-endpoint-tokens, opt-in-regions, session-tokens]
level: advanced
status: docs-checked
description: "Point SDKs and CLI at STS regional endpoints, manage global endpoint token versions for opt-in Regions, and activate or deactivate STS per Region."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_region-endpoints.html", "https://docs.aws.amazon.com/sdkref/latest/guide/feature-sts-regionalized-endpoints.html", "https://docs.aws.amazon.com/cli/latest/reference/iam/set-security-token-service-preferences.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STS regional endpoints and session token versions

**Goal:** STS calls stay in-Region (lower latency, no single-Region dependency) and tokens work in every Region you use.

## 1. Use regional endpoints
- Endpoint: `https://sts.<region>.amazonaws.com`. The legacy global endpoint is `sts.amazonaws.com`.
- SDK/CLI setting (shared config or env):
```ini
[default]
sts_regional_endpoints = regional
```
`export AWS_STS_REGIONAL_ENDPOINTS=regional`. Valid values are `legacy` (global endpoint) and
`regional`. Per the SDKs and Tools reference, AWS CLI v1, the AWS SDK for Java 1.x, JavaScript 2.x and
Go 1.x default to `legacy`; AWS CLI v2 has no setting and uses the regional endpoint; Boto3 defaults to
`regional`. Check the support table for your SDK.

## 2. Global endpoint token versions
- Version 1 tokens from the global endpoint are valid only in Regions enabled by default; the IAM console shows the current setting.
- To use them in Regions you must enable manually (for example `af-south-1`, `me-central-1`):
```bash
aws iam set-security-token-service-preferences --global-endpoint-token-version v2Token
aws iam get-account-summary --query 'SummaryMap.GlobalEndpointTokenVersion'
```
- v2 tokens are longer. Apps that store session tokens in fixed-width columns or headers can break;
  test before switching.
- Tokens from a regional endpoint are always valid in all Regions, which makes the preference moot.

## 3. Activate/deactivate STS per Region
IAM console, Account settings, Security Token Service, Endpoints: STS can be activated or deactivated
only in some Regions that are enabled by default (not us-east-1, the global endpoint or cn-north-1).
Regions you enable manually are activated automatically and cannot be deactivated. A request to a
Region where STS is not active for the account that would receive the credentials fails with the
`RegionDisabled` error (HTTP 403). Deactivate unused Regions only after checking CloudTrail
`eventSource=sts.amazonaws.com` by region.

## Gotchas
- CloudTrail logs regional-endpoint calls in that Region; calls to the global endpoint are logged to
  us-east-1, and events carry `endpointType` and `awsServingRegion` fields showing which endpoint and
  Region served them. The `aws:RequestedRegion` key is `us-east-1` for global-endpoint requests.
- Pin the endpoint explicitly in tools that cannot read the config: `aws sts get-caller-identity --region eu-west-1 --endpoint-url https://sts.eu-west-1.amazonaws.com`.

## Verify
- [ ] `aws sts get-caller-identity --debug 2>&1 | grep -o 'sts\.[a-z0-9-]*\.amazonaws.com'` shows the regional host.
- [ ] Workloads in opt-in Regions authenticate without `InvalidClientTokenId`.

## Checked

Checked 2026-10-27 against the IAM User Guide pages "AWS STS Regions and endpoints" and "Manage AWS STS in an AWS Region", the AWS SDKs and Tools Reference page on STS Regional endpoints, the AWS CLI 2.38.6 reference for `set-security-token-service-preferences` and the AWS STS API reference:
- `sts_regional_endpoints` and `AWS_STS_REGIONAL_ENDPOINTS` settings and the per-SDK defaults.
- `--global-endpoint-token-version` takes `v1Token` or `v2Token`; the current version appears as `GlobalEndpointTokenVersion` in `GetAccountSummary`; v1 tokens are valid only in default-enabled Regions, v2 in all Regions and are longer; regional-endpoint tokens are valid in all Regions.
- Which Regions can be activated or deactivated; global endpoint logging to us-east-1 and the `endpointType` and `awsServingRegion` fields; the `RegionDisabled` error.
Removed: the VPC endpoint hostname statement and the boto3 version remark, which the pages do not support.

Method: documentation only; no commands were run.
