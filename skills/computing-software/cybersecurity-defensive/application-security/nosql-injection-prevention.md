---
id: computing-software.cybersecurity-defensive.application-security.nosql-injection-prevention
name: nosql-injection-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [nosql-injection, mongodb, operator-injection, express-mongo-sanitize, injection, cwe-943]
level: practitioner
status: docs-checked
description: "Prevent NoSQL injection in MongoDB and similar stores: operator injection from JSON bodies, $where and server-side JS, type enforcement, sanitisation middleware and tests."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Security_Cheat_Sheet.html", "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection", "https://www.mongodb.com/docs/manual/core/server-side-javascript/", "https://cwe.mitre.org/data/definitions/943.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NoSQL injection prevention

NoSQL databases avoid SQL syntax, not injection. The common form is **operator injection**: the app passes a
user-controlled object into a query, and the attacker supplies operators instead of values.

## The bug (Node + MongoDB)
```js
// body: {"username": "admin", "password": {"$ne": null}}
const user = await users.findOne({ username: req.body.username, password: req.body.password });
```
`{"$ne": null}` matches any password: authentication bypass. The OWASP NoSQL Security Cheat Sheet notes that building a query object does not prevent operator injection when an untrusted value is itself an object (for example `{ name: { $ne: "" } }`).

## Server-side JavaScript
`$where`, `$function` and `$accumulator` execute JS on the server (MongoDB server-side JavaScript docs). Concatenating input into them is
code injection: `{ $where: "this.name == '" + name + "'" }`. Avoid these operators; disable server-side JS
(`security.javascriptEnabled: false` in mongod config) if not needed.

## Defences
1. **Enforce types**: the value must be a string, number, etc., not an object. The OWASP cheat sheet's example checks `typeof name !== 'string'` and rejects the request.
2. **Disallow client-controlled query operators** (`$where`, `$regex`, `$expr`) unless strictly required and validated (OWASP NoSQL Security Cheat Sheet).
3. **Never check passwords in the query**: fetch by username, then compare a hash with a constant-time KDF
   verify.
4. Least-privilege DB users; authentication enabled; not internet-exposed.

## Verify
Tests sending `{"$ne": null}` as a value to login and search endpoints get 400 or
no match; code search finds no `$where` with string concatenation.

## Checked

2026-10-28. Confirmed: OWASP NoSQL Security Cheat Sheet (`$ne` operator injection with object values, `typeof` string check, disallowing `$where`/`$regex`/`$expr`); MongoDB server-side JavaScript page (`$where`, `$function`, `$accumulator`, `security.javascriptEnabled` set to false). Removed: `mapReduce`, `$gt`/`$in`, query-string `password[$ne]` form, Mongoose `sanitizeFilter` and `trusted()`, `$eq` wrapping, `express-mongo-sanitize`, schema-validator names, and the Elasticsearch, Redis, CouchDB and Cassandra section (none found in the fetched pages).
Method: documentation only; no commands were run.
