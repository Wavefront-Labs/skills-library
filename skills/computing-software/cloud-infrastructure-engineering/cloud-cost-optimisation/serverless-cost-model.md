---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.serverless-cost-model
name: serverless-cost-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-aware-architecture, serverless-cost-model, lambda-cost, cloud-run-cost, azure-functions-cost, break-even-analysis, gb-seconds, provisioned-concurrency, memory-tuning]
level: practitioner
status: draft
description: "Compare serverless vs provisioned compute cost: GB-second maths, break-even utilisation, memory power-tuning, hidden per-request costs, when to move off."
sources: ["https://aws.amazon.com/lambda/pricing/", "https://github.com/alexcasalboni/aws-lambda-power-tuning", "https://cloud.google.com/run/pricing", "https://www.finops.org/framework/capabilities/architecting-for-cloud/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serverless vs provisioned cost crossover

## The maths (function-as-a-service)
Cost ≈ requests × request_price + requests × duration_s × memory_GB × GB-s_price (+ free tier).
Compare to a container/VM fleet that handles the same peak with headroom, running 24/7.

Rules of thumb:
- **Spiky / low average utilisation** (idle most of the day): serverless wins by a lot.
- **Steady high throughput** (a fleet would be > ~40-60% utilised all day): containers/VMs with
  commitments usually win. Compute your own break-even with real numbers.

## Hidden per-request costs
API Gateway per-million requests (HTTP APIs much cheaper than REST APIs on AWS), CloudWatch log
ingestion per invocation, X-Ray traces, NAT for VPC functions, provisioned concurrency billed
even when idle.

## Optimise within serverless
1. **Memory tuning**: CPU scales with memory; more memory can be cheaper if duration drops.
   Run AWS Lambda Power Tuning (Step Functions state machine) to find the cost/speed optimum.
2. **ARM (Graviton)** for Lambda is cheaper per GB-s.
3. Cut duration: reuse connections outside the handler, avoid waiting on I/O (synchronous calls to slow APIs bill the wait).
4. Batch events (SQS batch size, Kinesis batch window).
5. Log less (set log level; use log retention).
6. Cloud Run: request-based vs instance-based billing; concurrency > 1 per instance amortises cost;
   min instances cost money while idle.

## Verify
- [ ] Break-even sheet for top serverless workloads with current traffic.
- [ ] Power-tuning results applied to the top 10 functions by cost.
