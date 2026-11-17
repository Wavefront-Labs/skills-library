---
id: computing-software.cloud-infrastructure-engineering.kyverno.cel-libraries
name: cel-libraries
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [cel-libraries, resource-get, http-client, globalcontext, x509-decode, parseserviceaccount, image-metadata]
level: advanced
status: docs-checked
description: "Use Kyverno's CEL extension libraries: resource, http, user, image, ImageData, globalContext, hash, math, random, json, yaml, time and x509 functions."
sources:
  - https://kyverno.io/docs/policy-types/cel-libraries/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- Resource: `resource.Get(apiVersion, resource, namespace, name)`; `resource.List(apiVersion, resource, namespace[, labelMap])` (empty namespace `""` means all; read `.items`); `resource.Post(apiVersion, resource, body)`, e.g. SubjectAccessReview.
- HTTP: `http.Get(url)`, `http.Post(url, body, headers)`, `http.Client(caBundle).Get(url)`. A non-empty PEM `caBundle` replaces the system roots for that client. With no `Authorization` header Kyverno injects a scoped ServiceAccount token (default audience `kyverno-svc.kyverno.io`). Flags `--httpBlocklist`, `--httpAllowlist`, `--allowHTTPInNamespacedPolicies`; disabled in namespaced policies by default. The page says both that the blocklist applies and that CEL HTTP bypasses it, so verify before relying on either.
- User: `parseServiceAccount(request.userInfo.username)` gives `.Name` and `.Namespace`.
- Image: `image(str)` must come first; `isImage(str)`; methods `registry()`, `repository()`, `identifier()`, `tag()`, `digest()`, `containsDigest()`.
- ImageData: `image.GetMetadata(ref)` returns config (`architecture`, `os`, `author`, `created`...), `digest`, `manifest.*`. Check for null first.
- GlobalContext: `globalContext.Get(entryName, "")`.
- Hash: `md5`, `sha1`, `sha256`. Math: `math.round(value, precision)` (`math.round(12345.6789, -2)` gives 12300.0).
- Random: `random()` is 8 chars `[0-9a-z]{8}`; `random(pattern)`.
- Transform: `listObjToMap(list1, list2, keyField, valueField)`. JSON: `json.unmarshal`. YAML: `yaml.parse`.
- Time: `time.now()`, `time.truncate(ts, duration)`, `time.toCron(ts)`.
- X509: `x509.decode(pem)` with fields such as `IsCA`, `NotBefore`, `NotAfter`, `DNSNames`; the page example wraps `NotAfter` in `timestamp()` for date arithmetic.

## Checked

2026-11-08. Read the Kyverno CEL libraries page sections for Resource, HTTP (including the security notes), User, Image, ImageData, GlobalContext, Hash, Math, Random, Transform, JSON, YAML, Time and X509; confirmed each function signature and example against the page text. Changed the rounding note to the page example and the x509 date note to what the example does. The HTTP page text contradicts itself on whether cluster-scoped policies are subject to the blocklist; that caveat is kept. The "check for null first" note is supported only by the sample policy's `variables.image != null` expression.

Method: documentation only; no commands were run.
