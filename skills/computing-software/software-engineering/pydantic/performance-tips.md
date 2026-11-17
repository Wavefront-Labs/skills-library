---
id: computing-software.software-engineering.pydantic.performance-tips
name: performance-tips
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-performance-tips, typeadapter, tagged-union, typeddict, failfast, optimization, python]
level: practitioner
status: docs-checked
description: "Speed up Pydantic validation: model_validate_json, reuse TypeAdapter, list over Sequence, discriminated unions, TypedDict, avoid wrap validators, FailFast."
sources:
  - https://docs.pydantic.dev/latest/concepts/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pydantic performance tips

Goal: remove avoidable validation cost. The page's caveat: in most cases Pydantic is not your bottleneck; apply these only if you are sure it is necessary.

1. **Use `model_validate_json()`, not `model_validate(json.loads(...))`.** The latter parses in Python, builds a dict, then validates. Exception: with a `'before'` or `'wrap'` model validator the two-step form may be faster.

2. **Instantiate `TypeAdapter` once.** Each instantiation builds a new validator and serializer. Build it at module level, not inside a function that is called repeatedly:

```python
adapter = TypeAdapter(list[int])   # module level

def my_func():
    ...  # use adapter
```

3. **Concrete containers.** `Sequence` triggers `isinstance(value, Sequence)` and tries several sequence types; use `list` or `tuple` if you know it. Likewise `dict` rather than `Mapping`.

4. **Use `Any` to skip validation** when you do not need it: `a: Any` keeps the value unchanged.

5. **Do not subclass primitives to attach data.** Instead of `class CompletedStr(str)` with extra attributes, use a model:

```python
class CompletedModel(BaseModel):
    s: str
    done: bool = False
```

6. **Tagged (discriminated) unions, not plain unions.** Add a `Literal` tag field and `Field(discriminator='el_type')`:

```python
class Html(BaseModel):
    contents: DivModel | SpanModel | ButtonModel | InputModel = Field(
        discriminator='el_type'
    )
```

7. **`TypedDict` over nested models.** The page's simple benchmark shows `TypedDict` (via `TypeAdapter`) about 2.5x faster than nested models.

8. **Avoid wrap validators** when performance matters: they require data to be materialised in Python.

9. **`FailFast` (v2.8+).** Fail on the first bad item in a sequence, trading error visibility for speed:

```python
ta = TypeAdapter(Annotated[list[bool], FailFast()])
ta.validate_python([True, 'invalid', False, 'also invalid'])
# 1 validation error for list[bool]; only index 1 is reported
```

## Checked

Checked 2026-11-07. Compared every claim with the performance page (concepts/performance.md): the not-a-bottleneck caveat, `model_validate_json()` and its before/wrap exception, `TypeAdapter` built once, `Sequence` versus `list` / `tuple` and `Mapping` versus `dict`, `Any`, primitive subclasses, tagged unions, the roughly 2.5x `TypedDict` benchmark, wrap validators, and `FailFast` from v2.8. All confirmed; nothing removed.

Method: documentation only; no commands were run.
