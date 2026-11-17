---
id: computing-software.cloud-infrastructure-engineering.docker.testcontainers-for-python-and-node
name: testcontainers-for-python-and-node
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, testcontainers, testcontainers-python, testcontainers-node, pytest-fixtures, jest-global-setup, vitest, integration-tests, wait-strategy]
level: practitioner
status: docs-checked
description: "Use Testcontainers from Python (pytest session fixtures) and Node/TypeScript (Jest/Vitest global setup): modules, generic containers, waits, timeouts and debug logging."
sources: ["https://testcontainers-python.readthedocs.io/en/latest/", "https://github.com/testcontainers/testcontainers-python", "https://node.testcontainers.org/quickstart/", "https://node.testcontainers.org/features/wait-strategies/", "https://node.testcontainers.org/modules/postgresql/", "https://node.testcontainers.org/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testcontainers for Python and Node

## Python
```bash
pip install "testcontainers[postgres,redis]" pytest psycopg
```
Session-scoped fixtures: start once per test run, not per test.
```python
# conftest.py
import pytest
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer

@pytest.fixture(scope="session")
def pg_url():
    with PostgresContainer("postgres:16-alpine", driver="psycopg") as pg:
        yield pg.get_connection_url()        # postgresql+psycopg://test:test@localhost:<port>/test

@pytest.fixture(scope="session")
def redis_client():
    with RedisContainer("redis:7-alpine") as r:
        yield r.get_client()
```
- `driver` defaults to `"psycopg2"`; `driver=None` returns a URL without a driver suffix
  (`postgresql://...`); any other value is added as `postgresql+<driver>://`. The container's
  default user, password and database are all `test`.
- The old module paths `testcontainers.postgres` and `testcontainers.redis` are deprecated aliases
  that emit a `DeprecationWarning`; import from `testcontainers.community.*`.
- The context manager stops the container; Ryuk is the safety net for killed runs.

Generic container:
```python
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

with DockerContainer("localstack/localstack:3").with_exposed_ports(4566) as ls:
    wait_for_logs(ls, "Ready.", timeout=60)
    endpoint = f"http://{ls.get_container_host_ip()}:{ls.get_exposed_port(4566)}"
```

## Node / TypeScript
```bash
npm i -D testcontainers @testcontainers/postgresql
```
```ts
import { PostgreSqlContainer, StartedPostgreSqlContainer } from "@testcontainers/postgresql";
import { GenericContainer, Wait } from "testcontainers";

let pg: StartedPostgreSqlContainer;
beforeAll(async () => {
  pg = await new PostgreSqlContainer("postgres:16-alpine").start();
  process.env.DATABASE_URL = pg.getConnectionUri();
}, 120_000);                                   // generous hook timeout: the first run pulls the image
afterAll(async () => { await pg?.stop(); });

const redis = await new GenericContainer("redis:7-alpine")
  .withExposedPorts(6379)
  .withWaitStrategy(Wait.forLogMessage("Ready to accept connections"))
  .start();
const url = `redis://${redis.getHost()}:${redis.getMappedPort(6379)}`;
```

### One container for the whole run
To share one container across test files, start it from your test runner's global setup hook and stop it in
the global teardown hook; check the runner's documentation for how values from global setup reach the test files.

## Debugging (both)
- Node: `DEBUG=testcontainers*` enables all logs; narrower loggers are `testcontainers:containers`,
  `testcontainers:pull`, `testcontainers:compose`, `testcontainers:exec` and `testcontainers:build`.
- Configuration comes from environment variables and `~/.testcontainers.properties`; in Python a property such as `ryuk.disabled`
  maps to `TESTCONTAINERS_RYUK_DISABLED`. `TESTCONTAINERS_HOST_OVERRIDE` sets the host on which ports are exposed and
  `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` the socket path Ryuk uses (Node docs).

## Verify
```bash
pytest -q tests/integration          # or: npx jest tests/integration
docker ps -a --filter label=org.testcontainers=true     # empty afterwards
```

## Checked
Documentation release: testcontainers-python 4.15.0 (docs/features, docs/modules and source under src/testcontainers/community and core), testcontainers-node v12.2.1 docs (modules/postgresql, features/wait-strategies, configuration) and module source, checked 2026-10-26.
Confirmed: `pip install testcontainers[postgres]` and `[redis]` extras; `testcontainers.community.postgres.PostgresContainer` (default `test`/`test`/`test`, `driver="psycopg2"`, `driver=None` for a plain URL, `get_connection_url`); `RedisContainer.get_client`; `DockerContainer.with_exposed_ports`, `get_container_host_ip`, `get_exposed_port`; `wait_for_logs(container, predicate, timeout)`; Node `npm install @testcontainers/postgresql`, `new PostgreSqlContainer(image)`, `getConnectionUri()`, `Wait.forLogMessage`, `GenericContainer`, `getHost`, `getMappedPort`; `DEBUG=testcontainers*` and sub-loggers; `TESTCONTAINERS_` property-to-env mapping.
Corrected: Python module imports moved to `testcontainers.community.*` (old paths are deprecated aliases).
Removed as unsupported: pytest-xdist behaviour, the Jest 5 s default timeout, the Jest `globalSetup` and Vitest `provide` snippets, the Python logging line, and Colima/Podman socket override advice.
Method: documentation only; no commands were run.
