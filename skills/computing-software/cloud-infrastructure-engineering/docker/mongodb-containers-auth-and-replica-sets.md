---
id: computing-software.cloud-infrastructure-engineering.docker.mongodb-containers-auth-and-replica-sets
name: mongodb-containers-auth-and-replica-sets
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, mongodb-container, mongo, mongosh, replica-set, keyfile, mongodump, wiredtiger-cache, docker-entrypoint-initdb]
level: practitioner
status: docs-checked
description: "Run MongoDB in Docker: root user and init scripts, mongosh healthchecks, a single-node replica set with keyFile for transactions, WiredTiger cache sizing, and dumps."
sources: ["https://hub.docker.com/_/mongo", "https://www.mongodb.com/docs/manual/tutorial/deploy-replica-set/", "https://www.mongodb.com/docs/manual/tutorial/deploy-replica-set-with-keyfile-access-control/", "https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.wiredTiger.engineConfig.cacheSizeGB", "https://www.mongodb.com/docs/database-tools/mongodump/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MongoDB in containers

## Basic, authenticated
```yaml
services:
  mongo:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD_FILE: /run/secrets/mongo_root_pw
      MONGO_INITDB_DATABASE: app
    secrets: [mongo_root_pw]
    volumes:
      - mongo-data:/data/db
      - mongo-config:/data/configdb
      - ./mongo-init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD", "mongosh", "--quiet", "--eval", "db.adminCommand('ping').ok"]
      interval: 10s
      retries: 10
volumes: { mongo-data: {}, mongo-config: {} }
secrets: { mongo_root_pw: { file: ./mongo_root_pw.txt } }
```
- Root user and init scripts (`*.js`, `*.sh` in `/docker-entrypoint-initdb.d`) run when the
  container starts for the first time (fresh instance). Scripts run against `MONGO_INITDB_DATABASE` (default `test`); create
  the app user there:
  ```js
  // mongo-init/01-user.js
  db.getSiblingDB('app').createUser({user: 'app', pwd: process.env.APP_PW, roles: [{role: 'readWrite', db: 'app'}]});
  ```
- The legacy `mongo` shell is gone since 6.0; healthchecks and scripts must use `mongosh`.
- The image declares volumes for `/data/db` **and** `/data/configdb`; name both.

## Single-node replica set (transactions, change streams)
```yaml
  mongo:
    image: mongo:7
    command: ["--replSet", "rs0", "--bind_ip_all", "--keyFile", "/etc/mongo/keyfile"]
    volumes:
      - mongo-data:/data/db
      - ./keyfile:/etc/mongo/keyfile:ro     # mode 400, readable by the mongod user
```
- Starting mongod with `--keyFile` enforces both internal membership authentication and
  access control. Generate it with `openssl rand -base64 756 > keyfile && chmod 400 keyfile`;
  on UNIX the file must not have group or world permissions, and the user running mongod must
  own it. MongoDB's docs call keyfiles suitable for testing and development only; use X.509
  certificates in production.
- Initiate once:
  ```bash
  docker compose exec mongo mongosh -u root -p --eval \
    "rs.initiate({_id:'rs0',members:[{_id:0,host:'mongo:27017'}]})"
  ```
- The member host name (`mongo:27017`) is what drivers are redirected to. Apps on the host
  cannot resolve `mongo`; connect with `mongodb://localhost:27017/?directConnection=true`
  or add `mongo` to the host's `/etc/hosts`.

## Resource settings
- WiredTiger cache defaults to 50% of (RAM − 1 GB). Set it explicitly under a memory limit:
  `--wiredTigerCacheSizeGB 0.5` for a 1.5 GB container.

## Backup / restore
```bash
docker compose exec -T mongo sh -c 'mongodump -u root -p "$(cat /run/secrets/mongo_root_pw)" --authenticationDatabase admin --archive --gzip' > app-$(date +%F).archive.gz
docker compose exec -T mongo sh -c 'mongorestore -u root -p "$(cat /run/secrets/mongo_root_pw)" --authenticationDatabase admin --archive --gzip --drop' < app-2026-10-16.archive.gz
```

## Verify
```bash
docker compose exec mongo mongosh -u root -p --quiet --eval 'rs.status().ok'   # 1
docker inspect -f '{{.State.Health.Status}}' $(docker compose ps -q mongo)      # healthy
```

## Checked
2026-10-31. Confirmed against the Docker Hub `mongo` page (`_FILE` variables, `.sh`/`.js` init scripts run on first start with `MONGO_INITDB_DATABASE` or `test`, `/data/configdb` volume, `mongosh` from 6.0), the MongoDB keyfile tutorial (`openssl rand -base64 756`, `chmod 400`, no group/world permissions, `--keyFile` enforces auth, keyfiles for test/dev), the `cacheSizeGB` reference (default 50% of RAM minus 1 GB) and the mongodump page (`--archive`, `--gzip`). Removed: AVX requirement, uid 999 ownership, Docker Desktop mode note, the exact keyfile error text, ulimits and upgrade-order advice (not on the pages read).
Method: documentation only; no commands were run.
