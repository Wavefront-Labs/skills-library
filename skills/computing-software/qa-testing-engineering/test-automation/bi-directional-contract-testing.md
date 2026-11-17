---
id: computing-software.qa-testing-engineering.test-automation.bi-directional-contract-testing
name: bi-directional-contract-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [bi-directional-contracts, contract-testing, openapi, pactflow, pact, can-i-deploy]
level: advanced
status: gated
description: "Run bi-directional contract testing: publish provider OpenAPI with verification evidence, consumer pacts or mocks, cross-contract comparison and can-i-deploy gating."
sources:
  - https://docs.pact.io/
  - https://github.com/pact-foundation/pact-broker-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bi-directional contract testing with OpenAPI

**Goal:** contract testing without the provider replaying consumer pacts: the provider publishes its OpenAPI spec plus proof it conforms, consumers publish what they use, and the broker checks compatibility (a PactFlow feature).

## How it works
1. **Provider:** tests its implementation against its own OpenAPI document using any tool of its choice, then publishes the spec and the verification result.
2. **Consumer:** publishes a contract describing the requests and responses it relies on: a Pact file from Pact tests, or a contract generated from mocks.
3. **PactFlow** statically compares each consumer contract against the provider spec: every consumer interaction must be a valid request and response under the OpenAPI (gated: unconfirmed, source is paywalled or blocked).
4. **can-i-deploy** gates both sides as in standard Pact.

```bash
pact-broker-cli pactflow publish-provider-contract openapi.yaml \
  --provider orders-api --provider-app-version $GIT_SHA --branch $GIT_BRANCH \
  --content-type application/yaml \
  --verification-exit-code=0 --verification-results results.txt \
  --verification-results-content-type text/plain --verifier schemathesis
pact-broker-cli can-i-deploy --pacticipant orders-api --version $GIT_SHA --to-environment production
```
(Both commands are subcommands of `pact-broker-cli`. Pass the broker with `--broker-base-url` or `PACT_BROKER_BASE_URL`, plus a token. `--content-type` is the contract's media type; `--verification-exit-code` can replace `--verification-success`. `can-i-deploy` can wait for slow verifications with `--retry-while-unknown` and `--retry-interval`.)

## Trade-offs
- **Pros:** providers keep their own tests, easy adoption with existing OpenAPI and mocks, works for teams that cannot run consumer pacts.
- **Cons:** only as good as the spec and the provider's conformance testing; loose specs (nothing marked required, undeclared fields allowed) let real breaks through.

## Practice
- Make the provider spec strict and generated from or validated against code.
- Ensure consumer mocks are realistic: a mock that matches the spec but not reality defeats the point.

## Verify
A consumer contract using a field absent from the provider spec makes can-i-deploy fail, and the provider's published verification comes from a real conformance run.

## Checked
2026-10-31. Confirmed against the pact-broker-cli README: `pactflow publish-provider-contract` exists with `--provider`, `--provider-app-version`, `--branch`, `--content-type`, `--verification-exit-code`, `--verification-results`, `--verification-results-content-type` and `--verifier`; `can-i-deploy` takes `--pacticipant`, `--version` and `--to-environment`; the retry flags. Gated: the PactFlow static comparison in step 3, because the PactFlow bi-directional page is no longer served at its old URL (404). Removed: named verification tools and mock adapters that could not be confirmed, the old `pactflow` / `pact-broker` binary names, and the `additionalProperties` spec-looseness example (not in the fetched pages).
Method: documentation only; no commands were run.
