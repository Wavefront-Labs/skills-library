---
id: computing-software.cloud-infrastructure-engineering.docker.exec-via-the-engine-api
name: exec-via-the-engine-api
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-api, api-exec, docker-exec, hijacked-connection, docker-py, go-sdk]
level: advanced
status: docs-checked
description: "Run commands in containers via the Engine API: exec create, start (attached or detached), demultiplexing stdout/stderr frames, reading ExitCode, with curl, Python and Go."
sources: ["https://docs.docker.com/reference/api/engine/version/v1.56/#tag/Exec", "https://docs.docker.com/reference/api/engine/version/v1.56/#tag/Container/operation/ContainerAttach", "https://github.com/moby/moby/blob/master/client/container_exec.go", "https://github.com/docker/docker-py/blob/main/docker/models/containers.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exec via the Engine API

`docker exec` is three API calls: create an exec instance, start it, inspect it for the exit
code.

## curl over the socket
```bash
S=/var/run/docker.sock; V=v1.47
curl -s --unix-socket $S -H 'Content-Type: application/json' -X POST \
  "http://localhost/$V/containers/web/exec" \
  -d '{"AttachStdout":true,"AttachStderr":true,"Tty":false,"Cmd":["sh","-c","nginx -t"],"User":"root","Env":["X=1"]}'
# the response contains {"Id": "<exec id>"}
EXEC_ID=<id from the response>
curl -s --unix-socket $S -H 'Content-Type: application/json' -X POST \
  "http://localhost/$V/exec/$EXEC_ID/start" -d '{"Detach":false,"Tty":false}' --output out.bin
curl -s --unix-socket $S "http://localhost/$V/exec/$EXEC_ID/json"     # Running, ExitCode
```
Body fields for create (API v1.56): `AttachStdin`, `AttachStdout`, `AttachStderr`, `ConsoleSize`,
`DetachKeys`, `Tty`, `Env`, `Cmd`, `Privileged`, `User`, `WorkingDir`.

## The stream format
With `Tty: false`, stdout and stderr are multiplexed in frames:
`[stream type: 1 byte (1=stdout, 2=stderr)][3 zero bytes][payload size: 4 bytes big-endian][payload]`.
With `Tty: true`, the stream is raw (not multiplexed). Do not print the multiplexed stream as text;
demultiplex it (SDK helpers do).

## Python (docker-py)
```python
import docker
c = docker.from_env().containers.get("web")
res = c.exec_run(["sh", "-c", "nginx -t"], user="root", environment={"X": "1"}, demux=True)
print(res.exit_code, res.output[0], res.output[1])     # stdout bytes, stderr bytes
```
`exec_run` has a `demux` option returning stdout and stderr separately, and returns the exit code
from an exec inspect.

## Go (github.com/moby/moby/client, Engine 29 era)
```go
create, _ := apiClient.ExecCreate(ctx, "web", client.ExecCreateOptions{
    Cmd: []string{"sh", "-c", "nginx -t"}, AttachStdout: true, AttachStderr: true})
att, _ := apiClient.ExecAttach(ctx, create.ID, client.ExecAttachOptions{})
defer att.Close()
var stdout, stderr bytes.Buffer
stdcopy.StdCopy(&stdout, &stderr, att.Reader)          // demultiplex
insp, _ := apiClient.ExecInspect(ctx, create.ID, client.ExecInspectOptions{})
fmt.Println(insp.ExitCode, stdout.String(), stderr.String())
```
Older SDK releases (`github.com/docker/docker/client`) used different names such as
`ContainerExecCreate`; match the names to the module version you import.

## Gotchas
- `ExitCode` is only meaningful once `Running` is false; poll `GET /exec/{id}/json`.
- `Detach: true` on start returns immediately after starting the command.
- Exec access is as powerful as the API itself; restrict who can reach the socket.

## Checked

2026-10-26 against Docker Engine API v1.56 reference and SDK pages (docker/docs main, 2026-10-23), Engine 29 release notes, moby/moby client source and API changelog, docker-py source, Tecnativa/docker-socket-proxy README. Confirmed: exec create body fields, exec start Detach/Tty fields and detach behaviour, exec inspect fields (Running, ExitCode), multiplexed frame layout and TTY raw stream, Go client ExecCreate/ExecAttach/ExecInspect and options types, docker-py exec_run demux and exit-code lookup. Removed unconfirmed claims about exec instance cleanup, container restarts, the default user and authz plugins, and the jq extraction.

Method: documentation only; no commands were run.
