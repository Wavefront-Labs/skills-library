---
id: computing-software.cybersecurity-defensive.cloud-security.serverless-function-security
name: serverless-function-security
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-workload-protection, serverless-security, aws-lambda, azure-functions, cloud-functions, function-iam-role, event-injection, function-url]
level: practitioner
status: draft
description: "Secure serverless functions: least-privilege execution roles, event input validation, secrets handling, network and URL exposure, dependencies and logging."
sources: ["OWASP Serverless Top 10", "AWS Lambda security documentation (execution role, resource-based policies, function URLs)", "CSA Top Threats to Serverless (Serverless Application Security guidance)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serverless function security

**Goal:** each function can do only its job, cannot be invoked by the wrong caller, and treats
every event as untrusted input.

## Identity and permissions
- One execution role per function, scoped to exact resources and actions (no `s3:*` on `*`).
  Use IAM Access Analyzer policy generation from CloudTrail activity to tighten.
- Resource-based policies (who can invoke): restrict `lambda:InvokeFunction` to specific
  services with `SourceArn`/`SourceAccount` conditions to prevent confused-deputy invocation.
- Function URLs: `AuthType AWS_IAM` unless public by design; public URLs need app-level auth and rate limiting.

## Input
Events come from many sources (API Gateway, S3 object keys, SQS, SNS, email): validate and
encode as you would for web input. Event injection (e.g. a crafted S3 object name fed into a
shell command or SQL) is the serverless form of injection.

## Secrets
Retrieve from Secrets Manager/Key Vault at cold start (with caching), not plaintext environment
variables (visible to anyone with `GetFunctionConfiguration`). If env vars are used, encrypt with a CMK.

## Network
- Functions in a VPC only when they need private resources; egress control via NAT + firewall or VPC endpoints.
- Concurrency limits (reserved concurrency) to cap cost/DoS blast radius.

## Code and dependencies
- Small deployment packages; scan dependencies and layers (SCA) in CI; sign code (AWS Signer code signing configs) and enforce signature validation.
- Timeouts as short as practical.

## Logging and detection
- Structured logs to CloudWatch/Log Analytics; CloudTrail data events for Lambda invoke where needed.
- GuardDuty Lambda Protection monitors network activity of functions.

## Gotchas
- Shared execution roles across functions give each function the union of permissions.
- `/tmp` and global state persist between warm invocations: do not leave sensitive data there across tenants.
- Wildcard triggers (any SNS topic) let others invoke your function.

## Verify
- [ ] Each function's role reviewed with Access Analyzer unused-permissions findings addressed.
- [ ] Invocation by an unauthorised principal fails.
