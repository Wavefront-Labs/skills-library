---
id: computing-software.software-engineering.java.hikaricp-pool-sizing-and-diagnostics
name: hikaricp-pool-sizing-and-diagnostics
category: computing-software
field: software-engineering
product: java
tags: [java, java-jdbc, hikaricp, connection-pool, pool-sizing, leak-detection-threshold, connection-timeout, maxlifetime]
level: practitioner
status: docs-checked
description: "Size and diagnose HikariCP: maximumPoolSize, connectionTimeout, maxLifetime below DB limits, keepaliveTime, leakDetectionThreshold and pool exhaustion errors."
sources: ["https://github.com/brettwooldridge/HikariCP#configuration-knobs-baby", "https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing", "https://docs.spring.io/spring-boot/reference/data/sql.html#data.sql.datasource.connection-pool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HikariCP sizing and diagnostics

Spring Boot's default pool. Properties under `spring.datasource.hikari.*`.

## Settings that matter
```yaml
spring.datasource.hikari:
  maximum-pool-size: 10        # default 10
  minimum-idle: 10             # default = maximum-pool-size (fixed-size pool, recommended by HikariCP)
  connection-timeout: 3000     # ms to wait for a connection (default 30000, minimum 250); fail fast
  max-lifetime: 1740000        # ms; several seconds shorter than any DB/infrastructure limit (default 1800000, minimum 30000)
  idle-timeout: 600000         # only applies if minimum-idle < maximum-pool-size (default 600000, minimum 10000)
  leak-detection-threshold: 20000   # ms a connection may be out before a leak is logged (default 0 = off, minimum 2000)
  keepalive-time: 300000       # ping idle connections; must be below max-lifetime (default 120000, minimum 30000)
  pool-name: orders-db         # shows in logging and JMX
```
HikariCP says to run `minimumIdle` unset so the pool is fixed-size, and to leave `connectionTestQuery` unset on JDBC4 drivers (it uses `isValid()`).

## Sizing
The About-Pool-Sizing page gives `connections = ((core_count * 2) + effective_spindle_count)` as a starting point: core count excludes hyperthreading threads, and effective spindle count is zero when the active data set is fully cached. Total across all instances must fit the database's own connection limit with headroom for admin sessions. When the pool is at maximum with no idle connection, `getConnection()` blocks up to `connectionTimeout` and then throws a `SQLException`, so more threads than connections just queue.

## Diagnose
- "Connection is not available, request timed out" with all connections active: the pool is exhausted. Find who holds connections with a thread dump (threads sitting in `getConnection` are waiters; the holders are elsewhere) and set `leak-detection-threshold` so the holder's stack is logged.
- Long transactions: a `@Transactional` method spanning HTTP calls holds a connection for its whole duration.
- Dropped idle connections: keep `max-lifetime` shorter than any network device or database limit, and use `keepalive-time` to keep idle connections from being timed out.
- Pool metrics: HikariCP can report to a Dropwizard `MetricRegistry` (programmatic configuration); check your metrics integration's own docs for the meter names.

## Gotchas
- Multiple pools (read replica, reporting) need distinct `pool-name`s and sums within DB limits.
- Don't set `maximumPoolSize` huge to hide leaks.
- Some JDBC URLs set their own timeouts (`socketTimeout`, `connectTimeout`); align them below app request timeouts.
- Flyway/Liquibase at startup use the same pool.

## Verify
Load test with concurrency above the pool size and confirm waiting requests fail at `connection-timeout` rather than hanging.

## Checked
Confirmed on the HikariCP README configuration section: defaults and minimums for connectionTimeout, idleTimeout, keepaliveTime, maxLifetime, leakDetectionThreshold, minimumIdle, maximumPoolSize; and on the About-Pool-Sizing wiki page: the sizing formula, core and spindle notes.
Removed: Micrometer meter names, DEBUG logger name and 30 s claim, the "Failed to validate connection" message, "10-20 usually saturates", and the virtual-thread advice, none confirmed on the cited pages.
Method: docs-only read of cited pages, 2026-11-08
