---
id: computing-software.software-engineering.java.preparedstatement-and-parameter-binding
name: preparedstatement-and-parameter-binding
category: computing-software
field: software-engineering
product: java
tags: [java, java-jdbc, preparedstatement, sql-injection, jdbc-batch-fetchsize, generated-keys, allow-list]
level: practitioner
status: docs-checked
description: "Use JDBC PreparedStatement for parameterised SQL: bind values, allow-list identifiers, set NULLs, fetch generated keys, batch, and set query timeout and fetch size."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/PreparedStatement.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/Statement.html", "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PreparedStatement and parameter binding

## Always bind values
```java
String sql = "SELECT id, email FROM users WHERE status = ? AND created_at >= ?";
try (Connection c = ds.getConnection();
     PreparedStatement ps = c.prepareStatement(sql)) {
    ps.setString(1, status);
    ps.setObject(2, since);
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) { ... rs.getLong("id") ... }
    }
}
```
- A `PreparedStatement` holds a precompiled SQL statement that can be executed many times efficiently.
- Parameter markers stand for data values, not table names, column names or SQL keywords such as `ASC` and `DESC`. Keep those structural choices fixed in code; when users choose, map the selection to a small set of application-owned tokens allowed for that query and reject unknown choices (map a requested direction to the literal `ASC` or `DESC`, never append the supplied text).
- Do not use manual escaping as a substitute for binding: escaping depends on the SQL dialect and configuration (for example MySQL's `NO_BACKSLASH_ESCAPES` mode disables backslash escaping). Least privilege limits damage but does not prevent SQL injection.

## Common tasks
- Null: use `setNull(i, Types.X)` or `setObject(i, value, sqlType)`. Not all databases accept an untyped null, so the Javadoc recommends these over `setObject(i, x)` for portability.
- Arbitrary type conversions: use `setObject` with a target SQL type.
- Generated keys: `c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)`, execute, then `ps.getGeneratedKeys()`. It returns an empty `ResultSet` if no keys were generated; if key columns were not specified the driver chooses the columns. A driver may throw `SQLFeatureNotSupportedException`.
- Timeouts: `setQueryTimeout(seconds)`; zero (the default) means no limit, and exceeding it throws `SQLTimeoutException`. With batching it is implementation defined whether the timeout applies per command or to the whole batch.
- Result metadata: `ps.getMetaData()` can be read before executing because the statement is precompiled.

## Batch and fetch size
```java
for (Row r : rows) { ps.setLong(1, r.id()); ps.addBatch(); }
int[] counts = ps.executeBatch();
ps.setFetchSize(500);      // hint only
```
- `executeBatch` returns update counts in the order commands were added. Each element is a count of zero or more, or `Statement.SUCCESS_NO_INFO` (success, row count unknown).
- If a command fails, `BatchUpdateException` is thrown. A driver may or may not continue with the rest, consistently for the DBMS; if it continues, `getUpdateCounts` has an entry per command and failed ones are `Statement.EXECUTE_FAILED`.
- `setFetchSize(rows)` is only a hint for how many rows to fetch when more are needed; zero (the default) means the hint is ignored, and a negative value throws `SQLException`.

## Self-check
- [ ] A test binds the string `x'; DROP TABLE t;--` as a parameter and asserts it is stored or matched literally.

## Checked

Confirmed on the JDK 21 PreparedStatement and Statement Javadoc and the OWASP SQL injection cheat sheet. Removed because the pages do not state them: JDBC 4.2 `java.time` support in `setObject`, PostgreSQL `RETURNING` and `= ANY(?)` array use, IN-list sizing, PostgreSQL `prepareThreshold`, MySQL `useCursorFetch` and `rewriteBatchedStatements`, PostgreSQL autocommit requirement for cursors, LIKE-wildcard escaping, `LocalDateTime` zone advice, and connection-pool leak notes.

Method: docs-only read of cited pages, 2026-11-08
