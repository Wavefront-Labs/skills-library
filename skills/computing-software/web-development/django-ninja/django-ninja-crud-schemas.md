---
id: computing-software.web-development.django-ninja.django-ninja-crud-schemas
name: django-ninja-crud-schemas
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, crud-schemas, modelschema, schema, response, status, patchdict, django-orm]
level: practitioner
status: docs-checked
description: "Build CRUD endpoints in Django Ninja with Schema or ModelSchema, response status-code maps, Status() for multiple outcomes and get_object_or_404."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/quickstart/models-and-schemas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRUD from a Django model with schemas

Goal: expose a model through list/detail/create/update/delete endpoints.

## Schemas

A schema is a Pydantic model describing data in or out. Use separate in/out classes so clients cannot set `id`:

```python
from ninja import ModelSchema
from events.models import Event


class EventIn(ModelSchema):
    class Meta:
        model = Event
        fields = ["title", "city", "starts_at", "capacity"]


class EventOut(ModelSchema):
    class Meta:
        model = Event
        fields = ["id", "title", "city", "starts_at", "capacity"]
```

`ModelSchema` takes types, defaults and constraints (e.g. `max_length=200`) from the model. Hand-written `Schema` subclasses (`from ninja import Schema`) behave the same and can be mixed freely; use them for non-table data such as login payloads.

## Read

```python
from django.shortcuts import get_object_or_404

@api.get("/events", response=list[EventOut])
def list_events(request):
    return Event.objects.all()

@api.get("/events/{event_id}", response=EventOut)
def get_event(request, event_id: int):
    return get_object_or_404(Event, id=event_id)
```
Return querysets and model instances directly; only fields in the response schema are sent. A missing object via `get_object_or_404` becomes a `404` JSON response.

## Create, update, delete

A schema-typed argument is read from the JSON body:

```python
@api.post("/events", response={201: EventOut})
def create_event(request, payload: EventIn):
    return Event.objects.create(**payload.dict())

@api.put("/events/{event_id}", response=EventOut)
def update_event(request, event_id: int, payload: EventIn):
    event = get_object_or_404(Event, id=event_id)
    for attr, value in payload.dict().items():
        setattr(event, attr, value)
    event.save()
    return event

@api.delete("/events/{event_id}", response={204: None})
def delete_event(request, event_id: int):
    get_object_or_404(Event, id=event_id).delete()
```

`response={201: EventOut}` maps status to schema; with one code listed, every response gets that code. A body missing required fields returns an error listing every problem (`"type": "missing"`, `"loc": ["body", "payload", "city"]`).

## Several status codes

```python
from ninja import Schema, Status

@api.post("/events", response={201: EventOut, 409: Conflict})
def create_event(request, payload: EventIn):
    clash = Event.objects.filter(city=payload.city, starts_at=payload.starts_at).first()
    if clash:
        return Status(409, {"message": "Another event is already scheduled then", "existing_id": clash.id})
    return Status(201, Event.objects.create(**payload.dict()))
```
Each response is validated against the schema for its code.

## Partial updates

For `PATCH`, use `PatchDict[EventIn]` (see the Request Body guide).

## Checked

2026-11-07: Confirmed against quickstart/models-and-schemas.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
