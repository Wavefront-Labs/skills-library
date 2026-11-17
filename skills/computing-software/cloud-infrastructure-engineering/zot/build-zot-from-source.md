---
id: computing-software.cloud-infrastructure-engineering.zot.build-zot-from-source
name: build-zot-from-source
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, build-from-source, make-binary, binary-minimal, golang, container-image-build]
level: practitioner
status: docs-checked
description: "Build Zot from source with make for a chosen OS and architecture, full or minimal, and build a container image with Stacker or Docker."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-getting-started.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/security-posture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisite: a golang toolchain at least as new as the minimum in `go.mod`, findable on PATH.

```
git clone https://github.com/project-zot/zot.git
make OS=os ARCH=architecture {binary | binary-minimal}
make OS=linux ARCH=amd64 binary
```

- OS and ARCH default to `linux` and `amd64`.
- `binary` builds the full image with all extensions; `binary-minimal` builds without extensions.
- Output lands in `zot/bin`, for example `zot-linux-amd64-minimal`.
- To pick extensions, pass a list: `make EXTENSIONS=search binary` builds with only search enabled.

Container image:

- With Stacker: `make binary-stacker`.
- With Docker: edit the sample Dockerfile (`ARG OS`, `ARG ARCH`, and the `RUN make ... clean binary-minimal` line), then `make image`.

Run the result, bind-mounting storage at `/var/lib/registry`:

```
docker run --rm -it -p 5000:5000 -v $(pwd)/registry:/var/lib/registry zot:latest
```

Authentication is off by default and the default config sits at `/etc/zot/config.json` in the container.

## Checked

Build, Stacker and Docker steps confirmed; EXTENSIONS example confirmed on the security posture page.

Method: docs-checked 2026-11-09 against zot docs admin-guide/admin-getting-started.md and articles/security-posture.md.
