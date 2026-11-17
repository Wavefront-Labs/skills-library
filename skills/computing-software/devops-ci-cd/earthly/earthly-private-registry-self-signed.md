---
id: computing-software.devops-ci-cd.earthly.earthly-private-registry-self-signed
name: earthly-private-registry-self-signed
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, self-signed, buildkit-additional-config, buildkit-additional-args, insecure, registry, mirrors, ca]
level: advanced
status: docs-checked
description: "Trust a self-signed registry CA in Earthly via buildkit_additional_args and buildkit_additional_config, allow insecure or http registries, and set mirrors or client keypairs."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/registries/self-signed.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Private registry with self-signed certificates in Earthly

Goal: push to and pull from a registry whose certificate is self-signed.

## Earthfile

Nothing special:

```
FROM alpine:3.18

build:
    RUN echo "Hello from Earthly!" > motd
    ENTRYPOINT cat motd
    SAVE IMAGE --push <registry-hostname>/hello-earthly:with-love
```

## Add the CA

In the Earthly config file set:

```yaml
global:
  buildkit_additional_args: ["-v", "<absolute-path-to-ca-file>:/etc/config/add.ca"]
  buildkit_additional_config: |
    [registry."<registry-hostname>"]
      ca=["/etc/config/add.ca"]
```

`<absolute-path-to-ca-file>` is the CA certificate on the host and `<registry-hostname>` is the registry host. The quotes are intended; keep them.

## Insecure registries (testing only)

Non-test use is strongly discouraged because of man-in-the-middle risk.

```yaml
global:
  buildkit_additional_config: |
    [registry."<registry-hostname>"]
      insecure = true
```

Also pass `--insecure` in the `SAVE IMAGE` command:

```
    SAVE IMAGE --push --insecure <registry-hostname>/hello-earthly:with-love
```

## Gotcha: http vs insecure

They are typically mutually exclusive. Use `insecure=true` only when the registry is https with an insecure certificate; use `http=true` only for a plain http registry (no SSL). If both are set, BuildKit tries http (port 80) or https (port 443).

## Other BuildKit registry options

```yaml
global:
  buildkit_additional_config: |
    [registry."<registry-hostname>"]
      mirrors = ["<mirror>"]
      http = true|false
      insecure = true|false
      ca=["<ca-path-pem>"]
      [[registry."<registry-hostname>".keypair]]
        key="<key-path-pem>"
        cert="<cert-path-pem>"
```

## Checked

2026-11-07. Read docs/guides/registries/self-signed.md in full. CA configuration, insecure setting with SAVE IMAGE --insecure, the http versus insecure note and the other BuildKit options block match. Nothing removed.
Method: documentation only; no commands were run.
