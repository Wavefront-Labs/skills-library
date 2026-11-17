---
id: computing-software.cloud-infrastructure-engineering.kubernetes.invalidimagename-image-reference-syntax
name: invalidimagename-image-reference-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshoot-pods, invalidimagename, image-reference, containers, errimagepull]
level: practitioner
status: docs-checked
description: "Fix pods stuck with InvalidImageName by checking image reference syntax (registry, repo, tag, digest), case, whitespace and unexpanded variables."
sources: ["https://kubernetes.io/docs/concepts/containers/images/", "https://github.com/distribution/reference/blob/main/reference.go", "https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/images/image_manager.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InvalidImageName

When the kubelet cannot parse the image reference, it raises a Warning event with reason
`InspectFailed` and message `Failed to apply default image tag "<image>": <parse error>`, and
the container waits with reason `InvalidImageName`. For an uppercase repository the parse error
ends with `invalid reference format: repository name must be lowercase`. The kubelet never
attempts a pull, which separates this from `ErrImagePull`.

## Valid form (distribution reference grammar)
`[domain[:port]/]path[:tag][@digest]`
- Path components are lowercase alphanumerics joined by separators: `.`, `_`, `__` or runs of
  `-`. No uppercase letters.
- Tag: `[\w][\w.-]{0,127}`, i.e. word characters, `.` and `-`, at most 128 characters, and not
  starting with `.` or `-`.
- Digest: `algorithm:hex`; a sha256 digest carries 64 hex characters. With both tag and digest
  (`name:3.5@sha256:...`) only the digest is used for pulling.
- The reference has no URL scheme.

## Common causes
| Value | Problem |
|---|---|
| `Acme/App:1.0` | uppercase in the repository name |
| `app:1.0 ` or a value with a newline | trailing whitespace or newline from templating |
| `registry:5000/app::1.0` | double colon |
| `app:$(TAG)` / `app:${TAG}` | variable never substituted; the field is a literal string |
| `app@sha256:abc` | truncated digest |
| `https://registry/app` | scheme is not part of an image reference |

## Find it
```bash
kubectl get pod <p> -o jsonpath='{range .spec.containers[*]}[{.image}]{"\n"}{end}'
kubectl describe pod <p>     # Events section shows the InspectFailed warning
```
Brackets reveal hidden spaces.

## Fix
Correct the manifest or Helm values, quote tags in YAML so numeric-looking tags stay strings,
then roll out. A CI step that parses image references with a reference-grammar library (or
checks they resolve in the registry) catches this before deploy.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Images", the kubelet image manager,
events and image error definitions, and the distribution/reference grammar and error values
(latest release v1.37.1). Confirmed: `InspectFailed` event reason, message prefix, the
`InvalidImageName` error name, grammar for path, tag, digest, the lowercase error text, tag-plus-digest
behaviour. Removed unconfirmed claims (exact full error line, where `$(VAR)` is expanded,
named CLI tools for digest checks).
Method: documentation only; no commands were run.
