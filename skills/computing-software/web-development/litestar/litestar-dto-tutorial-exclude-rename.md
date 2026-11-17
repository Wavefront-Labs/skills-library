---
id: computing-software.web-development.litestar.litestar-dto-tutorial-exclude-rename
name: litestar-dto-tutorial-exclude-rename
category: computing-software
field: web-development
product: litestar
tags: [litestar, dto, dto-tutorial, dataclass-dto, dtoconfig, exclude, rename-fields, rename-strategy]
level: practitioner
status: docs-checked
description: "Use DataclassDTO and DTOConfig in Litestar to exclude top-level and nested fields from responses and to rename fields explicitly or by strategy."
sources: [https://docs.litestar.dev/latest/tutorials/dto-tutorial/01-simple-dto-exclude.html, https://docs.litestar.dev/latest/tutorials/dto-tutorial/02-nested-exclude.html, https://docs.litestar.dev/latest/tutorials/dto-tutorial/05-renaming-fields.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar DTO tutorial: exclude and rename fields

Goal: stop a handler leaking fields (such as an email) and control the serialized field names.

## Method

1. Define a DTO by subclassing `DataclassDTO[Model]` and setting a `config` attribute built from `DTOConfig`:

```python
from litestar.dto import DataclassDTO, DTOConfig

class ReadDTO(DataclassDTO[Person]):
    config = DTOConfig(exclude={"email"})

@get("/person/{name:str}", return_dto=ReadDTO, sync_to_thread=False)
def get_person(name: FromPath[str]) -> Person: ...
```

`return_dto=ReadDTO` makes the handler transfer its response through the DTO. Subclassing is only needed to attach the config; `ReadDTO = DataclassDTO[Person]` alone is also a valid specialized DTO.

2. Exclude from nested models with dotted paths: `exclude={"a.b"}` drops attribute `b` of the object on `a`. Example from the tutorial: `DTOConfig(exclude={"email", "address.street"})` where `Person.address` is an `Address` dataclass.

3. Rename explicitly with `rename_fields`, a dict of original name to new name:

```python
DTOConfig(exclude={"email"}, rename_fields={"address": "location"})
```

4. Or rename with `rename_strategy`. Supported values: `lower`, `upper`, `camel`, `pascal`. Example: `DTOConfig(rename_strategy="upper")`. You can also pass your own callable that receives the field name and returns the new name.

## Verify

Run the app, request `/person/peter`, and the response should lack the excluded field(s); with `rename_fields={"address": "location"}` the nested object appears under `location`, and with `rename_strategy="upper"` keys appear in upper case.

## Checked

2026-11-07. Read the full cited page(s) (tutorials/dto-tutorial/01-simple-dto-exclude.html, tutorials/dto-tutorial/02-nested-exclude.html, tutorials/dto-tutorial/05-renaming-fields.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
