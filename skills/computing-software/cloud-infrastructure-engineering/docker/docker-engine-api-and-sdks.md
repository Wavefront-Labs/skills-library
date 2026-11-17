---
id: computing-software.cloud-infrastructure-engineering.docker.docker-engine-api-and-sdks
name: docker-engine-api-and-sdks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-api, engine-api, docker-sdk, api, docker-py, moby-client, unix-socket, api-version, curl-unix-socket, dockerode, go-sdk, python-sdk, socket-proxy]
level: advanced
status: docs-checked
description: "Talking to the Docker Engine directly: curl over the unix socket, API version negotiation, the Go and Python SDKs for create/start/logs/events, and the socket-proxy pattern for least privilege."
sources: ["https://docs.docker.com/reference/api/engine/", "https://docs.docker.com/reference/api/engine/sdk/", "https://docs.docker.com/reference/api/engine/sdk/examples/", "https://docs.docker.com/engine/release-notes/29/", "https://github.com/moby/moby/tree/master/client", "https://github.com/docker/docker-py", "https://github.com/Tecnativa/docker-socket-proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Engine API and SDKs

**Goal:** automate the daemon from a program (CI tooling, a deploy bot, a dashboard, an
integration test harness) with the official clients, correctly versioned, and without
handing the program root on the host.

## The API is just HTTP over the socket
Everything the CLI does is a REST call. Explore it with curl:
```bash
curl -s --unix-socket /var/run/docker.sock http://localhost/version
curl -s --unix-socket /var/run/docker.sock 'http://localhost/v1.47/containers/json?all=1'
curl -s --unix-socket /var/run/docker.sock -X POST \
  -H 'Content-Type: application/json' http://localhost/v1.47/containers/create?name=hello \
  -d '{"Image":"alpine","Cmd":["echo","hi"],"HostConfig":{"AutoRemove":false}}'
curl -s --unix-socket /var/run/docker.sock -X POST http://localhost/v1.47/containers/hello/start
curl -s --unix-socket /var/run/docker.sock 'http://localhost/v1.47/containers/hello/logs?stdout=1' | tail -c +9
curl -s --unix-socket /var/run/docker.sock 'http://localhost/v1.47/events?filters=%7B%22type%22%3A%5B%22container%22%5D%7D'
```
- Put the API version first in the path (`/v1.47/...`). `docker version` shows the client and
  server `API version` and the server's minimum version. Docker's docs show the minimum as
  1.40 for current engines; Docker Engine 29.0 raised the minimum to 1.44 and 29.3 lowered it
  back to 1.40, so check the daemon you target. A client that requests a version the daemon
  does not know gets an error; set `DOCKER_API_VERSION` to force the CLI or SDKs to use an
  older version.
- Logs/attach streams for non-TTY containers are **multiplexed**: each frame is an 8-byte
  header (`[stream type, 0,0,0, big-endian uint32 size]`) then the payload, hence `tail -c +9`
  above to skip one header; real code must parse frames (`stdcopy.StdCopy` in Go,
  `demux=True` on `exec_run` in docker-py).
- `HostConfig` holds runtime settings (`Binds`, `PortBindings`, `Memory`, `RestartPolicy`,
  `CapDrop`); `Config` is the image-like part (`Env`, `Cmd`, `Labels`, `ExposedPorts`).
- `/_ping` returns headers including `Api-Version` and `Builder-Version`.
- For TCP endpoints with TLS see `remote-daemon-tls-ssh-and-contexts`.

## Go
Install with `go get github.com/moby/moby/client`. This example is the one in Docker's SDK docs
(Engine 29 era client; older code used `github.com/docker/docker/client`, whose signatures differ):
```go
import (
	"context"; "io"; "os"
	"github.com/moby/moby/api/pkg/stdcopy"
	"github.com/moby/moby/api/types/container"
	"github.com/moby/moby/client"
)

ctx := context.Background()
apiClient, err := client.New(client.FromEnv)
defer apiClient.Close()

reader, err := apiClient.ImagePull(ctx, "docker.io/library/alpine", client.ImagePullOptions{})
io.Copy(os.Stdout, reader)

resp, err := apiClient.ContainerCreate(ctx, client.ContainerCreateOptions{
	Image:  "alpine",
	Config: &container.Config{Cmd: []string{"echo", "hello world"}},
})
_, err = apiClient.ContainerStart(ctx, resp.ID, client.ContainerStartOptions{})
wait := apiClient.ContainerWait(ctx, resp.ID, client.ContainerWaitOptions{})
select {
case err := <-wait.Error:
	if err != nil { panic(err) }
case <-wait.Result:
}
out, err := apiClient.ContainerLogs(ctx, resp.ID, client.ContainerLogsOptions{ShowStdout: true})
stdcopy.StdCopy(os.Stdout, os.Stderr, out)
```
- `client.FromEnv` reads `DOCKER_HOST`, `DOCKER_API_VERSION`, `DOCKER_CERT_PATH` and
  `DOCKER_TLS_VERIFY`. By default the client negotiates the API version on its first request,
  downgrading for older daemons; `WithAPIVersion` or `WithAPIVersionFromEnv` fixes the version
  and disables negotiation.
- Docker contexts are not read by the client; resolve the endpoint yourself.

## Python (docker-py)
```python
import docker
client = docker.from_env()                     # or DockerClient(base_url="ssh://user@host", use_ssh_client=True)
c = client.containers.run("alpine", ["echo", "hi"], detach=True, name="hello",
                          mem_limit="256m", labels={"owner": "bot"})
print(c.wait())                                # {'StatusCode': 0, ...}
print(c.logs(stdout=True, stderr=False).decode())
for ev in client.events(decode=True, filters={"type": "container"}):
    print(ev["Action"], ev["Actor"]["Attributes"].get("name"))
```
- `pip install docker` is the recommended install (Docker's SDK page). `from_env` takes
  `version` (default `auto`) and `timeout` (default 60 seconds).
- `containers.run` raises `docker.errors.ContainerError` on a non-zero exit when run attached.
- `c.exec_run(cmd, demux=True)` returns exit code plus a `(stdout, stderr)` tuple.
- Community libraries for other languages (for example dockerode for Node, bollard for Rust,
  Docker.DotNet for C#, docker-java) are listed in Docker's SDK docs as untested by Docker.

## Least privilege: never mount the socket into app containers raw
Any process with the socket can control the daemon. For dashboards/agents that need read-only
access, put a filtering proxy in front, such as Tecnativa/docker-socket-proxy, which returns
`403 Forbidden` for requests whose section is not enabled:
```yaml
services:
  socket-proxy:
    image: tecnativa/docker-socket-proxy     # pin a current release (latest at check time: v0.5.0)
    environment: {CONTAINERS: 1, EVENTS: 1, PING: 1, VERSION: 1, POST: 0}
    volumes: ["/var/run/docker.sock:/var/run/docker.sock:ro"]
    networks: [socket]
  traefik:
    environment: {DOCKER_HOST: "tcp://socket-proxy:2375"}
    networks: [socket, web]
```
`POST: 0` limits the proxy to GET and HEAD requests. Check the proxy's README for the full list
of section variables.

## Verify
```bash
curl -s --unix-socket /var/run/docker.sock http://localhost/_ping -i
docker version --format '{{.Client.APIVersion}} {{.Server.APIVersion}} {{.Server.MinAPIVersion}}'
```

## Checked

2026-10-26 against Docker Engine API v1.56 reference and SDK pages (docker/docs main, 2026-10-23), Engine 29 release notes, moby/moby client source and API changelog, docker-py source, Tecnativa/docker-socket-proxy README. Confirmed: Go SDK install path and example (client.New, FromEnv variables, ContainerCreateOptions, ContainerWait result/error channels), version negotiation, docker version minimum API (1.40) and the Engine 29.0 and 29.3 release-note entries on the minimum, multiplexed frame layout, /_ping headers, docker-py defaults (timeout 60, from_env version auto, exec_run demux, ContainerError, events), community library list, docker-socket-proxy variables and 403 behaviour. Removed the unconfirmed jq pipelines, the Docker 27 version floor, the error-message text, the pinned proxy tag, authz and rootless suggestions, and the SDK pull-cancellation claim.

Method: documentation only; no commands were run.
