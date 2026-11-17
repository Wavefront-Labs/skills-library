---
id: computing-software.firmware-embedded-development.iot-protocols.nanopb-protobuf
name: nanopb-protobuf
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [nanopb-protobuf, protobuf-iot, nanopb, protobuf, options-file, pb-encode, iot-protocols]
level: practitioner
status: docs-checked
description: "nanopb on microcontrollers: Encode protobuf on MCUs without malloc."
sources:
  - https://jpa.kapsi.fi/nanopb/docs/concepts.html
  - https://jpa.kapsi.fi/nanopb/docs/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nanopb on microcontrollers

**Goal:** Encode protobuf on MCUs without malloc.

## Steps
1. Write .proto and an .options file (same name as the .proto, e.g. Foo.options with a line Foo.name max_size:16) using max_size, max_length, max_count or fixed_length to bound strings, bytes and repeated fields
2. Generate: nanopb_generator.py msg.proto (writes msg.pb.h and msg.pb.c; needs protoc 3.6 or newer, e.g. via the grpcio-tools pip package), or protoc --nanopb_out=. msg.proto with the plugin
3. Encode with pb_ostream_from_buffer(buf, bufsize) and pb_encode(&stream, Msg_fields, &msg); read stream.bytes_written and pass it as the message length on the decoding side
4. Decode with a pb_istream_t and pb_decode; pb_decode returns false when a string, bytes or array exceeds its allocated max_size or max_count
5. Use callbacks (pb_callback_t) for large, unbounded or variable fields; in encoding the callback is called once and must write complete fields including tags
6. A pb_ostream_t whose callback is NULL only counts bytes, so encoding into it measures the encoded size without a buffer
7. max_size for a string includes the terminating zero; max_length N is equivalent to max_size N+1

## Gotcha
Without max_size or max_count options, strings, bytes and repeated fields map to callbacks that need extra handling; bound everything for static allocation. A callback field inside a oneof cannot be set before decoding.

## Verify
- [ ] Encode and decode round trip
- [ ] Output buffer is large enough (pb_encode returns false if it is not)
- [ ] pb_encode returns true

## Checked
Confirmed 2026-11-08 against the nanopb docs "Basic concepts" and "API reference". Both were partial reads (line ranges and keyword searches covering the proto-file, streams, field-option, callback, .options file and pb_encode.h sections), not full reads. Removed as not found on these pages: the Msg_size worst-case macro and pb_istream_from_buffer.
Method: documentation only; no commands were run.
