---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-memory-sizing-and-power-tuning
name: lambda-memory-sizing-and-power-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, power-tuning, memory-sizing, lambda-cost, arm64, compute-optimizer, performance]
level: practitioner
status: docs-checked
description: "Right-size Lambda memory: memory-to-CPU scaling, the AWS Lambda Power Tuning tool, arm64 vs x86 comparison, and Compute Optimizer recommendations and their limits."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html", "https://github.com/alexcasalboni/aws-lambda-power-tuning", "https://docs.aws.amazon.com/compute-optimizer/latest/ug/view-lambda-recommendations.html", "https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda memory sizing with Power Tuning

## 1. Why memory is the CPU knob
Lambda allocates CPU in proportion to configured memory (128 MB to 10,240 MB, 1 MB steps); at **1,769 MB** a
function has the equivalent of one vCPU. Memory is the principal performance lever and 128 MB is the default and
lowest setting. Cost scales with memory x duration, so a CPU-bound function can sometimes run faster at higher
memory for a similar cost. If a function is CPU, network or memory-bound, more memory can dramatically improve
performance; functions waiting on I/O gain less.
```bash
aws lambda update-function-configuration --function-name my-function --memory-size 1024
```

## 2. Run Power Tuning
AWS documents the open source AWS Lambda Power Tuning tool: it uses AWS Step Functions to run concurrent
versions of your function at different memory settings and measures performance. The function runs in your
account, making live HTTP calls and SDK calls, so point it at a test alias or environment (side effects are real).
Follow the repository README for deployment options and the exact input fields (the state machine takes the
function ARN, the list of memory values to try, the number of invocations per value, a payload and an
optimisation strategy). It can also run in CI to measure new functions.

## 3. Architecture
Repeat the test on an arm64 copy (see the arm64 skill). Change architecture with `update-function-code
--architectures arm64` once layers, extensions and native dependencies support it.

## 4. Ongoing
- Monitor with CloudWatch and alarm when memory consumption approaches the configured maximum; use the
  `Max Memory Used` field in the invocation REPORT log line to see how close you are.
- AWS Compute Optimizer produces Lambda memory recommendations (opt-in, admin permissions; refreshed daily
  from the last 14 days of metrics). Limits: it supports only x86_64 functions, and functions configured above
  1,792 MB are marked Unavailable (Inconclusive). Accept recommendations in the Lambda console under General
  configuration.

## Gotchas
- Downstream throttling (DB, API) during parallel tuning distorts results.
- Extensions and the function compete for the same CPU, so low memory also slows init and extension work.

## Verify
- [ ] Power Tuning result saved with the chosen setting and its cost/duration numbers.
- [ ] After the change, p95 duration and monthly cost moved in the expected direction.
- [ ] `Max Memory Used` stays comfortably below configured memory.

## Checked
Date 2026-10-23. Lambda Developer Guide memory and quotas pages, Compute Optimizer user guide (Lambda recommendations page).
Confirmed: memory range, 1,769 MB = one vCPU, memory as the principal lever, Power Tuning description (Step
Functions, live calls), `--memory-size` CLI, Compute Optimizer 14-day window, daily refresh, x86_64 only,
1,792 MB Inconclusive. Removed unconfirmed claims: "up to 6 vCPUs at 10 GB", "about 20% cheaper arm64", the
Power Tuning input JSON and strategy names (the README page could not be fetched), the SAR app name, the
`num >= 50` advice and the 80% memory rule of thumb.
Method: documentation only; no commands were run.
