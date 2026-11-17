---
id: computing-software.web-development.litestar.litestar-dto-field-marking
name: litestar-dto-field-marking
category: computing-software
field: web-development
product: litestar
tags: [litestar, abstract-dto, dto-config, dto-field, exclude, rename-fields, private, read-only]
level: practitioner
status: docs-checked
description: "Hide, exclude, rename and mark fields private or read-only in Litestar DTOs with dto_field and DTOConfig."
sources: [https://docs.litestar.dev/latest/usage/dto/1-abstract-dto.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar DTO field marking, exclusion and renaming

Goal: stop clients setting or seeing fields they should not.

## Method

DTO factories (`DataclassDTO`, `MsgspecDTO`, `PydanticDTO`, `SQLAlchemyDTO`) take the model as a generic argument, for example `UserDTO = SQLAlchemyDTO[User]`.

Marking with `dto_field` (from `litestar.dto`):
- `"private"`: never parsed from client data and never serialized into return data.
- `"read-only"`: not parsed from client data, but returned.
- How you attach the mark depends on the library: SQLAlchemy uses `mapped_column(info=dto_field("private"))`; `DataclassDTO` expects it in the `metadata` parameter of `dataclasses.field`.
- A leading underscore on a field name makes it private by default; set `DTOConfig.underscore_fields_private` to `False` to override.

Excluding: `DTOConfig(exclude={...})` takes dotted paths. Nested models and list items use paths such as:

```python
config = DTOConfig(exclude={"id", "address.id", "address.street", "pets.0.id", "pets.0.user_id"})
```

For generic types, the index chooses the type parameter: `a.0.b` is the first type parameter of `a`, `a.1.b` the second.

Renaming, applied through `Annotated`:

```python
config = DTOConfig(rename_fields={"name": "userName"})
UserDTO = SQLAlchemyDTO[Annotated[User, config]]
```

Or rename everything with `rename_strategy`: `"camel"`, `"pascal"`, `"upper"`, `"lower"`, `"kebab"`, or a callable taking the field name and returning a string (for example `lambda x: f"-{x}-"`). Fields renamed through `rename_fields` are excluded from the strategy.

Unknown fields are silently ignored by default; `DTOConfig(forbid_unknown_fields=True)` returns a validation error response instead.

Attach with `@post("/users", dto=UserDTO)`. A DTO checks that the handler annotation is a subclass of its generic type; a mismatch raises `InvalidAnnotationException` at runtime.

## Verify

With `rename_fields={"name": "userName"}`, posting `{"userName": "Litestar User", ...}` sets `data.name`; with a `private` password and `read-only` created_at, neither appears on `data` even though the client sent them (the page's assertions).

## Checked

2026-11-07. Read the full cited page(s) (usage/dto/1-abstract-dto.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
