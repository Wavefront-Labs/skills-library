---
id: computing-software.web-development.gin.gin-bind-text-unmarshaler
name: gin-bind-text-unmarshaler
category: computing-software
field: web-development
product: gin
tags: [gin, textunmarshaler, bindunmarshaler, unmarshalparam, parser, custom-binding, form-tag]
level: advanced
status: docs-checked
description: "Override Gin field binding with encoding.TextUnmarshaler via parser=encoding.TextUnmarshaler, or the binding.BindUnmarshaler interface (UnmarshalParam)."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-custom-unmarshaler.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom unmarshalers for Gin binding

Goal: control how a form/uri value is converted into a custom type.

## Option 1: encoding.TextUnmarshaler
Implement `UnmarshalText` and add `parser=encoding.TextUnmarshaler` to the `uri`/`form` tag.

```go
type Birthday string

func (b *Birthday) UnmarshalText(text []byte) error {
  *b = Birthday(strings.Replace(string(text), "-", "/", -1))
  return nil
}

var request struct {
  Birthday         Birthday   `form:"birthday,parser=encoding.TextUnmarshaler"`
  Birthdays        []Birthday `form:"birthdays,parser=encoding.TextUnmarshaler" collection_format:"csv"`
  BirthdaysDefault []Birthday `form:"birthdaysDef,default=2020-09-01;2020-09-02,parser=encoding.TextUnmarshaler" collection_format:"csv"`
}
// handler: _ = ctx.BindQuery(&request); ctx.JSON(200, request)
```

`curl 'localhost:8088/test?birthday=2000-01-01&birthdays=2000-01-01,2000-01-02'` returns `{"Birthday":"2000/01/01","Birthdays":["2000/01/01","2000/01/02"],"BirthdaysDefault":["2020/09/01","2020/09/02"]}`.

## Option 2: BindUnmarshaler
When a type already implements `encoding.TextUnmarshaler` but you want Gin to bind it differently (for example to change the returned error message), implement `binding.BindUnmarshaler`:

```go
func (b *Birthday) UnmarshalParam(param string) error {
  *b = Birthday(strings.Replace(param, "-", "/", -1))
  return nil
}
var _ binding.BindUnmarshaler = (*Birthday)(nil)
```

The tags are then plain, for example `form:"birthday"`.

## Gotchas
- If `parser=encoding.TextUnmarshaler` is set on a type that does not implement it, Gin ignores it and uses default binding.
- If a type implements both interfaces, Gin uses `BindUnmarshaler` unless the tag specifies `parser=encoding.TextUnmarshaler`.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind custom unmarshaler (parser=encoding.TextUnmarshaler, BindUnmarshaler/UnmarshalParam, both notes, curl output).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
