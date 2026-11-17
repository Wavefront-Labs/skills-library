---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-http-uri
name: kserve-storage-http-uri
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [http-uri, https, https-host, headers, tarball, joblib, secret-headers, uri-secret]
level: practitioner
status: docs-checked
description: "Serve a model from an HTTP or HTTPS URL: single-file or tar/zip artifacts, optional https-host and headers Secret (base64) attached to the predictor ServiceAccount."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/uri.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP/HTTPS URI model storage

Set `storageUri` to an `http(s)://` URL. Supported: a single model file (for example sklearn `model.joblib`) or an archive (`tar`, `zip`, `.tar.gz`) holding all files for multi-file formats such as tensorflow or pytorch.

```yaml
spec:
  predictor:
    model:
      modelFormat: {name: sklearn}
      storageUri: https://example.com/models/model.joblib
```

Tensorflow archives must be built from the versioned directory (`tar -cvf artifacts.tar 0001/`), containing `saved_model.pb` and `variables/`.

## Optional request headers

Define a Secret with base64 keys `https-host` (host name) and `headers` (a base64 JSON object of header names to values), then list it in a ServiceAccount `secrets:` and set `spec.predictor.serviceAccountName`.

```yaml
apiVersion: v1
kind: Secret
metadata: {name: mysecret}
type: Opaque
data:
  https-host: ZXhhbXBsZS5jb20=      # echo -n "example.com" | base64
  headers: <base64 of {"account-name": "...", "secret-key": "..."}>
---
apiVersion: v1
kind: ServiceAccount
metadata: {name: sa}
secrets:
  - name: mysecret
```

The headers are sent on every HTTP/HTTPS request to that same host. Both values must be base64 encoded.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KServe HTTP/HTTPS URI storage page in full; every claim matches it. No content removed.
