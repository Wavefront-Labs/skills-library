---
id: computing-software.web-development.django-ninja.django-ninja-schema-config-camelcase-extra
name: django-ninja-schema-config-camelcase-extra
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, schema-config, model-config, alias-generator, camelcase, extra-forbid, by-alias]
level: practitioner
status: docs-checked
description: "Configure Django Ninja schemas with model_config: camelCase via alias_generator, populate_by_name, by_alias, extra=forbid, validate_assignment."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/schema-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema configuration (model_config)

Set Pydantic's `model_config` on the schema:

```python
from pydantic import ConfigDict
from ninja import Schema

class UserSchema(Schema):
    model_config = ConfigDict(extra="forbid")
    id: int
    email: str
```

`Schema` sets `from_attributes=True`; Pydantic merges a subclass's config with inherited config, so you only repeat it to turn it off. Works on `ModelSchema` and `create_schema()` classes too.

## camelCase output

Three pieces are needed:

1. `alias_generator=to_camel` (from `pydantic.alias_generators`).
2. `populate_by_name=True`, otherwise only the alias (`isStaff`) is accepted as input, which breaks `from_orm()`: Django objects and dicts are still keyed by `is_staff` (you get "field required" errors).
3. `by_alias=True` on the operation or `Router`; without it output uses plain field names.

```python
class UserSchema(ModelSchema):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    class Meta:
        model = User
        fields = ["id", "email", "is_staff"]

@api.get("/users", response=list[UserSchema], by_alias=True)
def get_users(request):
    return User.objects.all()
```

Output: `{"id": 1, "email": "tim@apple.com", "isStaff": true}`. `to_pascal`, `to_snake`, or any function work as generators. Request bodies are always documented in OpenAPI using aliases regardless of `by_alias`.

## Reject unknown fields

Default is `extra="ignore"` (unknown keys silently dropped). `extra="forbid"` makes a payload like `{"title": "Write docs", "typo_field": true}` fail with a `422` and an `extra_forbidden` error. `extra="allow"` keeps them as attributes. `extra` affects input only, not response output.

## validate_assignment

`ConfigDict(validate_assignment=True)` revalidates attribute assignment: `task.title = 123` raises `pydantic.ValidationError`.

Other options (`str_strip_whitespace`, `frozen`, `json_schema_extra`, ...) behave as in plain Pydantic.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/schema-config.md from GitHub. Confirmed against the whole page: model_config, from_attributes inheritance, camelCase with alias_generator, populate_by_name and by_alias, extra modes, validate_assignment and other options. Nothing removed.

Method: documentation only; no commands were run.
