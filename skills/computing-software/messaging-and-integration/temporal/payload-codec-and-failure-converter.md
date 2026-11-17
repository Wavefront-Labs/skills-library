---
id: computing-software.messaging-and-integration.temporal.payload-codec-and-failure-converter
name: payload-codec-and-failure-converter
category: computing-software
field: messaging-and-integration
product: temporal
tags: [payload-codec, encryption, compression, failure-converter, encodecommonattributes, data-converter]
level: practitioner
status: docs-checked
description: "Temporal Payload Codec for encryption and compression, converter then codec chain, and enabling EncodeCommonAttributes so failure messages and stacks are encoded."
sources:
  - https://docs.temporal.io/payload-codec
  - https://docs.temporal.io/failure-converter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Payload Codec maps a list of Payloads to another list (bytes to bytes). Unlike a Payload Converter it runs outside the Workflow sandbox, so it may call remote services and use non-deterministic code: encryption, compression, or offloading big payloads to an object store. It can also be hosted as a Codec Server.

Chain, outbound: Payload Converter `toPayload` turns objects into Payloads, then the codec `encode` runs. Inbound: codec `decode` first, then the converter `fromPayload`. For end-to-end encryption put the cipher in the codec; you hold the keys, the Server sees only ciphertext, and plaintext exists only on your Client and Worker hosts. Samples use AES-GCM with a 256-bit key (Go, Java, Python, TypeScript).

Failure Converter: by default failure `message` and call stack are copied as plain text into the failure's `Message`, visible to anyone. They are not codec-encoded unless you opt in. Enabling encoding moves `message` and `stack_trace` into a Payload that runs through your codec. Go:
```go
c, err := client.Dial(client.Options{
    DataConverter: mycustom.DataConverter,
    FailureConverter: temporal.NewDefaultFailureConverter(
        temporal.DefaultFailureConverterOptions{
            EncodeCommonAttributes: true,
        }),
})
```
Replace `NewDefaultFailureConverter` with your own method when failures need different encryption from, say, logging or observability pipelines.

## Checked

2026-11-08. Read in full: the Payload Codec and Failure Converter pages (docs.temporal.io/payload-codec, docs.temporal.io/failure-converter). Every remaining claim matches those pages. Nothing removed.

Method: documentation only; no commands were run.
