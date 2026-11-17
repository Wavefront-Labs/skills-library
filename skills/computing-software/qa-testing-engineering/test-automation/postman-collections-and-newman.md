---
id: computing-software.qa-testing-engineering.test-automation.postman-collections-and-newman
name: postman-collections-and-newman
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [postman, newman, api-testing, ci-integration, api-collections]
level: practitioner
status: verified
description: "Build API test collections in Postman with pm.test scripts, environments and data files, and run them headless in CI with Newman and JUnit or HTML reporters."
sources:
  - https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/
  - https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/
  - https://github.com/postmanlabs/newman
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API collections with Postman and Newman

**Goal:** a versioned API test collection that runs the same way in the app and in CI.

## Test scripts (Post-response tab)
```js
pm.test('status is 201', () => pm.response.to.have.status(201));
pm.test('order has id and PENDING status', () => {
  const body = pm.response.json();
  pm.expect(body.id).to.be.a('number');
  pm.expect(body.status).to.eql('PENDING');
  pm.collectionVariables.set('orderId', body.id);     // chain to next request
});
pm.test('responds under 500 ms', () => pm.expect(pm.response.responseTime).to.be.below(500));
```
Schema check: `pm.response.to.have.jsonSchema(schema)`.
Pre-request scripts for auth tokens (`pm.sendRequest` to the token endpoint, cache in an environment variable with expiry).

## Variables and environments
Scopes: global < collection < environment < data < local. Keep `baseUrl`, credentials in environments (`staging.postman_environment.json`); secrets as secret-type values injected in CI, never committed.

## Data-driven runs
CSV/JSON file with one row per iteration, referenced as `{{columnName}}` or `pm.iterationData.get('sku')`.

## Newman in CI
```bash
npm i -g newman newman-reporter-htmlextra
newman run collections/orders.postman_collection.json \
  -e envs/staging.postman_environment.json \
  --env-var "token=$API_TOKEN" -d data/orders.csv \
  --reporters cli,junit,htmlextra --reporter-junit-export reports/newman.xml \
  --bail --timeout-request 10000
```
Exit code is non-zero on failed tests (Newman 6.2.3 run against a local stub: all five assertions per iteration, JUnit and htmlextra reports written, `--env-var` overrode the environment file, a wrong `status` gave exit code 1 and `--bail` stopped the run). `--help` lists `--env-var`, `--bail`, `--timeout-request`. Postman docs list variable scopes from broadest to narrowest as global, collection, environment, data, local, and the narrowest wins. Postman CLI (`postman collection run`) is the newer official alternative tied to Postman cloud.

## Organising
Folders per resource; requests ordered for flows; collection exported to git (or synced via Postman's git integration) and reviewed like code.

## Gotchas
- Tests that depend on request order break when someone runs a single request; set up state in pre-request scripts or folder-level flows.
- Exported collections may contain tokens; scrub before commit.

## Verify
Newman runs green in CI with a JUnit report, the collection lives in version control, and a broken response field fails a named test.
