---
id: computing-software.web-development.fastapi.path-enum-values
name: path-enum-values
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, path-parameters, enum, predefined-values, str-enum]
level: practitioner
status: docs-checked
description: "Restrict a FastAPI path parameter to predefined values with a str and Enum subclass, compare members, read .value and return enum members."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/path-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predefined path values with Enum

Goal: accept only a fixed set of values in a path parameter.

## Steps
1. Import `Enum` and create a class that inherits from both `str` and `Enum`. Inheriting from `str` lets the API docs know the values are strings and render correctly.
2. Add class attributes with the fixed values; those are the valid values.
3. Annotate the path parameter with the enum class.

The interactive docs then show the allowed values.

## Working with the member
- The parameter value arrives as an enumeration member. Compare it with members of your enum class.
- Get the underlying value (a `str` here) with `your_member.value`, e.g. `model_name.value`, or `ModelName.lenet.value` to reach the value `"lenet"`.
- You can return enum members, even nested in a JSON body such as a `dict`; they are converted to their values (strings) before reaching the client.

## Verify
Call the route with an allowed value and with an invalid one; the invalid one should produce a validation error and the docs dropdown should list the members.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
