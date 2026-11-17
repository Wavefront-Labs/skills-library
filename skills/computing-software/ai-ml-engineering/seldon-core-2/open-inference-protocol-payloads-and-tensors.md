---
id: computing-software.ai-ml-engineering.seldon-core-2.open-inference-protocol-payloads-and-tensors
name: open-inference-protocol-payloads-and-tensors
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, open-inference-protocol, v2-protocol, inference-request, tensor-data, datatypes, tensor-shape, parameters]
level: practitioner
status: docs-checked
description: "Build V2 inference request and response JSON: inputs with name, shape, datatype and data in row-major order, optional outputs and id, and the tensor datatypes table."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/user-guide/v2/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Open Inference Protocol: payloads and tensors

## Request object
POST to `v2/models/${MODEL_NAME}/infer`. The body is an `$inference_request`:
- `id`: optional identifier; if set it must be returned in the response.
- `parameters`: optional key/value pairs (string, number or boolean). No standard parameters are defined yet; servers may add their own.
- `inputs`: list of input tensors, each with `name`, `shape` (unsigned 64-bit integers), `datatype`, optional `parameters`, and `data`. For a batched input the shape and data hold the whole batch.
- `outputs`: optional list of requested output tensors by `name`. If omitted, all model outputs are returned.

```
{
  "id" : "42",
  "inputs" : [
    { "name" : "input0", "shape" : [ 2, 2 ], "datatype" : "UINT32", "data" : [ 1, 2, 3, 4 ] },
    { "name" : "input1", "shape" : [ 3 ], "datatype" : "BOOL", "data" : [ true ] }
  ],
  "outputs" : [ { "name" : "output0" } ]
}
```

## Response
A 200 status carries `model_name`, optional `model_version`, `id`, optional `parameters`, and `outputs` with name, shape, datatype and data.

## Tensor data
Data is row-major in linear order, no stride or padding. It can be nested, `[[1, 2], [4, 5]]`, or flat, `[1, 2, 4, 5]`. The server may coerce element types or return an error. FP16 is hard to express in JSON.

## Datatypes
BOOL, UINT8, UINT16, UINT32, UINT64, INT8, INT16, INT32, INT64, FP16, FP32, FP64 and BYTES (variable size). Sizes in bytes are 1, 1, 2, 4, 8, 1, 2, 4, 8, 2, 4, 8 for the fixed types.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/user-guide/v2/README.md (read in full, request, response, tensor data and datatype sections).
