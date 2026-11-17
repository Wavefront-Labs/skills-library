---
id: computing-software.cloud-infrastructure-engineering.talos-linux.extension-service-manifest
name: extension-service-manifest
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [extension-services, system-extensions, container, depends, privileged, talosctl-service]
level: sme
status: docs-checked
description: "Write an extension service manifest: name, container entrypoint and mounts, security flags, depends conditions, restart policy and logToConsole for early boot services."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/build-and-extend-talos/custom-images-and-development/extension-services.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Extension services are privileged containers started early in boot, shipped inside the root filesystem (usually via a system extension). They fit cases a static pod or DaemonSet cannot, such as open-iscsi, software RAID, BGP FRR or VMware tools. At boot Talos scans `/usr/local/etc/containers` for `*.yaml` manifests:

```yaml
name: hello-world
container:
  entrypoint: ./hello-world
  environment:
    - XDG_RUNTIME_DIR=/run
  args:
     - -f
  mounts:
     - # OCI Mount Spec
depends:
   - configuration: true
   - service: cri
   - path: /run/machined/machined.sock
   - network:
       - addresses
       - connectivity
       - hostname
       - etcfiles
   - time: true
restart: never|always|untilSuccess
logToConsole: true|false
```

- `name`: `[a-z0-9-_]+`. The container root is `/usr/local/lib/containers/<name>`; the service is registered as `ext-<name>`.
- `container.mounts`: standard OCI mount spec; missing writable source directories are created.
- `container.security`: `maskedPaths`, `readonlyPaths`, `writeableRootfs`, `writeableSysfs`, `rootfsPropagation`. Rootfs and sysfs are read-only by default.
- `depends`: `service`, `path`, `network`, `time: true`, and `configuration: true` which waits for an `ExtensionServiceConfig` of the same name. Using that config without declaring `configuration: true` is unsupported.
- `restart`: `always`, `never` or `untilSuccess`.
- `logToConsole`: also writes logs to the console, useful in maintenance mode or early boot.

Manage with `talosctl service ext-hello-world start|restart|stop` and `talosctl logs ext-hello-world`.

## Checked

2026-11-04. Manifest format, field semantics, ExtensionServiceConfig warning and service management commands confirmed on the Extension Services page.

Method: documentation only; no commands were run.
