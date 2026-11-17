---
id: computing-software.software-engineering.api-design.bola-object-level-authorization
name: bola-object-level-authorization
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, bola, idor, object-level-authorization, owasp-api-top-10, api-security]
level: practitioner
status: docs-checked
description: "Prevent broken object level authorization (OWASP API1:2023): check ownership on every object access, not just authentication, and test it with two accounts."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/", "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broken object level authorization (BOLA)

BOLA is OWASP API1:2023: the API accepts an object ID from the client (`GET /orders/1234`) and acts on it without checking the caller may perform that action on that object. The user is meant to reach the endpoint; the violation is at the object level, by manipulating the ID. IDs can be integers, UUIDs or strings and appear in the path, query string, headers or body.

## Fix pattern
OWASP: every function that uses client input to access a record must check that the logged-in user may perform the requested action on that record, using an authorization mechanism based on user policies and hierarchy. A practical shape is to authorize at the data-access layer so no handler can forget:
```python
def get_order(user, order_id):
    row = db.query("SELECT * FROM orders WHERE id = %s AND tenant_id = %s",
                   order_id, user.tenant_id)
    if row is None:
        raise NotFound()   # same response as "does not exist"
    if not policy.allows(user, "read", row):
        raise NotFound()
    return row
```
- Scope every query by the caller's tenant or owner, not by ID alone.
- Comparing the session user ID (for example from the JWT) with an ID parameter is not a sufficient fix; OWASP says it covers only a small subset of cases. Use a policy check on the record.
- Apply to every verb, including destructive ones: in OWASP scenario #3 a GraphQL delete mutation took a document ID and deleted it without any permission check.
- Check nested paths (`/users/{id}/invoices/{invoice_id}`) against both IDs.
- Prefer random, unpredictable GUIDs as record IDs, as OWASP recommends; treat this as defence in depth, not a substitute for the check.
- Write tests for the authorization mechanism and do not deploy changes that make them fail.

## Gotchas
- Returning 404 rather than 403 for other tenants' objects avoids confirming existence (a design choice, not an OWASP rule).
- Bulk and search endpoints leak the same way: filter the result set, not only single GETs.
- A privileged endpoint reachable by the wrong user is BFLA, not BOLA; see the bfla skill.

Verify: create two users A and B with separate data; replay each of A's object requests using B's token and confirm every one returns 404/403. Automate this as a test over every route in the OpenAPI document.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API1 (definition, session-ID comparison caveat, three scenarios, prevention list). The Authorization Cheat Sheet was not used for any claim kept here. Removed: the statement that the OWASP page says random IDs do not replace checks (the page only recommends random GUIDs), ULID as an example, and the claim that every GraphQL resolver needs a check (the page shows a mutation lacking one). The Python example is illustrative and was not run.
Method: documentation only; no commands were run.
