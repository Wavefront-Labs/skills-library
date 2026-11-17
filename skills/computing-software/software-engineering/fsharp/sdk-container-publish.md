---
id: computing-software.software-engineering.fsharp.sdk-container-publish
name: sdk-container-publish
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, sdk-container-publish, fsharp-containers, publish-container, container-registry]
level: practitioner
status: docs-checked
description: "Build container images without a Dockerfile using dotnet publish with /t:PublishContainer and the Container* MSBuild properties."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/containers/sdk-publish
  - https://learn.microsoft.com/en-us/dotnet/core/containers/publish-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDK container publishing
**Goal:** image from `dotnet publish` alone (.NET 8+ SDK).

```bash
dotnet publish --os linux --arch x64 /t:PublishContainer
dotnet publish --os linux --arch x64 /t:PublishContainer -p ContainerRegistry=ghcr.io
dotnet publish --os linux --arch x64 /t:PublishContainer -p ContainerArchiveOutputPath=./images/app.tar.gz
```
```xml
<PropertyGroup>
  <ContainerRepository>myorg/app</ContainerRepository>
  <ContainerImageTags>1.0.0;latest</ContainerImageTags>
  <ContainerBaseImage>mcr.microsoft.com/dotnet/aspnet:8.0</ContainerBaseImage>
</PropertyGroup>
<ItemGroup>
  <ContainerPort Include="8080" Type="tcp" />
</ItemGroup>
```
- The SDK builds the image without Docker. By default it is pushed to a local container runtime (Docker or Podman); a running OCI-compatible daemon is needed for that, else the CreateNewImage task fails. A registry push or tarball needs no daemon.
- Tarball: `ContainerArchiveOutputPath` takes a folder (file named `$(ContainerRepository).tar.gz`) or a file path; one archive holds all tags. Load with `docker load -i` or `podman load -i`. The reference page also shows `-p PublishProfile=DefaultContainer` on the command line.
- Registry: `ContainerRegistry` (default is the local daemon). Authenticate with the usual `docker login` mechanisms. Any registry supporting Docker Registry HTTP API V2 works. `LocalRegistry` picks the local tool (Docker, Podman, Wslc, MacOSContainer).
- Image name: `ContainerRepository` defaults to the AssemblyName; lowercase alphanumerics, periods, underscores, dashes, slash-delimited segments. Tags: `ContainerImageTag` or semicolon-delimited `ContainerImageTags` (one image per tag; 127 characters max). From .NET 8 the default tag is `latest`.
- Base image: inferred as `runtime-deps` for self-contained, `aspnet` for ASP.NET Core projects, otherwise `runtime`, tagged with the TargetFramework number. `ContainerFamily` (for example `alpine`) appends to the tag and is ignored when `ContainerBaseImage` is set. Multi-arch via semicolon-delimited `ContainerRuntimeIdentifiers`, which must be a subset of `RuntimeIdentifiers`.
- `ContainerPort` is inferred from `ASPNETCORE_URLS`, `ASPNETCORE_HTTP_PORTS` and `ASPNETCORE_HTTPS_PORTS` when not set. Other items: `ContainerEnvironmentVariable`, `ContainerLabel`, `ContainerUser` (non-root `app` user by default with Microsoft .NET 8+ images on Linux), `ContainerWorkingDirectory` (default `/app`).
- `ContainerEntrypoint` and `ContainerEntrypointArgs` are deprecated since .NET 8; use `ContainerAppCommand`, `ContainerAppCommandArgs`, `ContainerDefaultArgs` and `ContainerAppCommandInstruction`.

## Gotchas
- RUN-style steps cannot be done; build a custom base image instead, or use a Dockerfile.
- Environment variables cannot be set from the .NET CLI when publishing a container; use `ContainerEnvironmentVariable` items.
- Escape `;` and quotes in `-p:ContainerImageTags=...` for PowerShell versus Bash, or set it as an environment variable.

## Self-check
`docker images` lists `myorg/app` after publishing.

## Checked
Checked against the Microsoft Learn "Containerize a .NET app with dotnet publish" tutorial and the container publish configuration reference.
Removed: the claim that console apps need `EnableSdkContainerSupport`, the "earlier SDKs need Microsoft.NET.Build.Containers" note, "web projects work out of the box", the Docker-config credentials gotcha and the generic index sources (none appear on the pages).
Method: docs-only read of cited pages, 2026-11-08
