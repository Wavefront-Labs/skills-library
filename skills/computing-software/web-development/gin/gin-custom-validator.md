---
id: computing-software.web-development.gin.gin-custom-validator
name: gin-custom-validator
category: computing-software
field: web-development
product: gin
tags: [gin, validation, custom-validator, registervalidation, validator-v10, gtfield, binding]
level: practitioner
status: docs-checked
description: "Register a custom go-playground validator function in Gin via binding.Validator.Engine and RegisterValidation, then use it in a binding tag."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/custom-validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Register a custom validator in Gin

Goal: add your own validation rule (here `bookabledate`, rejecting past dates) usable in `binding` tags.

```go
import (
  "github.com/gin-gonic/gin/binding"
  "github.com/go-playground/validator/v10"
)

type Booking struct {
  CheckIn  time.Time `form:"check_in" binding:"required,bookabledate" time_format:"2006-01-02"`
  CheckOut time.Time `form:"check_out" binding:"required,gtfield=CheckIn,bookabledate" time_format:"2006-01-02"`
}

var bookableDate validator.Func = func(fl validator.FieldLevel) bool {
  date, ok := fl.Field().Interface().(time.Time)
  if ok {
    if time.Now().After(date) {
      return false
    }
  }
  return true
}

func main() {
  route := gin.Default()
  if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
    v.RegisterValidation("bookabledate", bookableDate)
  }
  route.GET("/bookable", getBookable)
  route.Run(":8085")
}

func getBookable(c *gin.Context) {
  var b Booking
  if err := c.ShouldBindWith(&b, binding.Query); err == nil {
    c.JSON(http.StatusOK, gin.H{"message": "Booking dates are valid!"})
  } else {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
  }
}
```

Steps: write a `validator.Func`, type-assert `binding.Validator.Engine()` to `*validator.Validate`, call `RegisterValidation(tagName, fn)`, then reference the tag name in `binding`.

Test: `curl "http://localhost:8085/bookable?check_in=2118-04-16&check_out=2118-04-17"` returns `{"message":"Booking dates are valid!"}`. With check_out before check_in the response is an error for the `gtfield` tag on 'Booking.CheckOut'.

## Gotchas
- Built-in validators include `required`, `email`, `min`, `max`.
- For cross-field rules beyond single-field checks, the docs point to struct-level validations (example in gin-gonic/examples, struct-lvl-validations).

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Custom validators (RegisterValidation, bookabledate, gtfield error, struct-level tip).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
