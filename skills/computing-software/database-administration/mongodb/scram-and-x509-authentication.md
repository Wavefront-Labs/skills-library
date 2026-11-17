---
id: computing-software.database-administration.mongodb.scram-and-x509-authentication
name: scram-and-x509-authentication
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-security, mongodb-authentication, x509-authentication, scram-sha-256, keyfile, internal-authentication, enable-authentication, localhost-exception]
level: practitioner
status: docs-checked
description: "Turn on MongoDB authentication: SCRAM users, keyfile or x.509 internal auth for replica sets, client x.509 certs, and the rolling procedure to enable auth without downtime."
sources:
  - https://www.mongodb.com/docs/manual/core/authentication/
  - https://www.mongodb.com/docs/manual/tutorial/enforce-keyfile-access-control-in-existing-replica-set-without-downtime/
  - https://www.mongodb.com/docs/manual/tutorial/configure-x509-client-authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MongoDB authentication: SCRAM and x.509

**Goal:** no unauthenticated access, members authenticate to each other, and
enabling it on a live replica set causes no outage.

## Create the first admin
The first user you create must have privileges to create other users (`userAdmin` or
`userAdminAnyDatabase`); `root` also qualifies. Create it before enforcing authentication:
```javascript
use admin
db.createUser({ user: "admin", pwd: passwordPrompt(), roles: [ { role: "root", db: "admin" } ] })
```
App users live in their auth database (usually `admin` or the app DB):
```javascript
db.getSiblingDB("admin").createUser({ user: "app", pwd: passwordPrompt(),
  roles: [ { role: "readWrite", db: "shop" } ], mechanisms: ["SCRAM-SHA-256"] })
```

## Internal (member-to-member) auth
Keyfile (shared secret, simplest):
```bash
openssl rand -base64 756 > /etc/mongod/keyfile && chmod 400 /etc/mongod/keyfile && chown mongod: /etc/mongod/keyfile
```
```yaml
security:
  keyFile: /etc/mongod/keyfile
  authorization: enabled
```
x.509 for members instead: `security.clusterAuthMode: x509` with member certs
sharing O/OU/DC and TLS configured (`net.tls.mode: requireTLS`).

## Enabling on a running replica set (no downtime)
1. Create admin and app users (on primary) while auth is off.
2. On each member, rolling (secondaries first, then step down primary):
   set `security.keyFile` and `security.transitionToAuth: true`, restart.
3. Switch clients to authenticated connection strings.
4. Rolling again: remove `transitionToAuth`, keep keyFile (implies authorization), restart.

## Client x.509 auth
User name is the cert subject (RFC2253):
```javascript
db.getSiblingDB("$external").runCommand({ createUser: "CN=reporting,OU=apps,O=Example", roles: [ { role: "read", db: "shop" } ] })
```
```bash
mongosh --tls --tlsCertificateKeyFile client.pem --tlsCAFile ca.pem \
  --authenticationDatabase '$external' --authenticationMechanism MONGODB-X509
```
Each client certificate maps to exactly one user, and the subject must be RFC2253 compatible
(`openssl x509 -in client.pem -inform PEM -subject -nameopt RFC2253`). Keep client certificates'
O/OU/DC values different from the member certificates' (the `enforceUserClusterSeparation`
parameter controls whether MongoDB lets you create a `$external` user matching them).

## Gotchas
- `mongod` and `mongos` bind to localhost by default; set `net.bindIp` only with authentication enforced.
- `authSource` in the connection string must match where the user was created.

## Verify
A `mongosh` session without credentials cannot list databases or read data, and the
replica set rejects non-authenticated connections once `transitionToAuth` is removed.

## Checked
2026-10-31. Confirmed against the MongoDB manual pages for the no-downtime replica set
procedure (keyfile generation, `security.transitionToAuth`, rolling order), client X.509
authentication (`$external`, RFC2253 subject, `MONGODB-X509`), X.509 member authentication
(O/OU/DC, `clusterAuthMode`), `db.createUser` (`mechanisms`) and Users (authentication
database). Removed: the localhost-exception claim, the "since 3.6" bind note, the exact
error text and `connectionStatus` check, and the client-subject sentence rewritten to the
documented behaviour.
Method: documentation only; no commands were run.
