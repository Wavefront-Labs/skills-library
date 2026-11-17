---
id: computing-software.software-engineering.csharp-dotnet.container-images-with-dotnet-publish
name: container-images-with-dotnet-publish
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-container-publish, containers, chiseled-images, sdk-container-builds, dockerfile, dotnet-cli]
level: practitioner
status: docs-checked
description: "Build .NET container images without a Dockerfile via dotnet publish PublishContainer: chiseled or alpine bases, tags, registries, non-root, and when to use a Dockerfile."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/containers/sdk-publish
  - https://learn.microsoft.com/en-us/dotnet/core/containers/publish-configuration
  - https://learn.microsoft.com/en-us/dotnet/core/compatibility/containers/8.0/aspnet-port
  - https://github.com/dotnet/dotnet-docker/blob/main/documentation/ubuntu-chiseled.md
  - https://github.com/dotnet/dotnet-docker/blob/main/documentation/image-variants.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container images with dotnet publish

**Goal:** small, non-root, reproducible images for .NET services straight from the SDK.

## Publish to an image
```bash
dotnet publish -c Release -t:PublishContainer \
  -p:ContainerRepository=acme/orders \
  -p:ContainerImageTags='"1.4.2;latest"' \
  -p:ContainerRegistry=ghcr.io
```
A Dockerfile is not needed. Without a registry the image is pushed to the local OCI-compliant daemon (Docker or Podman); publishing to a registry or an archive does not need a running daemon. Configure in the csproj instead of flags:
```xml
<PropertyGroup>
  <ContainerRepository>acme/orders</ContainerRepository>
  <ContainerFamily>alpine</ContainerFamily>                  <!-- family variant of the base image -->
  <ContainerImageTags>$(Version);latest</ContainerImageTags>
</PropertyGroup>
<ItemGroup>
  <ContainerPort Include="8080" Type="tcp" />
  <ContainerEnvironmentVariable Include="DOTNET_gcServer" Value="0" />
  <ContainerLabel Include="org.opencontainers.image.source" Value="https://github.com/acme/orders" />
</ItemGroup>
```

## Base images
| Image | Size / surface | Notes |
|---|---|---|
| `mcr.microsoft.com/dotnet/aspnet:9.0` | Debian, full | shell and package manager; easiest to debug |
| `aspnet:9.0-noble-chiseled` | Ubuntu Chiseled: no shell, no package manager, non-root user by default | smaller attack surface |
| `aspnet:9.0-alpine` | Alpine (musl) | check native dependencies |
Alpine, Azure Linux and Ubuntu Chiseled images do not include ICU or tzdata by default and need globalization-invariant mode; use the `extra` variant if the app needs globalization support.

## Security defaults
With .NET 8+ and the Microsoft runtime images the SDK defaults `ContainerUser` to the rootless `app` user on Linux, and the default ASP.NET Core port changed from 80 to **8080** in .NET 8 images. Kubernetes probes and ports must match. `ContainerPort` is inferred from `ASPNETCORE_URLS`, `ASPNETCORE_HTTP_PORTS` and `ASPNETCORE_HTTPS_PORTS` when not set.

## When a Dockerfile is still better
The .NET SDK cannot run `RUN` commands (for example to install OS packages), so use a Dockerfile when the image needs them.

## Debugging chiseled containers
Chiseled images have no shell, so debug from a separate (ephemeral) container or a sidecar.

## Verify
- [ ] `docker run --rm -p 8080:8080 acme/orders:1.4.2` serves health checks; process runs as non-root.
- [ ] Image scanned in CI; base image updates rebuild automatically.

## Checked

Checked 2026-10-25 against dotnet/docs (core/containers/sdk-publish, publish-configuration, whats-new/dotnet-8/containers, compatibility/containers/8.0/aspnet-port) and dotnet/dotnet-docker (ubuntu-chiseled, image-variants) on main.
Confirmed: `ContainerImageTags` semicolon-delimited; `ContainerFamily`, `ContainerLabel`, `ContainerEnvironmentVariable` names; `ContainerPort` is an item (`Include`, `Type`) and is inferred from ASP.NET port variables in .NET 8+ (the earlier property form was wrong); default `ContainerUser` is the rootless `app` user for .NET 8+ Microsoft images; ASP.NET default port 8080; chiseled images have no shell or package manager and are non-root; ICU and tzdata need the `extra` variant; local daemon needed only for local publish; the SDK cannot run `RUN` commands.
Removed as unconfirmed: `noble-chiseled` as a `ContainerFamily` value, the numeric UID, image size savings, the multi-stage Dockerfile recipe, the `kubectl debug` command line, scanner names.

Method: documentation only; no commands were run.
