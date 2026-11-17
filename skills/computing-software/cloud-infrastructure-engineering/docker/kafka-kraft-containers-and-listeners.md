---
id: computing-software.cloud-infrastructure-engineering.docker.kafka-kraft-containers-and-listeners
name: kafka-kraft-containers-and-listeners
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, database-container, kafka-container, advertised-listeners, kraft, compose, apache-kafka]
level: advanced
status: docs-checked
description: "Run Kafka in KRaft mode in Docker with listeners that work from other containers and the host: advertised listeners, controller quorum, cluster ID, data persistence."
sources: ["https://hub.docker.com/r/apache/kafka", "https://kafka.apache.org/documentation/#brokerconfigs_advertised.listeners", "https://github.com/apache/kafka/blob/trunk/docker/examples/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka (KRaft) in containers: listeners that work

The number one Kafka-in-Docker bug: clients connect to the bootstrap address, receive the
broker's **advertised** address, and that address is unreachable from where the client runs.

## Single broker+controller with two client listeners
Based on the official `apache/kafka` examples (combined mode, one listener for the Docker network, one for the host):
```yaml
services:
  kafka:
    image: apache/kafka:<VERSION>             # pick a tag from Docker Hub; do not leave on latest
    hostname: kafka
    ports: ["127.0.0.1:29092:29092"]          # for clients on the host
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: INTERNAL://:9092,HOST://:29092,CONTROLLER://:9093
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka:9092,HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,HOST:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
```
- Containers on the Compose network use `kafka:9092`.
- Host tools use `localhost:29092`.
- Clients on other machines need a third listener advertising the host's routable name/IP.
- With one node and one listener on `localhost`, `localhost` is correct both inside the container and from the host;
  this stops working with several nodes (Docker Hub overview).

## How to reason about listeners
`KAFKA_LISTENERS` = where the broker binds. `KAFKA_ADVERTISED_LISTENERS` = what it tells
clients. Each client must be able to resolve and reach the advertised address of the listener
it connected through. Clients connect directly to brokers after bootstrapping, so use one listener per network
vantage point: a container-name listener for the Docker network (also used between brokers) and a `localhost` one on a
unique mapped port per broker for the host.

## Environment variables
- Env vars must begin with `KAFKA_`, and dots in broker config names become underscores:
  `num.partitions` -> `KAFKA_NUM_PARTITIONS`.
- Once you override any configuration, none of the image's default configuration is used, so supply every required
  setting (node id, process roles, listeners, quorum voters, replication factors).
- Replication factor defaults are 3 for the offsets topic and transaction state log (min ISR 2); with one broker set
  them to 1 explicitly or the internal topics cannot be created.
- `CLUSTER_ID` is optional: the image has a default cluster id.
- If `KAFKA_LISTENERS` is omitted it is derived from `KAFKA_ADVERTISED_LISTENERS` by replacing the host with `0.0.0.0`.

## Verify
```bash
docker compose exec --workdir /opt/kafka/bin kafka ./kafka-topics.sh --bootstrap-server kafka:9092 --create --topic t1
# from the host, with a Kafka distribution's bin directory:
./kafka-topics.sh --bootstrap-server localhost:29092 --create --topic t2
```

## Gotchas
- Persistence: the official examples set no volume. Mount storage for the broker's log directory (`log.dirs`) and check
  the Kafka Docker usage guide for the path before relying on it.
- In isolated mode (separate controller and broker containers) `KAFKA_PROCESS_ROLES` is `controller` or `broker`, not
  `broker,controller`, and `KAFKA_CONTROLLER_QUORUM_VOTERS` lists all controllers; make brokers `depends_on` controllers.
- The official multi-node Compose example is for learning, not production.

## Checked
2026-10-28. Confirmed on the Docker Hub apache/kafka overview and the apache/kafka docker examples README: env var
mapping and `KAFKA_` prefix, override-disables-defaults rule, listener/advertised-listener layout with `PLAINTEXT_HOST`
style second listener, combined and isolated process roles, replication factor defaults, optional CLUSTER_ID, derived
`KAFKA_LISTENERS`, tool path `/opt/kafka/bin`. Removed (not confirmed): the `3.8.0` tag, `KAFKA_LOG_DIRS` and
`/var/lib/kafka/data`, `kafka-storage.sh random-uuid`, `kafka-metadata-quorum.sh`, kcat, the `meta.properties` and
`/tmp` default-path statements, `KAFKA_CFG_*` and `CONFLUENT_*` names.
Method: documentation only; no commands were run.
