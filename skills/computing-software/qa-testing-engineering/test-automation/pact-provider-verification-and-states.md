---
id: computing-software.qa-testing-engineering.test-automation.pact-provider-verification-and-states
name: pact-provider-verification-and-states
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [provider-states, provider-verification, pact, contract-testing, can-i-deploy, pact-broker-webhooks, pact-pending-wip]
level: practitioner
status: verified
description: "Verify Pact contracts on the provider: state handlers that seed data, consumer version selectors, pending and WIP pacts, webhooks, and publishing verification results."
sources:
  - https://docs.pact.io/implementation_guides/javascript/docs/provider
  - https://docs.pact.io/getting_started/provider_states
  - https://docs.pact.io/pact_broker/advanced_topics/consumer_version_selectors
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Provider verification and provider states

**Goal:** the provider build proves it satisfies every consumer contract that matters for deployment.

## Provider states
Each interaction's `given('order 42 exists', {id: 42})` maps to a handler that sets up data on the real provider (via repository, test DB or stubbed downstream).
```ts
const opts = {
  provider: 'order-api',
  providerBaseUrl: 'http://localhost:8080',
  pactBrokerUrl: process.env.PACT_BROKER_URL,
  pactBrokerToken: process.env.PACT_BROKER_TOKEN,
  consumerVersionSelectors: [{ mainBranch: true }, { deployedOrReleased: true }, { matchingBranch: true }],
  enablePending: true,
  includeWipPactsSince: '2026-01-01',
  publishVerificationResult: process.env.CI === 'true',
  providerVersion: process.env.GIT_SHA,
  providerVersionBranch: process.env.GIT_BRANCH,
  stateHandlers: {
    'order 42 exists': async (params) => { await db.orders.insert(orderFactory({ id: params.id })); },
    'no orders exist': async () => { await db.orders.truncate(); },
  },
  requestFilter: (req, res, next) => { req.headers.authorization = `Bearer ${testToken()}`; next(); },
};
await new Verifier(opts).verifyProvider();
```
Run locally (pact 17.1.4, pact file from the consumer skill, `pactUrls: ['./pacts/web-shop-order-api.json']` in place of the broker options, a stub provider on a local port): `Verifier.verifyProvider()` called the `order 42 exists` state handler, `requestFilter` injected the Authorization header, and the matchers accepted a response with a different status and qty than the example. The selector keys (`mainBranch`, `deployedOrReleased`, `matchingBranch`) and the options `enablePending`, `includeWipPactsSince`, `publishVerificationResult`, `providerVersionBranch` exist in pact-core's `VerifierOptions` types; broker-side behaviour was not run (no broker). Set `PACT_DO_NOT_TRACK=true` to stop the anonymous usage-statistics notice.
JVM: `@Provider("order-api")`, `@PactBroker`, `@State("order 42 exists")` methods, `@TestTemplate` with `PactVerificationInvocationContextProvider`.

## Key settings
- **Consumer version selectors**: verify main branch, what is deployed/released, and same-named feature branches.
- **Pending pacts**: new consumer expectations do not fail the provider build until verified once.
- **WIP pacts**: also verify recent feature-branch pacts without failing.
- **Webhook**: broker triggers provider verification when a consumer publishes a changed pact (`contract_requiring_verification_published`).

## Gotchas
- States that call real downstream services make verification flaky; stub downstream in the provider test.
- Auth: inject valid test tokens with a request filter rather than disabling auth in code paths under test.
- State names are a shared API between teams; agree naming and keep them stable.

## Verify
Provider CI publishes verification results per SHA, can-i-deploy for both sides is green, and a breaking provider change fails verification.
