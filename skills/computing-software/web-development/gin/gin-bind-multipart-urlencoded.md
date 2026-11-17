---
id: computing-software.web-development.gin.gin-bind-multipart-urlencoded
name: gin-bind-multipart-urlencoded
category: computing-software
field: web-development
product: gin
tags: [gin, multipart, urlencoded, form-data, shouldbind, form-tag, login-form, binding]
level: intro
status: docs-checked
description: "Bind multipart/form-data or application/x-www-form-urlencoded bodies into a Gin struct with ShouldBind, form tags and binding:required."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/multipart-urlencoded-binding.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multipart and URL-encoded form binding

Goal: accept an HTML form submission, in either encoding, in one handler.

`ShouldBind` detects the Content-Type and binds `multipart/form-data` or `application/x-www-form-urlencoded`. Map field names with the `form` tag and enforce mandatory fields with `binding:"required"`.

```go
type LoginForm struct {
  User     string `form:"user" binding:"required"`
  Password string `form:"password" binding:"required"`
}

router.POST("/login", func(c *gin.Context) {
  var form LoginForm
  if err := c.ShouldBind(&form); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  if form.User == "user" && form.Password == "password" {
    c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
  } else {
    c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
  }
})
```

Test:

```sh
curl -X POST http://localhost:8080/login -F "user=user" -F "password=password"      # multipart
curl -X POST http://localhost:8080/login -d "user=user&password=password"          # urlencoded
# both: {"status":"you are logged in"}

curl -X POST http://localhost:8080/login -d "user=user"
# {"error":"Key: 'LoginForm.Password' Error:Field validation for 'Password' failed on the 'required' tag"}
```

## Notes
Wrong credentials return `{"status":"unauthorized"}` from the handler logic. A missing required field returns the validation error shown above.

## Related
This is the typical pattern for login forms, registration pages or any HTML form submission. For checkbox groups use gin-bind-html-checkboxes. The 400 error text names the struct field and the failed `required` tag.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Multipart/Urlencoded binding (ShouldBind detection, form and binding:required tags, curl outputs).
Removed or corrected: unconfirmed attribution of the error text to the validator.

Method: documentation only; no commands were run.
