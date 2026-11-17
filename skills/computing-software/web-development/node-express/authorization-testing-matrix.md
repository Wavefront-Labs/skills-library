---
id: computing-software.web-development.node-express.authorization-testing-matrix
name: authorization-testing-matrix
category: computing-software
field: web-development
product: node-express
tags: [authorization-testing, access-control-testing, idor-testing, autorize, permission-matrix, security-testing]
level: practitioner
status: docs-checked
description: "Testing access control systematically: a role x endpoint permission matrix as data, automated per-role tests and Burp Autorize replays."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet.html
  - https://github.com/PortSwigger/autorize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorization testing matrix

## 1. Write the matrix
| Endpoint | anon | user (own) | user (other's) | other tenant | support | admin |
|---|---|---|---|---|---|---|
| `GET /api/invoices/:id` | 401 | 200 | 404 | 404 | 200 (read-only) | 200 |
| `PATCH /api/invoices/:id` | 401 | 200 | 404 | 404 | 403 | 200 |
| `POST /api/admin/users` | 401 | 403 | 403 | 403 | 403 | 201 |
Keep it as a machine-readable file (the OWASP cheat sheet uses XML; YAML or JSON work the same) that a person can also read and update, and make the tests read it as their input. The cheat sheet treats an authorization as feature x logical role, with an optional third dimension of data (filtering at business-data level). The status codes above are illustrative values, not a standard.

## 2. Drive tests from it
```ts
for (const row of matrix) for (const [actor, expected] of Object.entries(row.expect)) {
  test(`${row.method} ${row.path} as ${actor} -> ${expected}`, async () => {
    const res = await request(app)[row.method.toLowerCase()](fill(row.path, fixtures[actor]))
      .set(authHeaders(actor)).send(row.body ?? {});
    expect(res.status).toBe(expected);
  });
}
```
Use one test case per point of view (role) with shared helper code, so a failure names the role and service that broke the matrix. Run the suite on each release, because most authorization problems come from features added or changed in later releases. Fixtures: two users per tenant, two tenants, each role; objects owned by each.

## 3. Tool-assisted replay
Burp **Autorize** (BApp Store, needs Jython): set a low-privileged user's cookie or Authorization header in its configuration, switch interception on, then browse as a high-privileged user. It replays each request with the low-privilege header and with no authentication, and marks each as Bypassed, Enforced or "Is enforced???" (needs an enforcement detector, such as a fingerprint string for the denial page). It relies on response comparison heuristics, so false positives and negatives are possible.

## Verify
- [ ] Every service exposed by the system has a row in the matrix and the suite runs on each release.

## Checked

The matrix-as-data approach, point-of-view test structure, release-time automation and Autorize behaviour were confirmed on the OWASP Authorization Testing Automation Cheat Sheet and the Autorize README. Dropped as unconfirmed by any page read: the 404-for-hidden-objects advice, router enumeration per framework, identifier-swap and method-tampering lists, and mass-assignment probes. The OWASP WSTG page could not be read (404 on the raw source).

Method: docs-checked 2026-11-09 against the OWASP Authorization Testing Automation Cheat Sheet (raw markdown read in full) and the PortSwigger Autorize README (read in full).
