---
id: computing-software.software-engineering.perl.docker-perl-images
name: docker-perl-images
category: computing-software
field: software-engineering
product: perl
tags: [perl, docker-perl, perl-docker-image, multi-stage-build, carton-docker, container-image, docker-perl-images]
level: practitioner
status: draft
description: "Build small, reproducible container images for Perl apps: official perl images, multi-stage builds, Carton deployment and non-root users."
sources: ["https://hub.docker.com/_/perl", "https://metacpan.org/pod/Carton"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Docker images for Perl applications

**Goal:** repeatable containers.

```dockerfile
# syntax=docker/dockerfile:1
FROM perl:5.40 AS build                      # official image; check Docker Hub for available tags (e.g. -slim, -threaded)
WORKDIR /app
COPY cpanfile cpanfile.snapshot ./
RUN cpanm --notest Carton && carton install --deployment --without develop,test
COPY . .

FROM perl:5.40-slim
RUN useradd -r -u 10001 app
WORKDIR /app
COPY --from=build /app /app
COPY --from=build /usr/local/bin/carton /usr/local/bin/carton   # not needed at run time if you set PERL5LIB
ENV PERL5LIB=/app/local/lib/perl5 PATH=/app/local/bin:$PATH
USER app
EXPOSE 8080
CMD ["perl", "script/app", "daemon", "-l", "http://*:8080"]
```

## Rules
- Build XS modules in the same OS and Perl as the runtime image (the multi-stage example uses matching tags); the slim image lacks compilers, so build in the full image.
- Pin the Perl version and use `cpanfile.snapshot` for reproducible module sets; cache layers by copying `cpanfile*` before the source.
- Run as a non-root user; write only to mounted volumes.
- Log to STDOUT/STDERR; configure through environment variables; add a health endpoint.
- Use `STOPSIGNAL SIGTERM` and handle TERM so workers exit cleanly (hypnotoad/Starman handle signals).
- Use `perl:5.xx-slim` or Alpine only after checking XS modules build there (musl may need extra packages).
- Add `.dockerignore` for `local/`, `.git/`, `_build/`.
- Prefer one process per container; use the framework's prefork server (Starman, hypnotoad) behind a proxy.
- Rebuild periodically to pick up Perl and OS security updates.

## Self-check
- [ ] `docker run --rm image perl -v` and `carton exec perl -MMojolicious -e1` succeed inside the image.
