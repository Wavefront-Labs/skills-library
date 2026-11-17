---
id: computing-software.ai-ml-engineering.kserve.kserve-binary-tensor-data-extension
name: kserve-binary-tensor-data-extension
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [binary-tensor-data, binary-data-size, binary-data, binary-data-output, inference-header-content-length, fp16, applicationoctet-stream, infer-input]
level: advanced
status: docs-checked
description: "V2 Binary Tensor Data Extension: binary_data_size, binary_data, binary_data_output parameters, Inference-Header-Content-Length header, byte layouts and Python client usage."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/architecture/data-plane/v2-protocol/binary-tensor-data-extension.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Binary Tensor Data Extension (V2)

Lets REST clients send and receive tensors as raw bytes after the JSON header: useful for FP16 (no JSON representation), large tensors and throughput. Layout is little-endian, row-major, no stride or padding.

Parameters:
- `binary_data_size` (int64): on a request input or response output; tensor bytes follow the JSON.
- `binary_data` (bool): on a requested output; return that output as binary.
- `binary_data_output` (bool): on the request-level `parameters`; all outputs binary. Per-output `binary_data` overrides it.

Headers: `Inference-Header-Content-Length` = JSON length in bytes; `Content-Length` = JSON plus binary. The body content type is `application/octet-stream`.

Special encodings: BOOL is one byte (1/0); BYTES is a 4-byte unsigned length then the bytes; FP16 native 16-bit.

```json
{"inputs": [{"name": "input0", "shape": [2, 2], "datatype": "FP16",
             "parameters": {"binary_data_size": 16}}],
 "outputs": [{"name": "output0", "parameters": {"binary_data": true}}]}
```

Python client:

```python
input_0 = InferInput(name="input_0", datatype="FP16", shape=[2, 2])
input_0.set_data_from_numpy(fp16_data, binary_data=True)
out = RequestedOutput(name="output_0", binary_data=True)
```

Then `InferenceRESTClient(config=RESTConfig(protocol="v2")).infer(...)` and `outputs[i].as_numpy()`.

Limits: not every server or client supports it; harder to debug than JSON.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited binary tensor extension page in full. Removed the buffer-ordering sentence, which was not confirmed there.
