---
id: computing-software.data-engineering.apache-kafka.connector-lifecycle-operations
name: connector-lifecycle-operations
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-connect, connector-restart, connect-rest-api, pause-resume, connector-validate, failed-tasks, connector-status]
level: practitioner
status: docs-checked
description: "Operate Kafka Connect connectors via the REST API: validate configs, create/update idempotently, check status, restart failed tasks, pause/resume/stop, and delete safely."
sources:
  - https://kafka.apache.org/documentation/#connect_rest
  - https://kafka.apache.org/documentation/#connect_administration
  - https://github.com/apache/kafka/blob/trunk/docs/kafka-connect/user-guide.md
  - https://github.com/apache/kafka/blob/trunk/docs/kafka-connect/administration.md
  - https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResource.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connector lifecycle operations

**Goal:** routine day-2 handling of connectors: deploy, detect failures, restart only what failed, and change config without surprises.

`CONNECT=http://connect:8083` below. Secure the REST API in production: any caller allowed onto it can act on every connector.

## Validate before deploying
```bash
curl -s -X PUT -H 'Content-Type: application/json' \
  $CONNECT/connector-plugins/<connector-class-or-alias>/config/validate \
  -d @pg-orders.json    # per-config validation with suggested values and error messages
```

## Create or update (idempotent)
```bash
curl -s -X PUT -H 'Content-Type: application/json' $CONNECT/connectors/pg-orders/config -d @pg-orders.config.json
```
`PUT /connectors/{name}/config` creates the connector if missing, otherwise updates its configuration. Prefer it over `POST /connectors` in CI.

## Status
```bash
curl -s "$CONNECT/connectors?expand=status"
curl -s $CONNECT/connectors/pg-orders/status    # failed tasks carry a trace field
```
States: `UNASSIGNED`, `RUNNING`, `PAUSED`, `STOPPED` (connectors only; the tasks of a stopped connector are shut down and not shown), `FAILED`, `RESTARTING`. A connector can be `RUNNING` while its tasks are `FAILED`: always check tasks. Status updates travel through `status.storage.topic`, so a change can take a moment to appear.

## Restart
```bash
# restart the connector and, with includeTasks, its tasks; onlyFailed limits it to FAILED instances
curl -s -X POST "$CONNECT/connectors/pg-orders/restart?includeTasks=true&onlyFailed=true"
curl -s -X POST $CONNECT/connectors/pg-orders/tasks/0/restart
```
Connect does not automatically restart failed tasks. Restarting a task during a rebalance returns 409 (Conflict); retry after the rebalance. Alert if the same task fails repeatedly (it is likely a data or config problem, not transient).

## Pause, resume, stop
```bash
curl -s -X PUT $CONNECT/connectors/pg-orders/pause     # tasks keep their resources, message processing stops
curl -s -X PUT $CONNECT/connectors/pg-orders/resume    # resumes a paused or stopped connector
curl -s -X PUT $CONNECT/connectors/pg-orders/stop      # tasks shut down and release resources; required before offset changes
```

## Delete
```bash
curl -s -X DELETE $CONNECT/connectors/pg-orders
```
Deleting halts all tasks and deletes the connector configuration, and also deletes the connector's active-topics set. Source offsets are stored separately, so a new connector with the same name would find its old offsets: reset them first with the offsets API on a stopped connector (see the offsets skill) or use a new name.

## Gotchas
- A rebalance effectively restarts all connectors and tasks; since 2.3.0 Connect uses incremental cooperative rebalancing by default (`connect.protocol=eager` restores the old behaviour).
- Secrets in configs are visible through the REST API and stored in `config.storage.topic` unless externalised with a ConfigProvider.
- `PATCH /connectors/{name}/config` patches configuration, where a `null` value removes the key; `POST /connectors` also accepts an `initial_state` of `STOPPED`, `PAUSED` or `RUNNING`.

## Verify
- [ ] Monitoring checks task states, not just connector state.
- [ ] Deploy pipeline runs validate and fails on any reported configuration error.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: REST endpoints and parameters for create, config PUT and PATCH, status, pause, stop, resume, restart (`includeTasks`, `onlyFailed`), task restart, delete, validation and `GET /connectors?expand=...` (user guide, administration docs and ConnectorsResource source), the connector and task states and that Connect does not restart failed tasks, the 409 on task restart during a rebalance, and the `connect.protocol` default. Removed: the `jq` pipelines, the Debezium class name and replication-slot advice, the KIP-745 and 3.5 version gates, and the claim that `PUT config` restarts tasks.

Method: documentation only; no commands were run.
