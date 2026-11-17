---
id: computing-software.database-administration.mongodb.mongod-configuration-file
name: mongod-configuration-file
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongod-conf, mongodb-configuration, mongodb-operations, yaml-config]
level: practitioner
status: verified
description: "Write and maintain a production mongod.conf (storage, net, security, replication, systemLog, setParameter) and change parameters at runtime safely."
sources:
  - https://www.mongodb.com/docs/manual/reference/configuration-options/
  - https://www.mongodb.com/docs/manual/reference/parameters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mongod configuration file

**Goal:** one reviewed YAML file per node that captures every non-default setting, instead of command-line flags and runtime changes nobody remembers.

## Baseline replica set member
```yaml
storage:
  dbPath: /var/lib/mongodb
  wiredTiger:
    engineConfig:
      cacheSizeGB: 24              # default is 50% of (RAM - 1 GB); set explicitly when sharing the host
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  logRotate: reopen               # rename-and-reopen rotation (set by an external tool or the logRotate command)
net:
  port: 27017
  bindIp: 127.0.0.1,10.0.1.11
  maxIncomingConnections: 20000
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/mongodb/tls/server.pem
    CAFile: /etc/mongodb/tls/ca.pem
security:
  authorization: enabled
  keyFile: /etc/mongodb/keyfile    # or clusterAuthMode: x509
replication:
  replSetName: rs0
  oplogSizeMB: 51200
operationProfiling:
  mode: off
  slowOpThresholdMs: 100
processManagement:
  timeZoneInfo: /usr/share/zoneinfo
setParameter:
  diagnosticDataCollectionEnabled: true
```
YAML must use spaces, not tabs; a tab produces a startup parse error ("Error parsing YAML config file: yaml-cpp ... illegal map value").

## Runtime vs file
```javascript
db.adminCommand({ getParameter: "*" })
db.adminCommand({ setParameter: 1, logLevel: 1 })     // runtime only, lost on restart
db.adminCommand({ getCmdLineOpts: 1 })                // what the running process actually parsed
```
Every runtime change must also go into the file (or config management) or it disappears at the next restart.

## Expansion directives
```yaml
storage:
  dbPath:
    __exec: "cmd /c echo <DATA_DIR>"      # on Linux: an absolute script path
    type: string
    trim: whitespace
```
`__exec` (command) and `__rest` (REST endpoint) pull values from outside the file, keeping secrets out of it. Expansion is off by default: start with `--configExpand exec` or the process refuses ("storage.dbPath.__exec support has not been enabled"). `trim: whitespace` was needed to drop the trailing newline of `echo`.

## Gotchas
- Start with `mongod --config <file>`; options on the command line override the file (`--port 27499` replaced `net.port: 27471` in `--outputConfig`).
- `bindIp: 0.0.0.0` without auth/TLS is the classic data-leak setup.
- Keep config identical across members except host-specific values; diff them in CI.

## Verify
`mongod --config /etc/mongod.conf --outputConfig` prints the parsed effective config without starting; diff it against the template.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. The baseline file (Linux paths) parsed with `mongod --config <file> --outputConfig` and printed the same options sorted; a Windows-path copy with port 27471, `logRotate: reopen`, `operationProfiling.mode: slowOp`, `slowOpThresholdMs: 50`, `setParameter.diagnosticDataCollectionEnabled` and `cacheSizeGB: 1` started a node; `getCmdLineOpts` showed those parsed values, `getParameter` showed `diagnosticDataCollectionEnabled: true` and `getProfilingStatus` slowms 50; the engine reported a 1 GB cache.
- A tab-indented file failed to parse; `__exec` worked with `--configExpand exec` and failed without; the command-line port overrode the file. The default cache formula (50% of RAM minus 1 GB) matched `maximum bytes configured` on this host (15742 MB for 32509 MB RAM).
- Not run: TLS and keyFile settings (parsed only), `__rest`, and `logRotate` with an external rotator.
