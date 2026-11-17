---
id: computing-software.ai-ml-engineering.kserve.kserve-inference-clients
name: kserve-inference-clients
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [inferencerestclient, restconfig, infer, explain, is-server-ready, is-model-ready, python-client, alpha]
level: practitioner
status: docs-checked
description: "Alpha Python InferenceRESTClient with RESTConfig (protocol, retries, timeout, verify) and its methods infer, explain and the readiness and liveness checks."
sources: ["https://github.com/kserve/website/blob/main/docs/reference/inference-client/inference-rest-client.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Python InferenceRESTClient (alpha)

An async client in the `kserve` package for inference servers that follow the V1 and V2 protocols. The docs call the feature alpha and subject to change. With no config, a default `RESTConfig` is used.

## RESTConfig
`RESTConfig(transport=None, protocol=v1, retries=3, http2=False, timeout=60, cert=None, verify=True, auth=None, verbose=False)`: `transport` is a custom `httpx.AsyncBaseTransport`; `protocol` is "v1" (default) or "v2"; `retries` is HTTP retries (3); `http2` (False); `timeout` in seconds (60); `cert`; `verify` (True; bool, str or ssl.SSLContext); `auth`; `verbose` (False).

```python
from kserve import RESTConfig, InferenceRESTClient
client = InferenceRESTClient(RESTConfig(protocol="v2", retries=5, timeout=30))
data = {"inputs": [{"name": "input_1", "shape": [1, 3], "datatype": "FP32", "data": [1.0, 2.0, 3.0]}]}
result = await client.infer("https://example.com:443", data, "example_model",
                            {"Authorization": "Bearer YOUR_TOKEN"}, {})
```

## Methods (all async)
- `infer(base_url, data, model_name=None, headers=None, response_headers=None, is_graph_endpoint=False, timeout=USE_CLIENT_DEFAULT)` returns `InferResponse` or dict; `data` is an `InferRequest` or dict; `response_headers` is a dict that receives the response headers. Raises `ValueError` if `model_name` is None and it is not a graph endpoint, `UnsupportedProtocol`, `HTTPStatusError`.
- `explain(base_url, model_name, data, headers=None, timeout)` returns a dict; V1 protocol only.
- `is_server_ready(base_url, headers=None, timeout=None)`: V2 protocol only; returns bool.
- `is_server_live(base_url, headers=None, timeout=USE_CLIENT_DEFAULT)` returns bool.
- `is_model_ready(base_url, model_name, headers=None, timeout=USE_CLIENT_DEFAULT)` returns bool.

The page's readiness examples construct `InferenceClient(config)`, which looks like a typo for `InferenceRESTClient`.

## Checked
Confirmed against the KServe Inference REST Client reference page: RESTConfig signature and defaults, method signatures, protocol limits and raised errors. Removed the InferenceGRPCClient section (SSL options, retry policy numbers) and the gRPC mentions in the description and tags because the cited page does not cover them.

Method: docs-only read of cited pages, 2026-11-08
