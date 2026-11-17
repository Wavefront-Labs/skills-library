---
id: computing-software.qa-testing-engineering.test-automation.contract-testing-with-pact
name: contract-testing-with-pact
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [contract-testing, consumer-driven-contracts, pact, pact-broker, pacticipant, microservices-testing, provider-verification, can-i-deploy, api-contract, integration-testing, versioning, backward-compatibility, cdc]
level: advanced
status: verified
description: "Use consumer-driven contract testing (Pact) to catch breaking API changes between services before deploy, without running a full integrated E2E environment."
sources: ["https://docs.pact.io/", "https://martinfowler.com/articles/consumerDrivenContracts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contract testing with Pact

**Goal:** catch a breaking change between a service and its consumers at the point
the change is made — in each service's own CI — instead of discovering it in a
slow, flaky, shared integration environment after both sides have already deployed.

## 1. The problem this solves
Full E2E tests across microservices are slow, need every dependency running, and
fail for reasons unrelated to the contract (a flaky downstream service, test data
drift). They also only run *after* code exists on both sides — too late to stop
either team from shipping independently. Contract testing instead verifies, in
isolation, that provider and consumer agree on the shape of their interaction,
without either side's full implementation running against the other.

## 2. Consumer-driven: who writes the contract
The **consumer** (the service calling the API) writes a test against a **mock
provider**, describing the exact requests it will make and the responses it
needs:
```js
// pact-js 17: this object-literal style is the V2 API: `import { PactV2 as Pact, Matchers } from '@pact-foundation/pact'`
// (call `await provider.setup()` first, then `verify()` and `finalize()`); `Pact` itself is now the V4 fluent builder.
await provider.addInteraction({
  state: 'an order with id 1 exists',
  uponReceiving: 'a request for order 1',
  withRequest: { method: 'GET', path: '/orders/1' },
  willRespondWith: { status: 200, body: { id: 1, total: like(39.98) } },
})
```
Running this test generates a **pact file** (JSON) — the contract — capturing
only what the consumer actually uses. Matchers like `like()` assert type/shape,
not exact values, so the contract doesn't break on data that legitimately varies.

## 3. Provider verification
The pact file is published to a **Pact Broker**. The provider's CI pulls it and
replays the described requests against its *real* implementation, checking the
real responses satisfy the contract:
```
pact-verifier --hostname localhost --port 8080 \
  --broker-url $BROKER_URL --provider-name orders-service
```
(`pact-verifier` is the CLI in `@pact-foundation/pact-cli`, whose `--help` lists `-h/--hostname`, `-p/--port`, `-b/--broker-url`, `-n/--provider-name`, `-s/--state-change-url`; the older `pact-provider-verifier` with `--provider-base-url` is not in that package and `npx pact-provider-verifier` returns 404 on npm.) In Node the same check is `new Verifier({...}).verifyProvider()`, see the provider-verification skill.
A broken contract fails the **provider's** build, not the consumer's — which is
the point: the side making the breaking change finds out immediately, in their
own pipeline, before deploy.

## 4. can-i-deploy — the actual safety gate
The real value is the Broker's `can-i-deploy` check, run before each deploy:
```
pact-broker can-i-deploy --pacticipant orders-service --version $GIT_SHA \
  --to-environment production
```
This asks "has every consumer currently depending on this provider version
verified compatibility with what I'm about to deploy?" across *all* known
consumers, including ones the deploying team may not even know exist — the thing
a single team's local testing can't answer. Wire this as a required CI gate
before any production deploy of a service with contracts.

## 5. When contract testing isn't the right tool
It verifies *shape* compatibility, not business logic or performance — a provider
can pass every contract and still compute the wrong total. It also only covers
interactions the consumer actually exercises; an unused endpoint has no contract
and no protection. Don't replace integration/E2E tests entirely — contract tests
remove the *need to run everything together just to catch breaking API changes*,
not the need for any end-to-end confidence at all.

## Unconfirmed / notes
The V2 interaction above was run (pact-js 17.1.4, vitest) and wrote a pact file; no live Pact Broker was available, so broker-side behaviour (`can-i-deploy` results) is documented, not run. Matcher syntax (`like`, `term`,
`eachLike`) and CLI flags differ across Pact's JS/Python/JVM implementations —
confirm against the language binding in use.

## Verify
- [ ] Pact file generated from the consumer's actual test, not hand-written.
- [ ] Provider verification runs in the provider's own CI, independent of the consumer's.
- [ ] `can-i-deploy` is a required gate before production deploy, not advisory.
- [ ] Contract matchers use shape/type matching (`like`) where exact values would be brittle.
- [ ] Team understands contract tests don't replace all integration/E2E coverage.
