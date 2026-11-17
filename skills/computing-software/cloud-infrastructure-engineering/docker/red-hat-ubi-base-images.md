---
id: computing-software.cloud-infrastructure-engineering.docker.red-hat-ubi-base-images
name: red-hat-ubi-base-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, base-image, ubi, ubi-minimal, ubi-micro, microdnf, rhel, openshift]
level: practitioner
status: docs-checked
description: "Build on Red Hat Universal Base Images: choosing ubi, ubi-minimal, ubi-micro or ubi-init, installing into ubi-micro, redistribution and RHEL subscription repos."
sources: ["https://catalog.redhat.com/software/base-images", "https://developers.redhat.com/articles/ubi-faq", "https://www.redhat.com/en/blog/introduction-ubi-micro", "https://access.redhat.com/articles/4238681"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Red Hat UBI base images

UBI images are OCI-compliant base images built from RHEL packages and freely redistributable under the UBI EULA. UBI-based images are supported like RHEL when run on a Red Hat platform such as OpenShift or RHEL.

## Variants (UBI 9 shown; the catalog lists the same four for UBI 8)
| Image | Use |
|---|---|
| `registry.access.redhat.com/ubi9/ubi` | Standard image |
| `ubi9/ubi-minimal` | Minimal image (`yum` is not available in it) |
| `ubi9/ubi-micro` | Smallest; install packages from a builder using `--installroot` |
| `ubi9/ubi-init` | Full systemd; run and manage several services |

The catalog also lists language-runtime images.

## Patterns
```dockerfile
FROM registry.access.redhat.com/ubi9/ubi-minimal:<TAG>
```
ubi-micro has no package manager, so install into its root from a full UBI builder (Red Hat's ubi-micro introduction does this with `--installroot`):
```dockerfile
FROM registry.access.redhat.com/ubi9/ubi AS builder
RUN mkdir -p /mnt/rootfs && \
    dnf install -y --installroot /mnt/rootfs --releasever 9 --setopt=install_weak_deps=0 --nodocs \
      openssl-libs && dnf --installroot /mnt/rootfs clean all

FROM registry.access.redhat.com/ubi9/ubi-micro
COPY --from=builder /mnt/rootfs/ /
```

## Repositories and subscriptions
- No subscription is needed to use UBI or update images from the UBI repositories, which hold a small subset of the RHEL packages.
- Accessing non-UBI content needs a Red Hat subscription and makes images built with it non-redistributable. Check before publishing publicly.
- UBI images come from both `registry.redhat.io` (authenticated) and `registry.access.redhat.com` (unauthenticated).

## Gotchas
- Pin a specific tag or a digest rather than a floating one.

## Verify
```bash
docker run --rm registry.access.redhat.com/ubi9/ubi-minimal cat /etc/redhat-release
```

## Checked
2026-10-28. Confirmed against the Red Hat Ecosystem Catalog base-images page, the UBI FAQ, the ubi-micro introduction and Red Hat article 4238681 (variants, redistribution under the UBI EULA, no subscription needed, UBI repositories, both registries, `--installroot` for ubi-micro, no `yum` in ubi-minimal). Removed unconfirmed claims: package-manager column, language image names, UID 1001 and group-0 guidance, microdnf feature limits, Podman entitlement behaviour, FIPS, example tags.
Method: documentation only; no commands were run.
