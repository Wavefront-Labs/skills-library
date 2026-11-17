---
id: computing-software.web-development.node-express.nosql-operator-injection
name: nosql-operator-injection
category: computing-software
field: web-development
product: node-express
tags: [injection, nosql-injection, mongodb, mongoose, operator-injection, security]
level: practitioner
status: verified
description: "Stopping NoSQL operator injection in MongoDB/Mongoose apps: $ne/$gt/$regex payloads from JSON and query strings, type validation, sanitizeFilter, and $where risks."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html
  - https://mongoosejs.com/docs/api/mongoose.html#Mongoose.prototype.sanitizeFilter()
  - https://portswigger.net/web-security/nosql-injection
  - https://www.mongodb.com/docs/manual/reference/operator/query/where/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NoSQL operator injection

## 1. The bug
```js
const user = await User.findOne({ email: req.body.email, password: req.body.password });
```
Body `{"email": "admin@x.com", "password": {"$ne": null}}` logs in as admin. Query strings do it too when the extended (`qs`) parser is on: `?password[$ne]=x` becomes `{ password: { $ne: "x" } }` (Express 5 default is `simple`, which gives the flat key `"password[$ne]"` instead; both checked on Express 5.3).
Other payloads: `{"$gt": ""}`, `{"$regex": "^a"}` (blind extraction char by char), `{"$where": "..."}` (server-side JavaScript; `$where` is deprecated in MongoDB docs and unavailable when `security.javascriptEnabled` is false).

## 2. Fixes (layer them)
1. **Validate types at the boundary** - the real fix:
```js
const Login = z.object({ email: z.string().email(), password: z.string().min(1).max(200) });
const { email, password } = Login.parse(req.body);
```
2. Mongoose: `mongoose.set("sanitizeFilter", true)` wraps filter values containing `$` keys in `$eq` (verified on mongoose 9.11: `{password:{$ne:null}}` became `{"password":{"$eq":{"$ne":null}}}`, and `$regex` likewise); `mongoose.trusted()` opts a specific filter back in. `strictQuery: true` drops unknown paths (`{nope:{$ne:1}}` is dropped; with the default, unset, it is passed through to MongoDB).
3. Cast explicitly: `{ email: String(email) }`, `{ _id: new ObjectId(id) }` (throws on bad input).
4. Strip `$`/`.` keys if you accept free-form objects (`express-mongo-sanitize` 2.2.0 (last published January 2025) fails on Express 5: `Cannot set property query of #<IncomingMessage> which has only a getter`, a 500 on every request - prefer schema validation).
5. Express: `app.set("query parser", "simple")` (Express 5 default) disables nested objects in query strings.

## 3. Server-side JS
Disable server-side JavaScript (`security.javascriptEnabled: false`, default `true`; it disables `$where`, `mapReduce`, `$accumulator` and `$function`) and never pass user input to them. `mongod` itself was not run here.

## 4. Passwords
Never query by password at all: fetch by email, then `argon2.verify(hash, password)`. That alone kills the classic bypass.

## 5. Other stores
Same class of bug in Elasticsearch query DSL (user-built JSON), Firestore rules, DynamoDB expressions built by concatenation, Redis commands built from strings.

## Verify
Send `{"field": {"$ne": null}}`, `field[$ne]=x`, `{"field": {"$regex": ".*"}}` to every JSON/query endpoint; expect 400 validation errors, not results.
