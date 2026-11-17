---
id: computing-software.cloud-infrastructure-engineering.aws.xray-cost-control-sampling-and-encryption
name: xray-cost-control-sampling-and-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, x-ray, xray-cost, sampling-rules, xray-encryption, kms, transaction-search]
level: practitioner
status: docs-checked
description: "Keep X-Ray affordable and compliant: how traces are billed, sampling rule design with reservoir and rate, Transaction Search trade-offs, and KMS encryption of trace data."
sources: ["https://docs.aws.amazon.com/xray/latest/devguide/xray-console-sampling.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-console-encryption.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Transaction-Search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X-Ray cost control and trace encryption

## What costs money
- X-Ray bills for traces recorded and for traces retrieved or scanned; Insights, Transaction
  Search and KMS key use are priced separately. Read the current X-Ray and CloudWatch pricing
  pages for the rates.
- Volume is driven by sampling: every sampled request is a trace, whatever its size.

## Sampling rules
Default behaviour: the **reservoir is 1 request per second**, plus **5%** of additional requests.
In the API, `FixedRate` is a fraction between 0 and 1 (0.05 = 5%); in the console it is a percentage.
```bash
aws xray create-sampling-rule --sampling-rule '{
  "RuleName":"health-checks-off","Priority":10,"FixedRate":0,"ReservoirSize":0,
  "ServiceName":"*","ServiceType":"*","Host":"*","HTTPMethod":"GET","URLPath":"/health*",
  "ResourceARN":"*","Version":1}'
aws xray create-sampling-rule --sampling-rule '{
  "RuleName":"checkout-more","Priority":20,"FixedRate":0.2,"ReservoirSize":5,
  "ServiceName":"orders-api","ServiceType":"*","Host":"*","HTTPMethod":"POST","URLPath":"/checkout",
  "ResourceARN":"*","Version":1}'
```
- Priority is 1-9999; rules are evaluated in ascending order and the first match decides.
  Reservoir is a per-second count shared by all services using the rule (X-Ray assigns each
  instance a quota); `FixedRate` applies after the reservoir.
- Exclude health checks and high-volume, low-value paths first; raise sampling for critical flows.
- Define rules in the X-Ray service rather than in local JSON files: each instance of a
  locally configured service samples independently, so reservoirs add up, and changes need a redeploy.
- Sampling is parent-based: a rule only takes effect where no sampling decision exists yet
  (the entry point or a new asynchronous trace). A downstream service honours the upstream
  decision, so put the rule on the root service.
- The X-Ray SDK only uses rules whose `ResourceARN` is `*` and ignores rules with `Attributes`.

## Transaction Search
Sends 100% of spans to CloudWatch Logs (`aws/spans`) and indexes a configurable percentage as trace
summaries in X-Ray. Good for "find every failed checkout"; it is billed through CloudWatch Logs
and X-Ray indexing (see the Pricing section of the Transaction Search page), so choose the
indexing percentage deliberately.

## Encryption
- X-Ray always encrypts traces at rest. `aws/xray` is the AWS managed key (audit key use in
  CloudTrail); a customer managed key lets you manage access and rotation. Symmetric keys only.
  KMS charges apply when X-Ray uses a KMS key. Example with a customer managed key:
```bash
aws xray put-encryption-config --type KMS --key-id alias/xray
aws xray get-encryption-config        # Status UPDATING -> ACTIVE
```
- You need user-level access to the key to configure it and to view encrypted traces. While a
  change is processed X-Ray may use a mix of old and new settings, and existing data is not
  re-encrypted. If X-Ray loses access to the key (for example it is disabled) it stops storing data.
- Insights notifications go to EventBridge, which does not support customer managed keys.
- Do not put PII in annotations/metadata; traces are visible to anyone with `xray:BatchGetTraces`.

## Verify
- [ ] `aws xray get-sampling-statistic-summaries` shows sampled counts in line with plan.
- [ ] Monthly X-Ray cost tracked in Cost Explorer (service AWS X-Ray) with an anomaly monitor.
- [ ] Encryption config ACTIVE with the CMK where required.

## Checked

2026-10-27, AWS documentation (current release as read on that date). X-Ray Developer Guide sampling and encryption pages, CloudWatch Transaction Search page, botocore xray 2016-04-12 model. Fixed: sampling is parent-based so rules apply at the root service, aws/xray is the AWS managed key (not an AWS-owned default), existing data is not re-encrypted, priority range 1-9999, FixedRate is a 0-1 fraction in the API. Confirmed: default 1 request per second plus 5 percent, EncryptionType NONE/KMS, EncryptionStatus UPDATING/ACTIVE, aws/spans log group, GetSamplingStatisticSummaries. Removed billing structure claims and the unsourced Lambda sampling remark.
Method: documentation only; no commands were run.
