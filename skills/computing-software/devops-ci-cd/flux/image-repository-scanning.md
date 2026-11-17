---
id: computing-software.devops-ci-cd.flux.image-repository-scanning
name: image-repository-scanning
category: computing-software
field: devops-ci-cd
product: flux
tags: [imagerepository, image-reflector-controller, exclusionlist, accessfrom, image-scan]
level: sme
status: docs-checked
description: "Scan a container registry for tags with ImageRepository, exclude Cosign signatures, and share it across namespaces."
sources:
  - https://fluxcd.io/flux/components/image/imagerepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An ImageRepository scans a registry repository on an interval and stores the tag list in the controller's internal database.

```yaml
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImageRepository
metadata:
  name: app1
  namespace: apps
spec:
  interval: 1h
  image: docker.io/org/image
  secretRef:
    name: regcred
```

`.spec.image` is the repository without a tag. Authentication uses `secretRef` (an image pull secret), `serviceAccountName`, or `provider` (generic by default; aws, azure or gcp for cloud registries). Also available: `certSecretRef` for custom CA or client certs, `proxySecretRef`, `insecure` for non-TLS HTTP and `timeout` (defaults to the interval).

`.spec.exclusionList` is a list of regexes for tags to skip. Its default is `^.*\.sig$`, which drops Cosign signature tags that are not deployable images. If you set your own list, re-add that pattern when you still use Cosign.

`.spec.accessFrom` restricts cross-namespace use. To grant access to ImagePolicies in other namespaces, list label selectors that match those namespaces' labels.

Scan results appear in `.status.lastScanResult`; the resolved canonical image name is in `.status.canonicalImageName`.

## Checked

2026-11-08: read the image-reflector-controller ImageRepository spec (docs/spec/v1/imagerepositories.md in the fluxcd/image-reflector-controller repo, the source of the fluxcd.io page) in part: the intro example, interval, timeout, auth, certSecretRef, proxySecretRef, accessFrom, exclusionList, insecure, provider and status sections, via search plus targeted reads. Confirmed: the example fields, the .sig default exclusion for Cosign, accessFrom, and the status fields. Removed: the components-extra install flags, the slow and memory-hungry scan warning and the flux CLI command, which are not in the spec.

Method: documentation only; no commands were run.
