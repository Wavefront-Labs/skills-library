---
id: computing-software.web-development.litestar.litestar-parameter-validation
name: litestar-parameter-validation
category: computing-software
field: web-development
product: litestar
tags: [litestar, parameter, validation, constraints, aliasing, layered-parameters, openapi, enum-schema]
level: practitioner
status: docs-checked
description: "Constrain, alias and layer Litestar request parameters, and give enum parameters distinct OpenAPI schema components."
sources: [https://docs.litestar.dev/latest/usage/routing/parameters.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar parameter validation, aliasing and layers

Goal: validate parameters, rename them, share them across layers and control OpenAPI output.

## Method

Constraints: `gt`, `ge`, `lt`, `le`, `multiple_of`, `min_length`, `max_length`, `min_items`, `max_items`, `pattern`. A violation raises `ValidationException`; constraints appear in the OpenAPI schema.

```python
@get("/")
def index(param: Annotated[int, QueryParameter(gt=5)]) -> dict[str, int]: ...
```

Aliasing: pass `name="..."` to the specifier (`QueryParameter`, `HeaderParameter`, `CookieParameter`, `PathParameter`). With `QueryParameter(name="camelCase")` on `snake_case`, `/?camelCase=foo` arrives as `snake_case="foo"`.

OpenAPI metadata: specifiers can extend or alter the schema, for example title, description and examples.

Enum schemas: one schema component exists per enum, so a changed `description` would apply to every parameter using it. Add `schema_component_key` for a separate component:

```python
q1: Annotated[MyEnum, QueryParameter(description="This is q1", schema_component_key="q1")],
q2: FromQuery[MyEnum],
```

Without the keys all three parameters share the "MyEnum" component and the first processed description wins.

Layered parameters: use the `parameters` argument or attribute on `Litestar`, `Router`, `Controller`:

```python
class MyController(Controller):
    parameters = {"controller_param": QueryParameter(annotation=int, lt=100)}

router = Router(path="/router", route_handlers=[MyController],
    parameters={"router_param": HeaderParameter(annotation=str, name="MyHeader", pattern="^[a-zA-Z]$")})

app = Litestar(route_handlers=[router],
    parameters={"app_param": CookieParameter(annotation=str, name="special-cookie", required=False)})
```

- A parameter declared only on a layer is still extracted and validated even if the handler never declares it.
- The handler can redeclare it to take the layer's declaration (`router_param: FromHeader[str]`) or tighten it (`Annotated[int, QueryParameter(lt=50)]`).
- If a layer sets `required=False`, the handler must give a default.

## Verify

With `QueryParameter(gt=5)`, a value that does not satisfy the constraint raises `ValidationException`, per the page.

## Checked

2026-11-07. Read the full cited page(s) (usage/routing/parameters.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
