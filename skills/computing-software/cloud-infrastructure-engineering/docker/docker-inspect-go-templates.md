---
id: computing-software.cloud-infrastructure-engineering.docker.docker-inspect-go-templates
name: docker-inspect-go-templates
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-inspect, inspect-format, go-template, format-flag, docker-ps-format, jq]
level: practitioner
description: "Extract exactly the field you need from docker inspect, ps, images and events with --format Go templates: index, range, json, join, conditionals and table output."
sources: ["https://docs.docker.com/reference/cli/docker/inspect/", "https://docs.docker.com/engine/cli/formatting/", "https://github.com/docker/cli/blob/master/docs/reference/commandline/docker.md", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# docker inspect --format with Go templates

## Recipes
```sh
# IP on each network
docker inspect -f '{{range $net, $cfg := .NetworkSettings.Networks}}{{$net}}={{$cfg.IPAddress}} {{end}}' app
# keys with dots or dashes need index
docker inspect -f '{{index .Config.Labels "com.docker.compose.service"}}' app
# exit code, OOM, restart count
docker inspect -f '{{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}} restarts={{.RestartCount}}' app
# mounts
docker inspect -f '{{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}} rw={{.RW}}{{println}}{{end}}' app
# published ports
docker inspect -f '{{range $p, $b := .NetworkSettings.Ports}}{{$p}} -> {{if $b}}{{(index $b 0).HostPort}}{{end}}{{println}}{{end}}' app
# env as lines
docker inspect -f '{{join .Config.Env "\n"}}' app
# whole subtree as JSON
docker inspect -f '{{json .HostConfig}}' app
# health (only if defined)
docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' app
```
Template functions Docker adds: `json`, `join`, `split`, `lower`, `upper`, `title`, `pad`,
`truncate`, `println`; `table` is a `--format` prefix. Standard Go: `index`, `range`, `if/else`, `eq`, `len`, `printf`.

## ps / images / events
```sh
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker ps --format '{{.Names}} {{.Label "com.docker.compose.project"}}'
docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
docker ps --format json
```
`table` adds headers; placeholders differ per command (`docker ps --format '{{json .}}'`
shows the available fields).
Defaults: `~/.docker/config.json` -> `"psFormat": "table {{.Names}}\t{{.Status}}"`.

## Gotchas
- To get the IP on each network, range over `.NetworkSettings.Networks` (the Docker docs' own example).
- `{{.Config.Labels.com.docker...}}` fails: dots are field separators; use `index`.
- PowerShell/cmd quoting: use double quotes outside and escape inner quotes.

## Verify
Compare with the raw output of `docker inspect app`; its `State` object holds the same values.

## Checked
2026-10-25, against docker/docs engine pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master) and the Engine API swagger (moby/moby master). Confirmed: `--format` template functions `join`, `table`, `json`, `lower`, `split`, `title`, `upper`, `pad`, `truncate`, `println`; docs examples for ranging over `.NetworkSettings.Networks`, `index` on ports, `{{json .Config}}`; Windows quoting hint; `psFormat` in the CLI config file; the fields `.State.ExitCode`, `.State.OOMKilled`, `.RestartCount`, `.Mounts[].RW`, `.HostConfig.NanoCpus` exist in the API schema. Removed: default-bridge `.NetworkSettings.IPAddress` claim, `map has no entry` explanation, jq and sort pipelines.
Method: documentation only; no commands were run.
