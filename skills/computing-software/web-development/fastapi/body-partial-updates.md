---
id: computing-software.web-development.fastapi.body-partial-updates
name: body-partial-updates
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, request-body, put, patch, exclude-unset, model-copy, jsonable-encoder]
level: advanced
status: docs-checked
description: "Implement PUT replace versus PATCH partial updates in FastAPI using model_dump(exclude_unset=True), model_copy(update=...) and jsonable_encoder."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/body-updates.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PUT versus PATCH updates

Goal: update stored data without clobbering fields.

## PUT replaces
Use `jsonable_encoder` to convert input to JSON-storable data (e.g. `datetime` to `str`). With PUT, fields missing from the body take the model defaults: a stored `tax` of 20.2 is overwritten by the model default 10.5 if the body omits it.

## PATCH partial update recipe
1. Retrieve stored data and put it in a Pydantic model.
2. `item.model_dump(exclude_unset=True)` gives a dict of only the values the client actually sent.
3. `stored_item_model.model_copy(update=update_data)` copies the stored model with those changes.
4. Convert the copy with `jsonable_encoder` and save.
5. Return the updated model.

## Notes
- PATCH is less known; many teams use only PUT. FastAPI imposes nothing, and the same technique works with PUT.
- The input model is still validated, so for partial updates make all attributes optional (default or `None`). Keep separate models for update and creation; see the extra-models skill.

## Verify
Send a body with one field and confirm others keep their stored values.

## Checked

Every claim above was read in the FastAPI body updates tutorial page (PUT replace warning with tax 20.2 and 10.5, PATCH, exclude_unset, model_copy update, jsonable_encoder). Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
