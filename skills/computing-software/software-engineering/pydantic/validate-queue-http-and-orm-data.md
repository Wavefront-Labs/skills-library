---
id: computing-software.software-engineering.pydantic.validate-queue-http-and-orm-data
name: validate-queue-http-and-orm-data
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-queues-requests-orm, redis, rabbitmq, arq, httpx, sqlalchemy, from-attributes]
level: practitioner
status: docs-checked
description: "Serialize and validate Pydantic models across Redis, RabbitMQ and ARQ queues, httpx responses, and SQLAlchemy objects with from_attributes and aliases."
sources:
  - https://docs.pydantic.dev/latest/examples/queues/
  - https://docs.pydantic.dev/latest/examples/requests/
  - https://docs.pydantic.dev/latest/examples/orms/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use `model_dump_json()` / `model_validate_json()` (or `model_dump()` / `model_validate()`) at system boundaries.

The page model: `class User(BaseModel): id: int; name: str; email: EmailStr`.

## Redis queue
Push: `r.rpush(QUEUE_NAME, user_data.model_dump_json())`. Pop: `data = r.lpop(QUEUE_NAME)`; if data, `User.model_validate_json(data)`, else the queue is empty. The client is `redis.Redis(host='localhost', port=6379, db=0)`.

## RabbitMQ (pika)
Sender: `channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=user_data.model_dump_json())` after `channel.queue_declare(queue=QUEUE_NAME)`. Receiver callback signature `(ch, method, properties, body: bytes)`: `User.model_validate_json(body)`, then `ch.basic_ack(delivery_tag=method.delivery_tag)`; register with `channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)` and `channel.start_consuming()`.

If `model_validate_json` raises a `ValidationError`, the offending message may no longer be on the queue, so record failures as they happen, e.g.:
```python
import logfire
logfire.configure()
logfire.instrument_pydantic(record='failure')
```

## ARQ
Enqueue dicts: `await redis.enqueue_job('process_user', user1.model_dump())`. The job validates: `User.model_validate(user_data)`, signature `async def process_user(ctx: dict[str, Any], user_data: dict[str, Any])`. Worker config: `class WorkerSettings: functions = [process_user]; redis_settings = REDIS_SETTINGS` with `REDIS_SETTINGS = RedisSettings()` from `arq.connections`.

## httpx responses
```python
response = httpx.get(url)
response.raise_for_status()
user = User.model_validate(response.json())
```
For a list endpoint use `TypeAdapter(list[User]).validate_python(response.json())`. A `ValidationError` is often the first sign an API changed its response format.

## SQLAlchemy
Keep Pydantic models alongside SQLAlchemy models. A column named `metadata` is reserved by SQLAlchemy, so the table attribute is `metadata_ = sa.Column('metadata', sa.JSON)` and the Pydantic model aliases it:
```python
class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    metadata: dict[str, str] = Field(alias='metadata_')

pydantic_model = MyModel.model_validate(sql_model)
pydantic_model.model_dump()               # {'metadata': {'key': 'val'}}
pydantic_model.model_dump(by_alias=True)  # {'metadata_': {'key': 'val'}}
```
This works because aliases have priority over field names for population. To reduce duplication the page suggests `SQLModel`. Rows written before a constraint was added, or nullable columns, only fail when read.

## Checked

Checked 2026-11-07. Re-read examples/queues, examples/requests and examples/orms in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
