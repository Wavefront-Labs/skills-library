---
id: computing-software.cloud-infrastructure-engineering.docker.language-specific-image-patterns
name: language-specific-image-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, language-images, node-image, python-image, go-image, java-image, dotnet-image, rust-image, multi-stage, official-images, slim, alpine, jlink, npm-ci, pip-install]
level: practitioner
status: draft
description: "The idiomatic production Dockerfile shape per language (Node, Python, Go, Java, .NET, Rust): dependency-layer ordering, which official tag to pick, lockfile install commands and the per-runtime traps."
sources: ["https://docs.docker.com/guides/nodejs/containerize/", "https://docs.docker.com/guides/python/containerize/", "https://docs.docker.com/guides/golang/build-images/", "https://docs.docker.com/guides/java/containerize/", "https://docs.docker.com/guides/dotnet/containerize/", "https://docs.docker.com/guides/rust/", "https://hub.docker.com/_/node", "https://hub.docker.com/_/python", "https://hub.docker.com/_/eclipse-temurin"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Language-specific image patterns

**Goal:** a Dockerfile for each runtime that rebuilds in seconds when only source changes,
ships only what runs, and runs as non-root. Every pattern below is the same shape: copy the
lockfile first, install, then copy source, then (if compiled) copy artifacts into a slim stage.

## Node
```dockerfile
FROM node:22-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev                    # ci, not install: respects lockfile, fails on drift

FROM node:22-slim
ENV NODE_ENV=production
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
USER node                                # official image ships uid 1000 "node"
CMD ["node", "server.js"]               # not "npm start": npm swallows signals
```
- Tag: `22-slim` (Debian, glibc) by default. `-alpine` is smaller but musl breaks native
  addons (`sharp`, `bcrypt`) and has a different DNS resolver; `-bookworm` full is for
  build stages needing compilers.
- Need a build step (TS/Next)? Add a stage that runs `npm ci` *with* dev deps, builds, then
  copy `dist/` and the prod `node_modules` into the runtime stage.
- `.dockerignore` must have `node_modules` or the host tree overwrites the installed one.

## Python
```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN useradd -r -u 1001 app && chown -R app /app
USER app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
```
- `PYTHONUNBUFFERED=1` or `docker logs` shows nothing until the buffer flushes.
- Packages with C extensions need `build-essential` — install in a builder stage and
  `pip install --prefix=/install`, then `COPY --from=build /install /usr/local`, or use a venv
  at `/opt/venv` and copy it. uv: `COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv` then
  `uv sync --frozen --no-dev` with `--mount=type=cache,target=/root/.cache/uv`.
- Don't use `-alpine` for data/science stacks: no manylinux wheels, builds numpy from source.

## Go
```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.23 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
ARG TARGETOS TARGETARCH
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build -ldflags="-s -w" -o /out/app .

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
- `CGO_ENABLED=0` is what makes the binary static enough for `scratch`/`distroless/static`.
  If you need cgo (sqlite, some crypto), use `distroless/base` (has libc).
- `scratch` has no CA certs or tzdata: copy `/etc/ssl/certs/ca-certificates.crt` from the
  builder or use distroless, which includes them.

## Java
```dockerfile
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw -q dependency:go-offline          # dependency layer, cached until pom changes
COPY src src
RUN ./mvnw -q package -DskipTests

FROM eclipse-temurin:21-jre
COPY --from=build /app/target/*.jar /app.jar
USER 1001
ENTRYPOINT ["java", "-jar", "/app.jar"]
```
- Modern JVMs (17+) are container-aware: `-XX:MaxRAMPercentage=75` beats a hardcoded
  `-Xmx`, and the heap sizes against the cgroup limit.
- Smaller: `jlink` a custom runtime from the `jdk` image and copy it onto
  `debian:slim`/distroless/java; Spring Boot's layered jar (`java -Djarmode=layertools
  -jar app.jar extract`) lets you copy `dependencies/` before `application/` for caching.
- `openjdk` images on Hub are deprecated; use `eclipse-temurin`, `amazoncorretto` or
  `bellsoft/liberica`.

## .NET
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY *.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .
USER app                                   # uid 1654 exists in 8.0+ images; port default 8080
ENTRYPOINT ["dotnet", "MyApp.dll"]
```
- 8.0+ runtime images listen on 8080 (not 80) and ship a non-root `app` user.
- `-chiseled` tags (Ubuntu) are the distroless equivalent; `dotnet publish
  /p:PublishAot=true` on the `sdk` image with `runtime-deps` base for native AOT.

## Rust
Dependency caching is the pain: `cargo build` needs a `main.rs` to compile deps alone. Use
`cargo-chef` (`lukemathwalker/cargo-chef`) — `chef prepare` produces a recipe.json, `chef cook`
builds deps in a cached layer, then copy source and `cargo build --release`. Runtime stage:
`debian:bookworm-slim` (needs `ca-certificates`, `libssl3` if not using rustls) or
`distroless/cc` for glibc+libgcc only.

## Cross-language rules
- Copy manifests → install → copy source. Never `COPY . .` before install.
- Pin a major.minor tag (`python:3.12-slim`), never `latest`; pin digests in production.
- `docker init` (see `docker-init-project-templates`) generates these shapes for Node, Python,
  Go, Java, .NET, Rust, PHP and ASP.NET as a starting point.

## Verify
Touch one source file and rebuild: every step up to and including the dependency install
should print `CACHED`. `docker run --rm app id` should not print `uid=0`.
