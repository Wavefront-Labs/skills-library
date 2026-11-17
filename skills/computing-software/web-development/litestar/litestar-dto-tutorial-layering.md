---
id: computing-software.web-development.litestar.litestar-dto-tutorial-layering
name: litestar-dto-tutorial-layering
category: computing-software
field: web-development
product: litestar
tags: [litestar, dto, dto-tutorial, max-nested-depth, collection-exclude, dtodata, layered-dto, controller]
level: practitioner
status: docs-checked
description: "Litestar DTO tutorial steps for excluding from nested collections, max_nested_depth, write DTOs that omit id with DTOData, and DTOs declared on controllers."
sources: [https://docs.litestar.dev/latest/tutorials/dto-tutorial/03-nested-collection-exclude.html, https://docs.litestar.dev/latest/tutorials/dto-tutorial/04-max-nested-depth.html, https://docs.litestar.dev/latest/tutorials/dto-tutorial/07-read-only-fields.html, https://docs.litestar.dev/latest/tutorials/dto-tutorial/10-layered-dto-declarations.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar DTO tutorial: collections, depth, write DTOs, layers

Goal: configure DTOs for self-referencing models and for create/update flows, then declare them once on a controller.

## Method

1. Collections: use the index of the type parameter in the dotted path. `a.0.b` excludes `b` from the first type parameter of `a`, `a.1.b` the second. For `children: list[Person]`:

```python
DTOConfig(exclude={"email", "address.street", "children.0.email", "children.0.address"})
```

2. Depth: `max_nested_depth` limits nested objects included in the output. Default is `1`, so `children` of items inside `Person.children` are omitted. Set `DTOConfig(..., max_nested_depth=2)` to see those (empty) collections.

3. Write DTO: exclude server-generated fields from client input and give the handler the DTO via `dto=`:

```python
class WriteDTO(DataclassDTO[Person]):
    config = DTOConfig(exclude={"id"})

@post("/person", dto=WriteDTO, return_dto=ReadDTO, sync_to_thread=False)
def create_person(data: JSONBody[Person]) -> Person: ...
```

If `id` is a required field of the model, this errors, because the DTO cannot construct `Person` without it. Use `DTOData` instead: type the parameter `JSONBody[DTOData[Person]]` and call `data.create_instance(id=1)`; for updates, `data.update_instance(person)`.

4. Layers: DTOs can be set on any layer. Put them on a `Controller`:

```python
class PersonController(Controller):
    dto = WriteDTO
    return_dto = ReadDTO

    @patch("/person/{person_id:int}", dto=PatchDTO, sync_to_thread=False)
    def patch_person(...) -> Person: ...
```

with `PatchDTO` using `DTOConfig(exclude={"id"}, partial=True)`. A handler-level `dto` overrides the controller-level `dto` for that handler.

## Verify

Request the endpoint and compare with the tutorial behaviour: with the default depth the nested `children.0.children` field is absent; with `max_nested_depth=2` empty `children` collections appear.

## Checked

2026-11-07. Read the full cited page(s) (tutorials/dto-tutorial/03-nested-collection-exclude.html, tutorials/dto-tutorial/04-max-nested-depth.html, tutorials/dto-tutorial/07-read-only-fields.html, tutorials/dto-tutorial/10-layered-dto-declarations.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
