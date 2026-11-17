---
id: computing-software.software-engineering.api-design.consumer-driven-contract-testing-with-pact
name: consumer-driven-contract-testing-with-pact
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-contracts, pact, contract-testing, consumer-driven-contracts, pact-broker, can-i-deploy]
level: practitioner
status: draft
description: "Run consumer-driven contract tests with Pact: consumer tests generate pacts, provider verification with states, Pact Broker, can-i-deploy gates and webhooks in CI."
sources:
  - https://docs.pact.io/
  - https://docs.pact.io/pact_broker/can_i_deploy
  - https://docs.pact.io/getting_started/provider_states
  - https://martinfowler.com/articles/consumerDrivenContracts.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Consumer-driven contract testing with Pact

Contract tests check that a provider API satisfies what each consumer actually uses, without spinning up the whole system for end-to-end tests.

## Flow
1. **Consumer test:** the consumer's code runs against a Pact mock server; the test declares expected interactions. Running it writes a pact file (JSON contract).
2. **Publish** the pact to a Pact Broker (self-hosted `pactfoundation/pact-broker` or PactFlow), tagged with consumer version (git SHA) and branch.
3. **Provider verification:** the provider's CI fetches relevant pacts and replays each interaction against the real provider (running locally with stubbed downstreams), checking responses match.
4. **can-i-deploy** queries the broker before each deploy: is this version compatible with what is deployed in the target environment?
5. **record-deployment** tells the broker what is live where.

## Consumer test (pact-js v4 style)
```javascript
const provider = new PactV4({ consumer: "web-app", provider: "orders-api" });
it("gets an order", () =>
  provider.addInteraction()
    .given("order 42 exists")                               // provider state
    .uponReceiving("a request for order 42")
    .withRequest("GET", "/orders/42", b => b.headers({ Accept: "application/json" }))
    .willRespondWith(200, b => b.jsonBody({
      id: like("42"), status: regex("open|shipped", "open"), total: decimal(12.5),
    }))
    .executeTest(async (mock) => {
      const order = await new OrdersClient(mock.url).get("42");
      expect(order.status).toBe("open");
    }));
```
Use matchers (`like`, `eachLike`, `regex`) so the contract checks types and shapes, not exact example values. Only include fields the consumer reads.

## Provider verification
```javascript
new Verifier({
  providerBaseUrl: "http://localhost:8080",
  pactBrokerUrl: process.env.PACT_BROKER_URL,
  provider: "orders-api",
  consumerVersionSelectors: [{ mainBranch: true }, { deployedOrReleased: true }],
  enablePending: true,                         // new consumer expectations do not break provider builds
  publishVerificationResult: process.env.CI === "true",
  providerVersion: process.env.GIT_SHA, providerVersionBranch: process.env.GIT_BRANCH,
  stateHandlers: { "order 42 exists": () => db.insertOrder({ id: "42", status: "open" }) },
}).verifyProvider();
```

## CI gates
```bash
pact-broker can-i-deploy --pacticipant orders-api --version $GIT_SHA --to-environment production
pact-broker record-deployment --pacticipant orders-api --version $GIT_SHA --environment production
```
Broker webhooks trigger provider verification when a consumer publishes a changed pact.

## Limits
Pact covers request/response shape and semantics consumers rely on, not performance or full business correctness. Use it for services you own on both sides; for public APIs with unknown consumers, use OpenAPI schema validation and breaking-change diffing (oasdiff) instead. Message pacts cover async events.

## Verify
- [ ] Removing a field a consumer uses fails provider verification.
- [ ] Deploy pipeline blocks when can-i-deploy returns false.
