---
id: computing-software.qa-testing-engineering.test-automation.authorization-and-idor-testing
name: authorization-and-idor-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [authorization-testing, idor, access-control-testing, security-testing, bola, owasp-wstg]
level: practitioner
status: draft
description: "Test access control: role/permission matrices, IDOR/BOLA by swapping object ids between users, vertical privilege escalation, and automated cross-user checks."
sources:
  - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/README
  - https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Authorization and access-control testing

**Goal:** prove each user can do and see only what their role and ownership allow. Broken access control is OWASP Top 10 #1 and API Security #1 (BOLA).

## Build the matrix
Rows: endpoints/actions (`GET /orders/{id}`, `POST /admin/users`, `DELETE /projects/{id}`). Columns: anonymous, user A, user B (same role, other tenant), manager, admin. Cells: expected allow/deny. This matrix is the test oracle.

## Test cases
- **Horizontal (IDOR/BOLA)**: as user A, request user B's object ids (`/orders/1002`, `/files/uuid-of-B`). Expect 403/404, never data.
- **Vertical**: as a normal user, call admin endpoints directly (UI hiding a button is not access control).
- **Function-level**: change HTTP method (`GET` allowed, `PUT` not checked), alternative routes (`/api/v1/` vs `/api/v2/`).
- **Mass assignment**: send extra fields (`"role":"admin"`, `"ownerId":...`) in updates.
- **Tenant isolation**: list/search endpoints never return other tenants' rows; check pagination and export.
- **State-based**: actions after logout, on deleted/locked objects, after role downgrade (token still valid?).

## Automate
```python
CASES = [("GET", "/orders/{b_order}", "user_a", 404),
         ("DELETE", "/admin/users/{b_user}", "user_a", 403),
         ("GET", "/orders/{b_order}", "user_b", 200)]
@pytest.mark.parametrize("method,path,actor,expected", CASES)
def test_access_matrix(clients, ids, method, path, actor, expected):
    r = clients[actor].request(method, path.format(**ids))
    assert r.status_code == expected
```
Generate cases from the matrix file so it stays the single source of truth.
Burp extensions Autorize/AuthMatrix replay every request with another user's session for manual sweeps.

## Gotchas
- Sequential ids make IDOR easy to find but UUIDs do not fix it; test with known UUIDs from user B.
- 200 with an empty body can still be a leak (counts, timing); inspect responses.

## Verify
Every matrix cell has an automated check, and a cross-tenant request for each object type returns 403/404.
