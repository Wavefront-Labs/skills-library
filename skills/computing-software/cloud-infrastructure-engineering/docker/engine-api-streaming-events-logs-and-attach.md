---
id: computing-software.cloud-infrastructure-engineering.docker.engine-api-streaming-events-logs-and-attach
name: engine-api-streaming-events-logs-and-attach
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-engine-api, api-streaming, hijacked-connection, attach, exec-start, stdcopy, multiplexed-stream, events-stream, stats-stream]
level: advanced
status: docs-checked
description: "Consume Docker Engine API streams correctly: events and stats JSON streams, multiplexed log frames, hijacked attach/exec connections with half-close, SDK helpers, proxy pitfalls."
sources: ["https://docs.docker.com/reference/api/engine/version/v1.56/#tag/Container/operation/ContainerAttach", "https://docs.docker.com/reference/api/engine/version/v1.56/#tag/Exec/operation/ExecStart", "https://docs.docker.com/reference/api/engine/version/v1.56/#tag/System/operation/SystemEvents", "https://github.com/moby/moby/blob/master/api/docs/CHANGELOG.md", "https://github.com/moby/moby/blob/master/client/container_exec.go", "https://github.com/docker/docker-py/blob/main/docker/constants.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Engine API streaming endpoints

## The four stream shapes
| Endpoint | Shape |
|---|---|
| `GET /events` | JSON message stream, open until `until` or disconnect |
| `GET /containers/{id}/stats` | stream by default (`stream=true`); `stream=false&one-shot=true` for a single sample |
| `GET /containers/{id}/logs?follow=1&stdout=1&stderr=1` | raw bytes (TTY) or **multiplexed frames** (no TTY) |
| `POST /containers/{id}/attach`, `POST /exec/{id}/start` | **hijacked** bidirectional connection |

```bash
curl -sN --unix-socket /var/run/docker.sock http://localhost/v1.47/events          # -N: no buffering
curl -sN --unix-socket /var/run/docker.sock 'http://localhost/v1.47/containers/web/stats?stream=true'
```
`/events` takes `since`, `until` and `filters` (a JSON-encoded `map[string][]string`; filters
include `container`, `event`, `image`, `label`, `network`, `plugin`, `scope`, and more).

## Multiplexed frames (logs, attach, exec without TTY)
Each frame: 8-byte header `[STREAM_TYPE, 0, 0, 0, SIZE1..SIZE4]` then the payload. The size is a
big-endian `uint32`. `STREAM_TYPE` is 0 for stdin (written on stdout), 1 stdout, 2 stderr.
Read 8 bytes, pick the stream, read `size` bytes, repeat. When the container was created with
`Tty: true` the stream is raw (not multiplexed) and must not be demuxed, so check
`Config.Tty` first. The `Content-Type` is `application/vnd.docker.multiplexed-stream` when the
stream is multiplexed and `application/vnd.docker.raw-stream` otherwise (the attach and logs
Content-Type change appears in the API changelog under v1.42).

Go: `stdcopy.StdCopy(os.Stdout, os.Stderr, body)` (package `github.com/moby/moby/api/pkg/stdcopy`).
Python: `container.logs(stream=True)` or `exec_run(..., demux=True)`.

## Hijacked connections (attach, exec start)
The reference documents this request and response for attach:
```
POST /v1.47/containers/web/attach?stream=1&stdin=1&stdout=1&stderr=1 HTTP/1.1
Upgrade: tcp
Connection: Upgrade
```
Reply: `HTTP/1.1 101 UPGRADED` with `Content-Type: application/vnd.docker.raw-stream` (or the
multiplexed type), `Connection: Upgrade`, `Upgrade: tcp`, then raw bidirectional bytes. The
upgrade headers are an optional hint for proxies. Either `stream` or `logs` must be true on
attach for it to do anything.
- Exec flow: `POST /containers/{id}/exec` (body fields `AttachStdout`, `AttachStdin`,
  `AttachStderr`, `Tty`, `Cmd`, `Env`, `User`, ...) returns an `Id`; `POST /exec/{id}/start`
  with `{"Detach": false, "Tty": false}` sets up an interactive session (with `Detach: true`
  it returns immediately); `GET /exec/{id}/json` returns `Running` and `ExitCode`.
- Terminal size: `POST /exec/{id}/resize?h=40&w=120` and `POST /containers/{id}/resize`.

Go (Engine 29 client, `github.com/moby/moby/client`):
```go
create, _ := apiClient.ExecCreate(ctx, "web", client.ExecCreateOptions{
	Cmd: []string{"sh", "-c", "nginx -t"}, AttachStdout: true, AttachStderr: true})
att, _ := apiClient.ExecAttach(ctx, create.ID, client.ExecAttachOptions{})
defer att.Close()
stdcopy.StdCopy(os.Stdout, os.Stderr, att.Reader)
insp, _ := apiClient.ExecInspect(ctx, create.ID, client.ExecInspectOptions{})   // insp.ExitCode
```
`ExecAttach` returns a hijacked response; the caller must close it. Its doc comment describes
the same two stream formats (single raw stream with a TTY, multiplexed otherwise).

## Things that break streams
- **HTTP clients with read timeouts**: docker-py's default `timeout` is 60 seconds, which can
  cut idle `events` or `logs(follow=True)` streams; pass `timeout=None` to `docker.from_env` or
  reconnect using `since`.
- **Proxies in front of the API** must pass the `Upgrade` and `Connection` headers and avoid
  buffering the response, or attach/exec can hang.
- When reconnecting to `/events`, pass `since` (and handle duplicates in your code).
- `stats`: `one-shot=true` (with `stream=false`) returns a single sample instead of waiting for
  two collection cycles, because CPU usage needs two samples.

## Verify
```bash
docker run -d --name echo alpine sh -c 'while sleep 1; do date; date >&2; done'
curl -s --unix-socket /var/run/docker.sock 'http://localhost/v1.47/containers/echo/logs?stdout=1&stderr=1&tail=2' | xxd | head -2
# first byte of each frame: 01 for stdout, 02 for stderr
```

## Checked

2026-10-26 against Docker Engine API v1.56 reference and SDK pages (docker/docs main, 2026-10-23), Engine 29 release notes, moby/moby client source and API changelog, docker-py source, Tecnativa/docker-socket-proxy README. Confirmed: attach hijacking and 101 UPGRADED exchange, frame header layout and stream types, TTY raw stream versus multiplexed Content-Type values (changelog v1.42), stats stream and one-shot parameters (changelog v1.41), events since/until/filters, logs parameters, exec create/start/json/resize endpoints and body fields, Go client ExecCreate/ExecAttach/ExecInspect and stdcopy package path, docker-py default timeout 60. Removed unconfirmed claims about the daemon's event buffer, the CloseWrite half-close recipe, the Python attach_socket recipe, stats timing of about one second and the precpu zeroing detail.

Method: documentation only; no commands were run.
