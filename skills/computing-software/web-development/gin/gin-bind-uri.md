---
id: computing-software.web-development.gin.gin-bind-uri
name: gin-bind-uri
category: computing-software
field: web-development
product: gin
tags: [gin, shouldbinduri, uri-tag, path-parameters, uuid, validation, binding]
level: intro
status: docs-checked
description: "Bind and validate Gin route path parameters into a struct with ShouldBindUri, uri struct tags and binding validators such as uuid."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-uri.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bind URI path parameters with ShouldBindUri

Goal: map route parameters like `/:name/:id` into a struct and validate them in one call.

```go
type Person struct {
  ID   string `uri:"id" binding:"required,uuid"`
  Name string `uri:"name" binding:"required"`
}

func main() {
  route := gin.Default()
  route.GET("/:name/:id", func(c *gin.Context) {
    var person Person
    if err := c.ShouldBindUri(&person); err != nil {
      c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
      return
    }
    c.JSON(http.StatusOK, gin.H{"name": person.Name, "uuid": person.ID})
  })
  route.Run(":8088")
}
```

Test:

```sh
curl http://localhost:8088/thinkerou/987fbc97-4bed-5078-9f07-9141ba07c9f3
# {"name":"thinkerou","uuid":"987fbc97-4bed-5078-9f07-9141ba07c9f3"}

curl http://localhost:8088/thinkerou/not-uuid
# {"error":"Key: 'Person.ID' Error:Field validation for 'ID' failed on the 'uuid' tag"}
```

## Gotcha
The `uri` tag name must equal the parameter name in the route definition: `:id` in the route pairs with `uri:"id"`. This is handy for resource IDs or slugs you want validated and type-checked before use; combined with `binding` tags such as `required,uuid`, one call checks all path parameters.

## Related
Path parameters themselves are declared in the route (`/:name/:id`). Use ShouldBindUri when you want them in a struct instead of calling `c.Param`. Failed validation returns the error to your handler, which here responds with HTTP 400 and the error text. See also gin-bind-vs-shouldbind for the Must-bind versus Should-bind difference.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind Uri (ShouldBindUri, uri tag, required,uuid, curl outputs).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
