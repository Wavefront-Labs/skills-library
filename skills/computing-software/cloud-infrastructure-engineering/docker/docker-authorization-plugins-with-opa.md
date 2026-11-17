---
id: computing-software.cloud-infrastructure-engineering.docker.docker-authorization-plugins-with-opa
name: docker-authorization-plugins-with-opa
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-bench, authz-plugin, opa-docker-authz, rego, daemon-json, policy]
level: sme
status: docs-checked
description: "Enforce per-request Docker API policy with an authorization plugin (opa-docker-authz): install, daemon.json wiring, Rego denying privileged and host mounts, failure modes."
sources: ["https://github.com/open-policy-agent/opa-docker-authz", "https://github.com/open-policy-agent/opa-docker-authz/blob/main/example.rego", "https://docs.docker.com/engine/extend/plugins_authorization/", "https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/engine/security/protect-access/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker authorization plugins with OPA

Authorization plugins see every API request (method, path, headers, body, and the user name taken from the
TLS client certificate's common name when TLS is enabled) and allow or deny it. Docker's default model is
all or nothing; the opa-docker-authz plugin needs TLS so the daemon can identify the user.

## Install opa-docker-authz
```bash
sudo mkdir -p /etc/docker/policies
sudo tee /etc/docker/policies/authz.rego >/dev/null <<'EOF'
package docker.authz

default allow := false

allow if not deny

create if glob.match("/**/containers/create", ["/"], input.Path)

deny if {
  create
  input.Body.HostConfig.Privileged == true
}
deny if {
  create
  input.Body.HostConfig.PidMode == "host"
}
deny if {
  create
  input.Body.HostConfig.NetworkMode == "host"
}
deny if {
  create
  some bind in input.BindMounts
  startswith(bind.Resolved, "/var/run/docker.sock")
}
EOF
docker plugin install --alias opa-docker-authz openpolicyagent/opa-docker-authz-v2:0.8 \
  opa-args="-policy-file /opa/policies/authz.rego"
```
The managed plugin is granted a mount of `/etc/docker` at `/opa` inside the plugin (its working directory),
so a policy at `/etc/docker/policies/authz.rego` is `/opa/policies/authz.rego` to the plugin. The tag `0.8`
is the one in the plugin README; check it for the current tag. The Rego input is Docker's request JSON
plus `PathPlain`, `PathArr` and `BindMounts` (each with `Source`, `ReadOnly` and `Resolved`, the
symlink-resolved host path); `Resolved` defeats symlink tricks, but only works if the plugin can read
those host paths (the README suggests the legacy plugin run as root). The rule style (`if`, `in`,
`glob.match` on `input.Path`) follows the plugin's `example.rego`. If the plugin is installed without a
policy or config file, all requests fail open and are authorized.

## Wire it into the daemon
```json
{ "authorization-plugins": ["openpolicyagent/opa-docker-authz-v2:0.8"] }
```
```bash
sudo systemctl reload docker      # the daemon reloads its configuration on SIGHUP; the plugin README sends HUP
docker run --rm --privileged alpine true      # denied by the policy above
```
The `dockerd` reference lists the authorization plugin option among those that can be reconfigured on
reload. `dockerd --authorization-plugin=PLUGIN_ID` may be repeated for several plugins.

## Failure modes
- The Engine's authorization middleware fails closed: if the plugin returns an error or `Allow: false`, the
  request is denied. Keep an out-of-band way to fix a broken plugin: remove the key from daemon.json and
  restart dockerd.
- The plugin receives the raw request body, so it must not trust it blindly; do not rely on the response
  body for security decisions on streamed or large responses (Docker's authorization plugin docs).
- Authz protects against API users, not host root, who can change daemon.json.
- Bind mounts can come from `HostConfig.Binds` or `HostConfig.Mounts`; the plugin's `BindMounts` input
  covers both.

## Logging
With a policy file the plugin logs each request and decision as JSON (`input`, `result`, `decision_id`);
with `-config-file` full OPA decision logging is available (plugin README).

## Checked
Date: 2026-10-24. Documentation: opa-docker-authz README and `example.rego` (main), Docker docs authorization plugin page and `dockerd` reference (configuration reload, `authorization-plugins`) in docker/docs main.
- Confirmed the plugin install form (`docker plugin install --alias ... openpolicyagent/opa-docker-authz-v2:0.8 opa-args="-policy-file ..."`), the `/etc/docker` to `/opa` mount, fail-open when no policy is configured, the need for TLS to identify users, the daemon.json `authorization-plugins` key with `HUP` reload, the input fields (`Body`, `Path`, `PathPlain`, `PathArr`, `BindMounts[].Resolved`), and the Rego v1 constructs from `example.rego`.
- Confirmed the Engine fails closed on plugin error or `Allow: false` and that plugins receive the raw request body.
- The Rego policy was rewritten to the documented input shape; it was not executed here. Removed the CIS recommendation, the `v2:0.9` tag, the quoted error message, `opa eval` advice and the claim that Rego mistakes lock out `docker plugin disable`.
Method: documentation only; no commands were run.
