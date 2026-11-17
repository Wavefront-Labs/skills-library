---
id: computing-software.web-development.gin.gin-query-and-form-params
name: gin-query-and-form-params
category: computing-software
field: web-development
product: gin
tags: [gin, c-query, c-defaultquery, c-postform, c-defaultpostform, query-string, urlencoded, multipart-form]
level: intro
status: docs-checked
description: "Read Gin query string values and POST form fields with c.Query, c.DefaultQuery, c.PostForm and c.DefaultPostForm, which never cross sources."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/querystring-param.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/query-and-post-form.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/multipart-urlencoded-form.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin query string and form parameters

Goal: read values from the URL query and the request body.

Query string (after `?`):
- `c.Query("key")` returns the value or an empty string if missing.
- `c.DefaultQuery("key", "default")` returns the value or your default.
- `c.Query` is a shortcut for `c.Request.URL.Query().Get(...)`.

Form body (works for both `application/x-www-form-urlencoded` and `multipart/form-data`):
- `c.PostForm("field")` returns the value or an empty string.
- `c.DefaultPostForm("field", "fallback")` returns the value or the fallback.

```go
router.POST("/post", func(c *gin.Context) {
  id := c.Query("id")
  page := c.DefaultQuery("page", "0")
  name := c.PostForm("name")
  message := c.PostForm("message")
  nick := c.DefaultPostForm("nick", "anonymous")

  c.String(http.StatusOK, "id: %s; page: %s; name: %s; message: %s; nick: %s",
    id, page, name, message, nick)
})
```

```sh
curl -X POST "http://localhost:8080/post?id=1234&page=1" -d "name=manu&message=this_is_great"
# Output: id: 1234; page: 1; name: manu; message: this_is_great

curl -X POST http://localhost:8080/post -F "name=manu" -F "message=hello"   # multipart form, same handler
```

## Gotcha
`c.Query` reads only the URL query and `c.PostForm` reads only the body; they never cross over. To check both automatically, use `c.ShouldBind` with a struct.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: routing/querystring-param.md, routing/query-and-post-form.md and routing/multipart-urlencoded-form.md. Confirmed: empty-string and default behaviour of Query, DefaultQuery, PostForm and DefaultPostForm, both content types, the curl outputs and the "never cross over, use ShouldBind" note. Trimmed nothing. Fixed three sources with the bogus website/ segment.

Method: documentation only; no commands were run.
