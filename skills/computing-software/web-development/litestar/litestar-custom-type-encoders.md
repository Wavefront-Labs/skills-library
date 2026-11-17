---
id: computing-software.web-development.litestar.litestar-custom-type-encoders
name: litestar-custom-type-encoders
category: computing-software
field: web-development
product: litestar
tags: [litestar, custom-types, type-encoders, type-decoders, pydantic, msgspec, serialization]
level: practitioner
status: docs-checked
description: "Teach Litestar to encode and decode a custom type with type_encoders and type_decoders, or use an Annotated custom Pydantic type directly."
sources: [https://docs.litestar.dev/latest/usage/custom-types.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar custom types: type_encoders and type_decoders

Goal: serialize, deserialize and validate a type Litestar does not natively know.

## Method

- Litestar handles many standard types, dataclasses, Pydantic and msgspec. For a custom type, supply hook functions through `type_encoders` and `type_decoders`.
- Both parameters can be set on every layer; the layer closest to the route handler wins.
- `type_encoders` is a mapping `{Type: encode_hook}`; the hook turns the value into something known (here a str).
- `type_decoders` is a list of `(predicate, decode_hook)` tuples; the predicate takes the type and returns bool, the hook takes `(type, obj)` and returns the instance.

```python
def tenant_user_type_predicate(type: type) -> bool:
    return type is TenantUser


def tenant_user_enc_hook(u: TenantUser) -> Any:
    return u.to_combined_str()


def general_dec_hook(type: type, obj: Any) -> Any:
    if tenant_user_type_predicate(type):
        return TenantUser.from_string(obj)
    raise NotImplementedError(f"Encountered unknown type during decoding: {type!s}")


class UserAsset(Struct):  # msgspec
    user: TenantUser
    name: str


app = Litestar(
    [create_asset],
    type_encoders={TenantUser: tenant_user_enc_hook},
    type_decoders=[(tenant_user_type_predicate, general_dec_hook)],
)
```

## Custom Pydantic types

With Pydantic, no Litestar hooks are needed; annotate the type and use the model directly:

```python
PydAnnotatedTenantUser = Annotated[
    TenantUser,
    BeforeValidator(TenantUser.from_string),
    PlainSerializer(lambda x: x.to_combined_str(), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


class UserAsset(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user: PydAnnotatedTenantUser
    name: str
```

## Verify

POST `{"name":"SomeAsset","user":"TenantA_Somebody"}` with `Content-Type: application/json` to the `/asset` handler (`data: JSONBody[UserAsset]`); `data.user` is a `TenantUser` instance and the response serializes it back to `TenantA_Somebody`.

## Checked

2026-11-07. Read the full cited page(s) (usage/custom-types.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
