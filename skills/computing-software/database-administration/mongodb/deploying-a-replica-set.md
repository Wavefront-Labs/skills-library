---
id: computing-software.database-administration.mongodb.deploying-a-replica-set
name: deploying-a-replica-set
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set, rs-initiate, keyfile, convert-standalone]
level: practitioner
status: docs-checked
description: "Deploy a three-member MongoDB replica set: mongod.conf with replSetName and keyFile, rs.initiate with hostnames, adding members, and converting a standalone."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/deploy-replica-set/
  - https://www.mongodb.com/docs/manual/tutorial/deploy-replica-set-with-keyfile-access-control/
  - https://www.mongodb.com/docs/manual/tutorial/convert-standalone-to-replica-set/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying a replica set

## Plan
- Three data-bearing members (PSS) in at least two, ideally three, failure domains. Avoid
  arbiters (PSA) for production: they cannot hold data and break majority write concern
  when a data node is down.
- Stable DNS hostnames that every member and client can resolve; use hostnames, not IP addresses, in the replica set config (since 5.0 nodes configured only with an IP address fail startup validation).

## mongod.conf on each member
```yaml
storage:
  dbPath: /var/lib/mongo
net:
  port: 27017
  bindIp: 0.0.0.0              # or specific interfaces; firewall to app + members only
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/mongod/tls/server.pem
    CAFile: /etc/mongod/tls/ca.pem
replication:
  replSetName: rs0
  oplogSizeMB: 51200           # optional; default 5% of free disk (min 990 MB, max 50 GB); only used when the oplog is first created
security:
  authorization: enabled
  keyFile: /etc/mongod/keyfile # internal auth between members; the manual limits keyfiles to test/dev and recommends X.509 for production
```
Keyfile (test/dev): `openssl rand -base64 756 > keyfile; chmod 400 keyfile`, the same file on all members (set ownership to the mongod service user). For production use X.509 member certificates.

## Initiate (on one member, over the localhost interface before any user exists)
```js
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1.example.net:27017", priority: 2 },
    { _id: 1, host: "mongo2.example.net:27017", priority: 1 },
    { _id: 2, host: "mongo3.example.net:27017", priority: 1 }
  ]
})
rs.status()
// then create the first admin user on the primary
db.getSiblingDB("admin").createUser({ user: "admin", pwd: passwordPrompt(), roles: ["root"] })
```
Add later members with `rs.add({ host: "mongo4.example.net:27017", priority: 0, votes: 0 })` and raise priority and votes with `rs.reconfig()` once the member reaches SECONDARY.

## Convert a standalone
1. Add `replication.replSetName` (and keyFile) to the config, restart.
2. `rs.initiate()` on it (it becomes a one-member set with its current data), check
   `rs.conf()` uses its resolvable hostname (`rs.reconfig` if it picked `localhost`).
3. `rs.add()` the new members; they initial-sync.
4. Change application connection strings to the replica set form.

## Client connection string
`mongodb://app:...@mongo1.example.net,mongo2.example.net,mongo3.example.net/?replicaSet=rs0&tls=true&w=majority&retryWrites=true`
or an SRV record (`mongodb+srv://`).

## Verify
`rs.status()` shows one PRIMARY and two SECONDARY with `health: 1`, small `optimeDate` gaps;
stepping down the primary (`rs.stepDown()`) elects another member and the app reconnects.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: keyfile generation (openssl rand -base64 756, chmod 400) and the manual's note that keyfiles are for test/dev with X.509 for production, localhost interface for rs.initiate and the first user, use DNS hostnames not IPs (5.0 startup validation), arbiter/PSA and w:majority limitation, default oplog size and oplogSizeMB semantics, standalone to replica set conversion steps (replSetName, rs.initiate(), rs.add), rs.add priority and votes fields. Removed unconfirmed guidance on raising votes.

Method: documentation only; no commands were run.
