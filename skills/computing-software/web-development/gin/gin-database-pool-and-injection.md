---
id: computing-software.web-development.gin.gin-database-pool-and-injection
name: gin-database-pool-and-injection
category: computing-software
field: web-development
product: gin
tags: [gin, database-sql, connection-pool, setmaxopenconns, setconnmaxlifetime, closure, dependency-injection, queryrowcontext]
level: practitioner
status: docs-checked
description: "Open database/sql once in main for Gin, configure SetMaxOpenConns and idle/lifetime limits, and share the DB via closure, middleware c.Set or a handler struct."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/database.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin database/sql setup, pooling and injection

Goal: open one `*sql.DB` in `main`, tune the pool and hand it to handlers.

Open once, ping to fail fast, pass the request context to queries:

```go
db, err := sql.Open("postgres", "host=localhost port=5432 user=app dbname=mydb sslmode=disable")
if err != nil { log.Fatal(err) }
defer db.Close()
if err := db.Ping(); err != nil { log.Fatal(err) }

r.GET("/users/:id", func(c *gin.Context) {
  var name string
  err := db.QueryRowContext(c.Request.Context(), "SELECT name FROM users WHERE id = $1", c.Param("id")).Scan(&name)
  if err == sql.ErrNoRows {
    c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
    return
  }
  ...
})
```

## Pool settings
```go
db.SetMaxOpenConns(25)                  // cap open connections
db.SetMaxIdleConns(10)                  // warm idle connections
db.SetConnMaxLifetime(5 * time.Minute)  // rotate; picks up DNS changes
db.SetConnMaxIdleTime(1 * time.Minute)  // close long-idle connections
```

## Injection patterns
Closure:
```go
func listUsers(db *sql.DB) gin.HandlerFunc {
	return func(c *gin.Context) { /* db.QueryContext(c.Request.Context(), ...) */ }
}
r.GET("/users", listUsers(db))
```
Middleware: `c.Set("db", db)` in a `gin.HandlerFunc`, then `c.MustGet("db").(*sql.DB)` in handlers.
Struct with methods: `type UserHandler struct{ DB *sql.DB }`, then `r.GET("/users/:id", uh.Get)`.

## Gotchas
- Closure and struct patterns are generally preferred over middleware: compile-time type safety, no runtime type assertions.
- Never open a new connection per request.
- Use parameterized queries (`$1`, `?`) to prevent SQL injection; do not leak internal errors to clients.
- Close `*sql.Rows` with `defer rows.Close()` or connections leak back to the pool.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Database Integration (database/sql open, Ping, pool settings with example values, closure/middleware/struct patterns, best practices).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
