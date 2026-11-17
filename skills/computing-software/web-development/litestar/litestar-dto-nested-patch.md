---
id: computing-software.web-development.litestar.litestar-dto-nested-patch
name: litestar-dto-nested-patch
category: computing-software
field: web-development
product: litestar
tags: [litestar, abstract-dto, dto-data, patch, max-nested-depth, partial, pagination, wrapper]
level: practitioner
status: docs-checked
description: "Control nested DTO depth, build instances with DTOData, support PATCH with partial=True, and wrap return data in generics, pagination or Response."
sources: [https://docs.litestar.dev/latest/usage/dto/1-abstract-dto.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar DTO nested fields, DTOData, PATCH and wrapped returns

Goal: handle related models, server-set fields, partial updates and envelopes.

## Method

Nested depth: `DTOConfig(max_nested_depth=...)`, default `1`. Set `0` on an inbound DTO so related items are not parsed; with the default on the return DTO, `b` is included but `b.a` is not.

DTOData: when a field is excluded for clients and has no model default, inject `DTOData` and build the instance yourself:

```python
class UserWriteDTO(DataclassDTO[User]):
    config = DTOConfig(exclude={"id"})

@post("/users", dto=UserWriteDTO, return_dto=None, sync_to_thread=False)
def create_user(data: JSONBody[DTOData[User]]) -> User:
    return data.create_instance(id=uuid4())
```

Nested values use double underscores: `create_instance(id=1, address__id=2)` supplies `id` on the person and on the nested `address`.

PATCH: exclude `id` and set `partial=True`; use `update_instance`:

```python
class PatchDTO(DataclassDTO[Person]):
    config = DTOConfig(exclude={"id"}, partial=True)

@patch("/person/{person_id:uuid}", dto=PatchDTO, return_dto=None, sync_to_thread=False)
def update_person(person_id: FromPath[UUID], data: JSONBody[DTOData[Person]]) -> Person:
    return data.update_instance(database[person_id])
```

Wrapping return data: use a generic wrapper such as

```python
@dataclass
class WithCount(Generic[T]):
    count: int
    data: List[T]
```

with `@get("/users", dto=UserDTO) def get_users() -> WithCount[User]`. The DTO finds the attribute holding the data and serializes it.

Pagination: `ClassicPagination[User]` works out of the box; the DTO operates on `items` (alongside `page_size`, `total_pages`, `current_page`).

Response: `Response[User]` is handled too; the DTO serializes `content`, and headers such as `{"X-Total-Count": "1"}` stay available.

## Gotchas

- The wrapper type returned must be natively encodable by Litestar, and exactly one of its type arguments must be a type the DTO supports.
- At least one wrapper type parameter must describe an instance attribute populated with the data.

## Verify

Following the page, `PATCH /person/<uuid>` with `{"name":"Peter Pan"}` changes only the name from `"Peter"` and returns the full object.

## Checked

2026-11-07. Read the full cited page(s) (usage/dto/1-abstract-dto.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
