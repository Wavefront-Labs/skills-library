---
id: computing-software.web-development.gin.gin-bind-query-or-post
name: gin-bind-query-or-post
category: computing-software
field: web-development
product: gin
tags: [gin, shouldbind, query-string, form, content-type, time-format, time-utc, binding]
level: intro
status: docs-checked
description: "Use one Gin handler with ShouldBind to accept query strings, form bodies or JSON, with time_format and time_utc tags for dates."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-query-or-post.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bind query string or POST data with ShouldBind

Goal: a single handler that accepts GET query parameters and POST bodies.

`ShouldBind` picks the binder from the HTTP method and Content-Type. GET uses query-string binding (`form` tags). For POST/PUT it uses JSON for `application/json`, XML for `application/xml`, and form binding for `application/x-www-form-urlencoded` or `multipart/form-data`.

```go
type Person struct {
  Name     string    `form:"name"`
  Address  string    `form:"address"`
  Birthday time.Time `form:"birthday" time_format:"2006-01-02" time_utc:"1"`
}

func startPage(c *gin.Context) {
  var person Person
  if err := c.ShouldBind(&person); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  c.JSON(http.StatusOK, gin.H{"name": person.Name, "address": person.Address, "birthday": person.Birthday})
}

route.GET("/testing", startPage)
route.POST("/testing", startPage)
```

All three requests below produce `{"address":"xyz","birthday":"1992-03-15T00:00:00Z","name":"appleboy"}`:

```sh
curl "http://localhost:8085/testing?name=appleboy&address=xyz&birthday=1992-03-15"
curl -X POST http://localhost:8085/testing -d "name=appleboy&address=xyz&birthday=1992-03-15"
curl -X POST http://localhost:8085/testing -H "Content-Type: application/json" \
  -d '{"name":"appleboy","address":"xyz","birthday":"1992-03-15"}'
```

## Gotchas
- `time_format` uses Go's reference time layout; `2006-01-02` means year-month-day.
- `time_utc:"1"` makes the parsed time UTC.

## Why it matters
A single handler can accept data from both query strings and request bodies without manual source selection. If you want query-only binding regardless of method, see the "Only bind query string" page, which the page lists as related reading. Errors from ShouldBind are returned to you, so the example answers with a 400 and the error message.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind query string or post data (binder per method and Content-Type, time_format, time_utc, curl outputs).
Removed or corrected: reference to a nonexistent skill and ShouldBindQuery claim not on the page.

Method: documentation only; no commands were run.
