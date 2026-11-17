---
id: computing-software.software-engineering.ocaml.docker-images-for-ocaml
name: docker-images-for-ocaml
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, docker-images, docker-ocaml, multi-stage-build, opam-docker]
level: practitioner
status: draft
description: "Build in an ocaml/opam image with opam install --deps-only and ship a slim runtime image; cache the opam layer."
sources: ["https://dune.readthedocs.io/", "https://opam.ocaml.org/doc/", "https://github.com/ocaml/setup-ocaml"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Docker for OCaml

```dockerfile
FROM ocaml/opam:debian-ocaml-5.2 AS build
WORKDIR /home/<user>/<app>
COPY --chown=opam *.opam dune-project ./
RUN opam install . --deps-only --yes
COPY --chown=opam . .
RUN eval $(opam env) && dune build --release ./bin/main.exe

FROM debian:stable-slim
COPY --from=build /home/<user>/<app>/_build/default/bin/main.exe /usr/local/bin/app
ENTRYPOINT ["/usr/local/bin/app"]
```

## Notes
- Image tags and names (`ocaml/opam:<distro>-ocaml-<version>`) change over time; check Docker Hub for current tags.
- Copy only `*.opam`/`dune-project` first so the dependency layer caches.
- The runtime image needs the shared libraries that `ldd` lists (libgmp, libssl...).
- Run as a non-root user; set `OCAMLRUNPARAM` through ENV if needed.
- The builder runs as user `opam`; use `--chown=opam` on COPY.

## Self-check
- [ ] The final image runs and is far smaller than the build image.
