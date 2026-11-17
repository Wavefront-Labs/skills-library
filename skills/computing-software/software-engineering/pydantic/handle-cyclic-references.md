---
id: computing-software.software-engineering.pydantic.handle-cyclic-references
name: handle-cyclic-references
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-cyclic-references, recursion-loop, wrap-validator, field-serializer, circular-reference, recursion-depth]
level: advanced
status: docs-checked
description: "Handle cyclic data in Pydantic: catch the recursion_loop ValidationError in a wrap field_validator and the Circular reference ValueError in a wrap field_serializer."
sources:
  - https://docs.pydantic.dev/latest/examples/cyclic_references/
  - https://docs.pydantic.dev/latest/errors/validation_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: drop cyclic references during validation or serialization instead of failing.

## Behaviour
Pydantic detects cyclic references in validation input and raises a `ValidationError` with error type `recursion_loop` rather than a `RecursionError`. During serialization it raises a `ValueError` immediately. Because the validation error is raised without actually exceeding the maximum recursion depth, you can catch it without worrying about the limited remaining recursion depth.

The error reference example: `x: list['Model']` with `d = {'x': []}; d['x'].append(d)` gives `recursion_loop`. A separate type, `recursion_depth_exceeded`, is for input nested deeper than allowed (the maximum varies between platforms and may change between releases).

## Validation: wrap validator
```python
def is_recursion_validation_error(exc: ValidationError) -> bool:
    errors = exc.errors()
    return len(errors) == 1 and errors[0]['type'] == 'recursion_loop'

@contextmanager
def suppress_recursion_validation_error() -> Generator[None]:
    try:
        yield
    except ValidationError as exc:
        if not is_recursion_validation_error(exc):
            raise exc

class Node(BaseModel):
    id: int
    children: list[Node] = field(default_factory=list)

    @field_validator('children', mode='wrap')
    @classmethod
    def drop_cyclic_references(cls, children, h):
        try:
            return h(children)
        except ValidationError as exc:
            if not (is_recursion_validation_error(exc) and isinstance(children, list)):
                raise exc
            value_without_cyclic_refs = []
            for child in children:
                with suppress_recursion_validation_error():
                    value_without_cyclic_refs.extend(h([child]))
            return h(value_without_cyclic_refs)
```
For the graph 1 -> 2 -> 3 -> 1, `Node.model_validate(node_data)` prints `id=1 children=[Node(id=2, children=[Node(id=3, children=[])])]`.

## Serialization: wrap serializer
`TypeAdapter(dict).dump_json(node_data)` on cyclic data raises `ValueError` with `Error serializing to JSON: ValueError: Circular reference detected (id repeated)`. Handle it with `@field_serializer('children', mode='wrap')` taking `(self, children, handler: SerializerFunctionWrapHandler)`: call `handler(children)`; on a `ValueError` whose message does not start with `Circular reference`, re-raise; otherwise serialize each child with `handler([node])` and, for a child that still raises the circular error, append `{'id': node.id}`.

The page's example uses `pydantic.dataclasses.dataclass` nodes and `TypeAdapter(Node).dump_python(nodes[0])`, which yields `{'id': 1, 'children': [{'id': 2, 'children': [{'id': 3, 'children': [{'id': 1}]}]}]}`.

## Checked

Checked 2026-11-07. Compared every claim with the cyclic references example (examples/cyclic_references.md) and the validation errors page (errors/validation_errors.md): `recursion_loop` instead of `RecursionError`, the immediate `ValueError` on serialization, the wrap validator and serializer code, the printed results, and the `recursion_depth_exceeded` note. All confirmed; nothing removed.

Method: documentation only; no commands were run.
