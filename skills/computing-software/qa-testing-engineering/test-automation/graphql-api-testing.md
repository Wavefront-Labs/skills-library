---
id: computing-software.qa-testing-engineering.test-automation.graphql-api-testing
name: graphql-api-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [graphql-testing, graphql, api-testing, schema-introspection, query-depth]
level: practitioner
status: verified
description: "Test GraphQL APIs: queries and mutations with variables, 200-with-errors assertions, schema diffs, field-level authorization, depth limits and N+1 checks."
sources:
  - https://graphql.org/learn/
  - https://spec.graphql.org/October2021/#sec-Response
  - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/01-Testing_GraphQL
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL API testing

## Basics
Everything is `POST /graphql` with JSON `{ "query", "variables", "operationName" }`. Status is usually **200 even on errors**: assert on the `errors` array, not just the status.

```python
def gql(client, query, variables=None, token=None):
    r = client.post("/graphql", json={"query": query, "variables": variables or {}},
                    headers={"Authorization": f"Bearer {token}"} if token else {})
    assert r.status_code == 200
    return r.json()

def test_order_query(client, user_token):
    body = gql(client, """
      query Order($id: ID!) { order(id: $id) { id status total { amount currency } } }
    """, {"id": "ord_1"}, user_token)
    assert "errors" not in body
    assert body["data"]["order"]["status"] == "PAID"

def test_invalid_input_error_shape(client, user_token):
    body = gql(client, "mutation { addItem(sku: \"\", qty: -1) { id } }", token=user_token)
    err = body["errors"][0]
    assert err["extensions"]["code"] == "BAD_USER_INPUT"
    assert body["data"] is None or body["data"]["addItem"] is None
```
Always use variables, not string interpolation, in tests (same as production clients).

Run against a Strawberry GraphQL (FastAPI) server through Starlette's TestClient: the tests above passed. Observed: an unknown field (`{ nope }`) and a syntax error both returned HTTP 200 with an `errors` array (Strawberry's behaviour on the plain `application/json` path; other servers differ, so assert on what yours does). `extensions.code` values such as `BAD_USER_INPUT` come from the server (Apollo Server uses that name); in this run the resolver set it explicitly, so confirm the code your server emits.

## What to cover
- **Schema contract:** snapshot the SDL (`get_schema`/introspection) and diff in CI; breaking changes (removed fields, nullability changes) caught with tools like GraphQL Inspector (`graphql-inspector diff old.graphql new.graphql` reported "Field owner was removed from object type Order" and "Field Order.status changed type from String! to String", printed `Detected 2 breaking changes` and exited 1).
- **Partial success:** one resolver failing returns `data` with nulls plus `errors` with `path`; test the client-visible shape (observed: `{'data': {'order': {'id': '1', 'secret': None}}, 'errors': [{'path': ['order', 'secret'], ...}]}`).
- **Authorization per field/object:** a user querying another user's `order(id:)` or a nested `customer { email }` field must be denied, not just the top-level query.
- **Introspection in production:** usually disabled; test that it is (with Strawberry's `DisableIntrospection` extension a `__schema` query returned `data: null` and an "introspection has been disabled" error).
- **Abuse limits:** deeply nested queries, aliases multiplying expensive fields, batch arrays; expect depth/complexity limit errors (Strawberry's `QueryDepthLimiter(max_depth=3)` rejected a 4-level query with "exceeds maximum operation depth of 3").
- **Performance:** N+1 resolver calls (count DB queries per request; DataLoader batching), persisted queries.

## Tools
Postman/Insomnia GraphQL support, `graphql-request`/`gql` clients in tests, Schemathesis GraphQL mode for property-based fuzzing of a schema (`schemathesis.graphql.from_asgi("/graphql", app)` with `@schema.parametrize()` generated cases and failed on the server errors it found), k6 for load (POST bodies).

## Gotchas
- Snapshotting whole responses breaks on field additions; assert on the fields under test.
- Caching layers keyed on URL don't apply to POST GraphQL; test persisted-query/GET caching if used.

## Verify
Removing a field or making it non-null fails the schema diff check; cross-user queries return authorization errors.
