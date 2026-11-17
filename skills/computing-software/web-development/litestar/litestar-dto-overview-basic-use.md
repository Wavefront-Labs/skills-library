---
id: computing-software.web-development.litestar.litestar-dto-overview-basic-use
name: litestar-dto-overview-basic-use
category: computing-software
field: web-development
product: litestar
tags: [litestar, dto, return-dto, data-transfer-object, layered, codegen, dataclass-dto, handlers]
level: practitioner
status: docs-checked
description: "Attach DTOs to Litestar handlers and layers with dto and return_dto, understand the data flow, and toggle the codegen backend."
sources: [https://docs.litestar.dev/latest/usage/dto/index.html, https://docs.litestar.dev/latest/usage/dto/0-basic-use.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar DTOs: overview and basic use

Goal: control how client data becomes handler data and how returned data is encoded.

## Method

Data flow per request: encoded bytes go to the DTO (multipart and URL-encoded data is first decoded into Python built-ins); the DTO does primitive type validation and marshals into the type declared on the handler; the handler returns data; the DTO marshals it into a type Litestar can encode; Litestar encodes it to bytes.

Two parameters exist on every layer (app, router, controller, handler):
- `dto`: decodes inbound data for the `data` kwarg. If no `return_dto` is declared it also encodes the return data.
- `return_dto`: encodes handler return data; falls back to `dto` if absent.

Both must be classes conforming to `AbstractDTO`.

```python
UserDTO = DataclassDTO[User]

@post(dto=UserDTO, sync_to_thread=False)
def create_user(data: JSONBody[User]) -> User:
    return data
```

Separate read and write DTOs on a controller; `return_dto=None` disables the implicit return DTO for one route:

```python
class UserWriteDTO(DataclassDTO[User]):
    config = DTOConfig(exclude={"id"})

class UserReadDTO(DataclassDTO[User]): ...

class UserController(Controller):
    dto = UserWriteDTO
    return_dto = UserReadDTO

    @delete("/{user_id:uuid}", return_dto=None, sync_to_thread=False)
    def delete_user(self, user_id: FromPath[UUID]) -> None: ...
```

The DTO applied is the one nearest the handler in the ownership chain. With `dto=UserDTO, return_dto=None` the handler must return something Litestar encodes itself (the page's example returns `bytes`).

Codegen backend: stable and on by default since 2.8.0 (introduced 2.2.0). Disable it per DTO:

```python
class FooDTO(DataclassDTO[Foo]):
    config = DTOConfig(experimental_codegen_backend=False)
```

`ExperimentalFeatures.DTO_CODEGEN` is deprecated and will be removed in 3.0.0.

## Gotchas

- Setting `return_dto=None` means you manage response encoding yourself.

## Verify

In the page's controller example, handlers with a `data` kwarg are converted by `UserWriteDTO`, all returns by `UserReadDTO`, except `delete`, which has `return_dto=None`.

## Checked

2026-11-07. Read the full cited page(s) (usage/dto/index.html, usage/dto/0-basic-use.html) and the example files they include, and confirmed the claims in this skill against that text. Corrected the DTO_CODEGEN removal wording to 'will be removed in 3.0.0'.

Method: documentation only; no commands were run.
