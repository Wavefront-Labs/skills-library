---
id: computing-software.messaging-and-integration.temporal.data-converter-and-payload-converter
name: data-converter-and-payload-converter
category: computing-software
field: messaging-and-integration
product: temporal
tags: [data-converter, payload, payload-converter, composite-data-converter, default-data-converter, serialization]
level: practitioner
status: docs-checked
description: "Temporal Data Converter order of operations: Payload structure, default converter chain nil, bytes, proto JSON, JSON, composite converters and sandbox limits."
sources:
  - https://docs.temporal.io/dataconversion
  - https://docs.temporal.io/default-custom-data-converters
  - https://docs.temporal.io/payload-converter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Data Converter is an SDK component that serialises everything entering or leaving the Temporal Service. Each argument or result becomes a Payload: binary data plus key-value metadata describing its type. Sensitive data then exists in original form only on hosts you control.

The flow is asymmetric: encoding happens automatically on input; decoding happens in your Workflow or Activity code. Decoded results are never written back, so stored data stays encoded, and `temporal workflow show` or the Web UI need an additional parameter to display it decoded.

Default converter order, tried until one returns a payload: Null, byte array, Protobuf JSON, then JSON. SDKs that cannot detect types at runtime (TypeScript) omit Protobuf. Protobuf messages encode as proto3 JSON; anything else is JSON, and an unserialisable value raises an error. It serialises by root type, so some SDKs cannot handle a list of Protobuf children without a custom converter.

Go's default is a composite, in this order:
```go
NewCompositeDataConverter(
    NewNilPayloadConverter(),
    NewByteSlicePayloadConverter(),
    NewProtoJSONPayloadConverter(),
    NewProtoPayloadConverter(),
    NewJSONPayloadConverter(),
)
```
A custom Payload Converter implements `ToPayload`/`ToPayloads` and `FromPayload`/`FromPayloads`. Order matters. Payload Converters run inside the Workflow sandbox, so they cannot call external services or use non-deterministic modules, which rules out most encryption; use a Payload Codec for that.

Custom converters can change format (MessagePack instead of JSON) or add compression and encryption. A custom Data Converter has three parts: Payload Converter, Payload Codec, Failure Converter. Search Attributes are never encoded, so they remain indexable.

## Checked

2026-11-08. Read in full on the Data Converter, Default and Custom Data Converters and Payload Converter pages: every concrete claim (names, events, rules, fields) matches the page. Removed the Codec Server remark: those pages only say an additional parameter is needed.

Method: documentation only; no commands were run.
