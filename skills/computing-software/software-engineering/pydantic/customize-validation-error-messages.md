---
id: computing-software.software-engineering.pydantic.customize-validation-error-messages
name: customize-validation-error-messages
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-error-details, custom-error-messages, translation, error-loc, validation-error, errors]
level: practitioner
status: docs-checked
description: "Rewrite Pydantic ValidationError messages by type (for translation) and reshape the loc tuple into a dotted path, using a converter over e.errors()."
sources:
  - https://docs.pydantic.dev/latest/errors/errors/
  - https://docs.pydantic.dev/latest/version-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: present Pydantic errors with your own wording or `loc` format by post-processing `ValidationError.errors()`.

## Custom messages by error type
Build a map from error `type` to a template, then rewrite `msg`. Templates are filled from the error's `ctx`:

```python
from pydantic_core import ErrorDetails
from pydantic import BaseModel, HttpUrl, ValidationError

CUSTOM_MESSAGES = {
    'int_parsing': 'This is not an integer!',
    'url_scheme': 'Hey, use the right URL scheme! I wanted {expected_schemes}.',
}

def convert_errors(e: ValidationError, custom_messages: dict[str, str]) -> list[ErrorDetails]:
    new_errors: list[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error['type'])
        if custom_message:
            ctx = error.get('ctx')
            error['msg'] = custom_message.format(**ctx) if ctx else custom_message
        new_errors.append(error)
    return new_errors
```
For `Model(a='wrong', b='ftp://example.com')` with `b: HttpUrl`, the `url_scheme` error has `ctx` `{'expected_schemes': "'http' or 'https'"}`, so the message becomes `Hey, use the right URL scheme! I wanted 'http' or 'https'.`

The page notes a common use is translating messages: replace `CUSTOM_MESSAGES` with a dictionary of translations.

## Custom `loc` representation
By default `e.errors()` gives `loc` as a tuple, e.g. `('items', 1, 'value')`. Convert it:

```python
def loc_to_dot_sep(loc: tuple[str | int, ...]) -> str:
    path = ''
    for i, x in enumerate(loc):
        if isinstance(x, str):
            if i > 0:
                path += '.'
            path += x
        elif isinstance(x, int):
            path += f'[{x}]'
        else:
            raise TypeError('Unexpected type')
    return path

def convert_errors(e: ValidationError) -> list[dict]:
    new_errors = e.errors()
    for error in new_errors:
        error['loc'] = loc_to_dot_sep(error['loc'])
    return new_errors
```
`('items', 1, 'value')` becomes `'items[1].value'`.

## Notes
- Errors without a `ctx` key (e.g. `int_parsing`) must not be formatted with `**ctx`; the code above guards for this.
- The version policy says `msg`, `ctx` and `loc` may change in minor releases while `type` will not, so key your map on `type`.

## Checked

Checked 2026-11-07. Compared every claim with the validation errors page (errors/errors.md) and the version policy (version-policy.md): `errors()` and `ErrorDetails` keys, the `CUSTOM_MESSAGES` converter with `url_scheme` ctx `expected_schemes`, translation use case, the `loc_to_dot_sep` converter and its `items[1].value` result, and that `msg`, `ctx` and `loc` may change in minor releases while `type` will not. All confirmed; nothing removed.

Method: documentation only; no commands were run.
