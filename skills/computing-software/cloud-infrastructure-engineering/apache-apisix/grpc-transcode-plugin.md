---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.grpc-transcode-plugin
name: grpc-transcode-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, grpc-transcode, grpc, protobuf, proto, transcoding, plugin]
level: advanced
status: docs-checked
description: "Expose a gRPC service as HTTP/JSON in APISIX with grpc-transcode: proto upload to /protos, proto_id, service, method, pb_option and status details."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/grpc-transcode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# grpc-transcode plugin

Attributes:
- `proto_id`, `service`, `method` (all required).
- `max_resp_body_size`: 67108864 bytes; larger responses are truncated.
- `deadline`: 0 ms to wait for the gRPC call.
- `pb_option`: defaults `enum_as_name`, `int64_as_number`, `auto_default_values`, `disable_hooks`.
- `show_status_in_body`: false; `status_detail_type`: message type for decoding `grpc-status-details-bin`.

Upload the proto with PUT to `/apisix/admin/protos/{id}` and the `X-API-KEY` header, with the definition in `content`. For protos with imports or several files, build a descriptor set and base64 it:

`protoc --include_imports --descriptor_set_out=<file>.pb <file>.proto`, then `base64 -w0`, sent as `content`.

Route (note the upstream scheme is `grpc`):

```json
{
  "methods": ["GET"],
  "uri": "/echo",
  "plugins": { "grpc-transcode": { "proto_id": "echo-proto", "service": "echo.EchoService", "method": "Echo" } },
  "upstream": { "scheme": "grpc", "type": "roundrobin", "nodes": { "127.0.0.1:50051": 1 } }
}
```

Request parameters map to request message fields, so `?msg=Hello` fills `EchoMsg.msg`.

Large int64 values lose precision as numbers; set `pb_option` to `["int64_as_string"]` to keep them. `show_status_in_body` shows raw details until `status_detail_type` decodes them.

## Checked

2026-11-04. Confirmed against the APISIX grpc-transcode plugin page: attribute defaults, the protos upload path and `content` field, the descriptor-set protoc and base64 steps, the grpc upstream scheme, the `?msg=Hello` example, int64_as_string. Nothing removed.

Method: documentation only; no commands were run.
