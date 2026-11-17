---
id: computing-software.cloud-infrastructure-engineering.docker.dotnet-container-images
name: dotnet-container-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dotnet-image, dotnet-publish, aspnet-runtime, multi-stage, chiseled, language-images]
level: practitioner
description: "Build .NET images with the sdk/aspnet stage split, dotnet publish with the -a architecture option, and SDK container publish without a Dockerfile."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/docker/build-container", "https://learn.microsoft.com/en-us/dotnet/core/containers/sdk-publish", "https://github.com/dotnet/dotnet-docker/blob/main/samples/README.md", "https://docs.docker.com/guides/dotnet/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# .NET container images

## Multi-stage Dockerfile
Pattern from Docker's .NET guide: build in an `sdk` stage with `ARG TARGETARCH`, publish with the architecture option, copy `/app` into an `aspnet` runtime stage.
```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:<VERSION> AS build
ARG TARGETARCH
WORKDIR /source
COPY . .
RUN dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM mcr.microsoft.com/dotnet/aspnet:<VERSION> AS final
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "<App>.dll"]
```
- `${TARGETARCH/amd64/x64}` maps Docker's architecture name to the .NET one (as in Docker's guide).
- Pick the tag for your .NET version from the Microsoft container registry listings; check the image's own docs for the user it runs as and for any shell it lacks.

## Without a Dockerfile
The .NET SDK can build the image itself (documented on the sdk-publish page):
```sh
dotnet publish --os linux --arch x64 /t:PublishContainer
```
Container properties are passed as MSBuild properties (`-p`); see that page for the list.

## Ports
The Docker .NET guide maps and browses the app on port 8080 (`8080:8080`).

## Checked
2026-10-28. Confirmed against Docker's .NET guide (multi-stage Dockerfile with `TARGETARCH`, publish flags, port 8080) and the .NET SDK container publish page (`/t:PublishContainer`, `--os`, `--arch`). Removed unconfirmed claims: chiseled/alpine/runtime-deps variant behaviour and UID, `APP_UID`, `ASPNETCORE_HTTP_PORTS`, `PublishTrimmed`/`PublishAot` sizing, ICU and GC settings, `--no-restore` cache mounts, image size figures.
Method: documentation only; no commands were run.
