---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.lambda-power-tuning
name: lambda-power-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimization, lambda-power-tuning, aws-lambda, serverless-cost, memory-tuning, graviton, function-optimisation]
level: practitioner
status: docs-checked
description: "Tune AWS Lambda memory for cost: run AWS Lambda Power Tuning, read the cost and speed results, and use Compute Optimizer memory recommendations."
sources: ["https://github.com/alexcasalboni/aws-lambda-power-tuning", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html", "https://docs.aws.amazon.com/compute-optimizer/latest/ug/view-lambda-recommendations.html", "https://aws.amazon.com/lambda/pricing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function memory / power tuning

Lambda event functions are priced per request and by duration in GB-seconds, and you choose the
memory. CPU is allocated in proportion to memory: 128 MB to 10,240 MB in 1-MB steps, with the
equivalent of one vCPU at 1,769 MB. More memory can finish faster and cost the same or less.
Measure instead of guessing.

## AWS Lambda Power Tuning
Open-source (Apache-2.0) AWS Step Functions state machine. It invokes your function at several
memory values (128 MB to 10 GB, you choose), analyses the logs and suggests the best setting to
minimise cost and/or maximise speed. The function runs in your account and performs real HTTP
requests, SDK calls and cold starts, so use a safe test payload. Deploy it with AWS SAM CLI (needs
Docker) or another of the project's five IaC options. A basic input:
```json
{
  "lambdaARN": "arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:resize-image",
  "powerValues": [128, 256, 512, 1024],
  "num": 50,
  "payload": {}
}
```
Strategies are `cost`, `speed` and `balanced`. The output gives `results.power` (best memory),
`results.cost` and `results.duration` (averages per invocation), the state machine's own cost, and a
`results.stateMachine.visualization` URL for the cost/speed chart (data stays in the URL hash,
client-side). `results.stats` per power value appears only if `includeOutputResults` is truthy. See
the project README for the full list of input parameters.

## Reading the result
- CPU-intensive functions can become cheaper and faster with more memory: the README shows 35 s at
  128 MB falling to under 3 s at 1.5 GB while 14% cheaper, and another going from 2.4 s to 300 ms
  at 1 GB for the same average cost.
- Per AWS guidance, 128 MB suits only simple functions that transform and route events; functions
  using libraries, layers, S3 or EFS, and CPU-, network- or memory-bound functions can improve
  substantially with more memory.
- Monitor with CloudWatch and alarm when memory use nears the configured maximum.

## Further levers
- **AWS Compute Optimizer** gives Lambda memory recommendations (findings such as memory
  under-provisioned or over-provisioned) once you opt in, with estimated monthly savings. It
  supports only x86_64 functions.
- On-demand duration pricing tiers apply per architecture (x86 or Arm) and Region; the Lambda
  pricing page has the current rates, so compare both architectures with the tuner rather than
  assuming a saving.
- Set memory with `aws lambda update-function-configuration --function-name <name> --memory-size
  1024` or `MemorySize` in an AWS SAM template.

## Verify
- [ ] High-volume functions have a recorded tuning run and chosen memory.
- [ ] Cost per invocation tracked before/after.

## Checked

Method: docs-checked 2026-11-09 against the aws-lambda-power-tuning README, Lambda configuration-memory page, Compute Optimizer Lambda recommendations page and Lambda pricing page (searched, not read in full). Removed unconfirmed: the arm64 percentage, parallelInvocation/balancedWeight field names, I/O-bound and multi-threaded rules, provisioned concurrency and batching advice, Azure Functions and Cloud Run notes.
