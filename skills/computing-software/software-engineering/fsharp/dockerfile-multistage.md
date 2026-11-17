---
id: computing-software.software-engineering.fsharp.dockerfile-multistage
name: dockerfile-multistage
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, dockerfile-multistage, fsharp-containers, dockerfile, docker-multistage]
level: practitioner
status: draft
description: "Containerise an F# app with a multi-stage Dockerfile using the .NET SDK and ASP.NET runtime images and a non-root user."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/docker/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-stage Dockerfile
**Goal:** small, cache-friendly, non-root image.

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY global.json Directory.Build.props nuget.config* ./
COPY src/App/App.fsproj src/App/
RUN dotnet restore src/App/App.fsproj
COPY . .
RUN dotnet publish src/App/App.fsproj -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app .
USER app
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "App.dll"]
```
- Copy project files first and restore, so the restore layer is cached until dependencies change.
- Use `runtime` images (`mcr.microsoft.com/dotnet/runtime`) for console apps and `aspnet` for web apps.
- Recent .NET images ship a non-root `app` user (.NET 8+); older images need `useradd`. Verify for your tag.
- Add a `.dockerignore` excluding `bin/`, `obj/`, `.git/`.
- `InvariantGlobalization=true` allows `-alpine` images without ICU.

## Gotchas
- F# projects list files explicitly, so changing source order alters the project file and busts the restore cache (rare).
- Alpine uses musl; native dependencies may not run.

## Self-check
`docker build -t app .` then `docker run --rm -p 8080:8080 app` and curl the endpoint.
