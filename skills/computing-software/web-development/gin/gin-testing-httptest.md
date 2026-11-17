---
id: computing-software.web-development.gin.gin-testing-httptest
name: gin-testing-httptest
category: computing-software
field: web-development
product: gin
tags: [gin, testing, httptest, newrecorder, servehttp, testmode, table-driven, middleware-test]
level: practitioner
status: docs-checked
description: "Test Gin routes with net/http/httptest and router.ServeHTTP, silence logs via gin.SetMode(gin.TestMode), table-driven cases and isolated middleware tests."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/testing/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing Gin handlers

Goal: test routes without starting a server, using `net/http/httptest`.

Quiet the debug route logs once for the whole package:

```go
func TestMain(m *testing.M) {
  gin.SetMode(gin.TestMode)
  os.Exit(m.Run())
}
```

Build the router in a function so tests can reuse it:

```go
func setupRouter() *gin.Engine {
  router := gin.Default()
  router.GET("/ping", func(c *gin.Context) {
    c.String(200, "pong")
  })
  return router
}
```

Basic test (uses testify `assert`):

```go
func TestPingRoute(t *testing.T) {
  router := setupRouter()

  w := httptest.NewRecorder()
  req, _ := http.NewRequest("GET", "/ping", nil)
  router.ServeHTTP(w, req)

  assert.Equal(t, 200, w.Code)
  assert.Equal(t, "pong", w.Body.String())
}
```

POST with JSON: marshal a struct, pass `strings.NewReader(string(userJson))` as the request body and compare `w.Body.String()` with the JSON.

## Table-driven
```go
tests := []struct {
  name     string
  method   string
  path     string
  wantCode int
  wantBody string
}{
  {"ping endpoint", "GET", "/ping", 200, "pong"},
  {"not found", "GET", "/nonexistent", 404, ""},
}
for _, tt := range tests {
  t.Run(tt.name, func(t *testing.T) {
    w := httptest.NewRecorder()
    req, _ := http.NewRequest(tt.method, tt.path, nil)
    router.ServeHTTP(w, req)
    assert.Equal(t, tt.wantCode, w.Code)
  })
}
```

## Middleware in isolation
Create `gin.New()`, apply the middleware under test with `router.Use(AuthRequired())`, add a trivial handler, then assert 401 without credentials and 200 after `req.Header.Set("Authorization", "Bearer valid-token")`.

## Gotcha
`gin.SetMode(gin.TestMode)` must run before the router is created to suppress the debug-level route registration logs.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: testing/index.md. Confirmed: SetMode(TestMode) in TestMain and before creating the router, setupRouter, the ping and POST tests with testify, the table-driven test and the middleware test. Trimmed nothing.

Method: documentation only; no commands were run.
