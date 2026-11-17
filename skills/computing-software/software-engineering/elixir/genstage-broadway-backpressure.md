---
id: computing-software.software-engineering.elixir.genstage-broadway-backpressure
name: genstage-broadway-backpressure
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, genstage, broadway, producer-consumer, demand, backpressure, sqs, rabbitmq, kafka, batcher, broadway-genstage]
level: sme
status: draft
description: "Use GenStage for demand-driven pipelines and Broadway for ingesting from SQS/RabbitMQ/Kafka with batching, acknowledgements and concurrency control."
sources: ["https://hexdocs.pm/gen_stage", "https://hexdocs.pm/broadway"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GenStage and Broadway pipelines

**Goal:** consume message streams with backpressure.

```elixir
defmodule MyApp.Pipeline do
  use Broadway
  def start_link(_) do
    Broadway.start_link(__MODULE__,
      name: __MODULE__,
      producer: [module: {BroadwaySQS.Producer, queue_url: "https://sqs.example/queue"}, concurrency: 2],
      processors: [default: [concurrency: 20]],
      batchers: [s3: [batch_size: 100, batch_timeout: 2_000, concurrency: 2]])
  end
  @impl true
  def handle_message(_proc, %Broadway.Message{data: d} = m, _ctx), do: m |> Broadway.Message.update_data(&decode/1) |> Broadway.Message.put_batcher(:s3)
  @impl true
  def handle_batch(:s3, messages, _info, _ctx), do: (store(messages); messages)
  def handle_failed(messages, _ctx), do: messages
end
```

## Rules
- Consumers ask producers for demand, so a slow stage slows the whole line instead of overflowing memory.
- Messages are acknowledged after successful processing; mark failures with `Broadway.Message.failed/2` for retry or dead-lettering.
- Producer modules (SQS, RabbitMQ, Kafka) are separate dependencies.
- Set `concurrency` to match downstream capacity; increase partitions with `partition_by`.

## Self-check
Run a dummy producer (`Broadway.DummyProducer`) with `Broadway.test_message/3` and assert on the result.
