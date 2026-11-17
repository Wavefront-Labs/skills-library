---
id: computing-software.database-administration.neo4j.testing-with-containers
name: testing-with-containers
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, testcontainers, integration-testing, docker, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Run Neo4j in Testcontainers for integration tests: password, config, plugins, enterprise image licence, and cleaning data between tests."
sources: ["https://java.testcontainers.org/modules/databases/neo4j/", "https://neo4j.com/docs/java-reference/current/extending-neo4j/procedures-and-functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing with Testcontainers

Goal: reliable tests.
- Use the Testcontainers Neo4j module (`org.testcontainers:testcontainers-neo4j`), based on the official Neo4j Docker image. It supports Neo4j 5.x images as well as 4.4. Add the Neo4j Java driver to reach it over Bolt.
- Container options include a custom password, a random password, disabled authentication, Neo4j configuration settings, and copying plugin jars (such as APOC) from the classpath or a folder.
- Pin the image tag so tests do not move with the latest release.
- For Enterprise on a 5.x image, declare the enterprise image yourself (for example `neo4j:5-enterprise`) and set `NEO4J_ACCEPT_LICENSE_AGREEMENT` to `yes` with `.withEnv(...)`. The 4.4 helper instead needs a `container-license-acceptance.txt` on the classpath.
- Wipe data between tests with `MATCH (n) DETACH DELETE n` (the pattern used in Neo4j's own Harness test example).
- Create constraints and indexes in fixtures so test data meets the same rules as production.
Verify: tests are independent and repeatable.

## Checked

2026-11-09. Confirmed against the Testcontainers Neo4j module page (testcontainers-java docs/modules/databases/neo4j.md) and the Neo4j Java Reference Harness example (MATCH (n) DETACH DELETE n after each test). Removed: the claim of a fresh database per test being Enterprise-only (multi-database edition limits not checked), and the draft disclaimer.

Method: documentation only; no commands were run.
