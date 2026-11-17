---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-versions-aliases-and-traffic-shifting
name: lambda-versions-aliases-and-traffic-shifting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, lambda-versions, lambda-alias, alias-routing, weighted-alias, canary-deployment, rollback]
level: practitioner
status: docs-checked
description: "Release Lambda safely: publishing versions, aliases as stable ARNs, weighted alias routing for canaries and its rules, finding the executed version, and rollback."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html", "https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda versions, aliases and traffic shifting

## 1. Concepts
- `$LATEST` is the unpublished, mutable version. A published **version** (`:7`) is a snapshot of code and
  configuration. An **alias** (`:live`) is a named pointer to a version, optionally split with a second version.
- Point triggers, API integrations and permissions at an alias ARN so the target can move without edits.

## 2. Release flow
```bash
aws lambda update-function-code --function-name orders --zip-file fileb://fn.zip
aws lambda wait function-updated --function-name orders
V=$(aws lambda publish-version --function-name orders --description "git $(git rev-parse --short HEAD)" --query Version --output text)
# canary: alias keeps its function-version, new version gets 10%
aws lambda update-alias --function-name orders --name live --routing-config 'AdditionalVersionWeights={"'$V'"=0.1}'
# promote: point the alias at the new version; this also resets the routing configuration
aws lambda update-alias --function-name orders --name live --function-version $V --routing-config AdditionalVersionWeights={}
# rollback = point back at the previous version (replace OLD_VERSION)
aws lambda update-alias --function-name orders --name live --function-version OLD_VERSION --routing-config AdditionalVersionWeights={}
```
The first version keeps the residual weight (10% to the additional version leaves 90% on the alias's main version).

## 3. Weighted alias rules
- An alias can point to at most two versions, and both must be **published** (not `$LATEST`).
- Both versions must have the same execution role and the same dead-letter queue configuration (or none).
- Routing is probabilistic: at low traffic the real split varies widely from the configured weights.
- With provisioned concurrency, raise it while routing is active to avoid spillover invocations.
- To see which version ran: the `START` log line includes `Version`; alias invocation metrics have an
  `ExecutedVersion` dimension; synchronous responses carry an `x-amz-executed-version` header.

## 4. Automate
AWS SAM `AutoPublishAlias: live` with `DeploymentPreference: Type: Linear10PercentEvery2Minutes` makes SAM create
an alias, a CodeDeploy application and deployment group, publish a version when the function changes and shift
traffic gradually with rollback handled by CodeDeploy (other predefined configurations are in the CodeDeploy
docs).

## Gotchas
- Code storage for uploaded zip functions and layers is 300 GB per Region, and each function version consumes
  storage; prune versions that no alias references (keep a few for rollback).
- Provisioned concurrency applies to versions and aliases; the amount on versions and aliases counts against the
  function's reserved concurrency when both are set.

## Verify
- [ ] `aws lambda get-alias --function-name orders --name live` shows the intended version and weights.
- [ ] During the canary, `ExecutedVersion` metrics show the expected share on the new version.
- [ ] Rollback restores the old version (test once in non-prod).

## Checked
Date 2026-10-23. Lambda Developer Guide alias routing, quotas and concurrency pages. Confirmed: two-version limit, published-only,
same role and DLQ rules, routing-config CLI syntax and residual weight, `update-alias` resets routing,
ExecutedVersion dimension, `x-amz-executed-version` header, SAM `AutoPublishAlias` and
`Linear10PercentEvery2Minutes` behaviour, 300 GB code storage. Wrong in the old text: the code storage quota
was given as 75 GB (documented: 300 GB), and `Canary10Percent5Minutes` was presented without the documented
example type. Removed unconfirmed CDK construct names and the signing-compatibility remark.
Method: documentation only; no commands were run.
