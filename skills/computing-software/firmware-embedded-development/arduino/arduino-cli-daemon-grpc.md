---
id: computing-software.firmware-embedded-development.arduino.arduino-cli-daemon-grpc
name: arduino-cli-daemon-grpc
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-cli-daemon, grpc, arduino-cli-api, tool-integration, protobuf, ide-backend, arduino-cli, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Drive arduino-cli as a gRPC service: start the daemon, create and init instances, call Compile/Upload/BoardList from Python or Go, stream progress, and versioning caveats."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/rpc/cc/arduino/cli/commands/v1/commands.proto
  - https://github.com/arduino/arduino-cli/blob/master/rpc/cc/arduino/cli/commands/v1/compile.proto
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/daemon/daemon.go
  - https://github.com/arduino/arduino-cli/blob/master/docs/integration-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# arduino-cli daemon (gRPC)

`arduino-cli daemon` exposes the full CLI as a gRPC API (the Arduino IDE 2.x backend uses it).
Use it when building tools (test farms, custom IDEs, web flashers on a host) that would otherwise
parse CLI text output.

## Start
```sh
arduino-cli daemon --port 50051 --daemonize      # listens on 127.0.0.1; keep running if the parent dies
arduino-cli daemon --port 50051 --debug          # log every gRPC call
```

## Workflow
1. `Create` an instance -> instance id.
2. `Init` the instance (streams progress while loading indexes, cores, libraries).
3. Call services with that instance: `Compile`, `Upload`, `BoardList`, `BoardListWatch`,
   `LibraryInstall`, `PlatformInstall`, `Monitor`, `Debug`, `UpdateIndex`.
4. `Destroy` when done.

## Python client
Generate stubs from the `.proto` files in the repo's `rpc/cc/arduino/cli/commands/v1/` matching
your CLI version:
```sh
python -m grpc_tools.protoc -I rpc --python_out=gen --grpc_python_out=gen \
  rpc/cc/arduino/cli/commands/v1/*.proto
```
```python
import grpc
from cc.arduino.cli.commands.v1 import commands_pb2 as pb, commands_pb2_grpc as svc, compile_pb2
ch = grpc.insecure_channel("localhost:50051"); cli = svc.ArduinoCoreServiceStub(ch)
inst = cli.Create(pb.CreateRequest()).instance
for _ in cli.Init(pb.InitRequest(instance=inst)): pass
req = compile_pb2.CompileRequest(instance=inst, fqbn="arduino:avr:uno",
                                 sketch_path="/work/blink", export_dir="/work/out")
for msg in cli.Compile(req):          # server-streaming: progress, out/err stream, result
    if msg.HasField("out_stream"): print(msg.out_stream.decode(), end="")
```

## Caveats
- Generate stubs from the `.proto` files of the same release tag as the CLI you run, and pin that
  CLI version.
- Many calls are server-streaming; handle progress and errors from the stream, not only the final
  message.
- Change settings through the `ArduinoCoreService` calls (`SettingsSetValue`, `ConfigurationSave`)
  rather than editing the YAML while the daemon runs.
- No authentication: keep it on localhost or behind a trusted proxy.

## Verify
- [ ] Script compiles and uploads a sketch purely through gRPC, with streamed output.
- [ ] Stub generation is part of the build, tied to the pinned CLI version.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 source and docs on master (commit 2026-10-22).

Confirmed: `daemon` flags `--port`, `--daemonize`, `--debug`; the daemon listens on 127.0.0.1; a single gRPC service `ArduinoCoreService` with `Create`, `Init` (server-streaming), `Destroy`, `Compile` (stream, response is a oneof with `out_stream`), `Upload`, `BoardList`, `BoardListWatch`, `LibraryInstall`, `PlatformInstall`, `UpdateIndex`, `Monitor`, `Debug`; `CompileRequest.sketch_path` and `export_dir`; settings calls `SettingsSetValue` and `ConfigurationSave` are on the same service; Arduino IDE 2.x uses daemon mode (integration options page). Fixed: there is no separate `SettingsService`. Removed the unconfirmed 0.35 release remark and the sentence about Go import paths.

Method: documentation only; no commands were run.
