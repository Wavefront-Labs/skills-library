---
id: computing-software.cloud-infrastructure-engineering.docker.docker-desktop-kubernetes-and-extensions
name: docker-desktop-kubernetes-and-extensions
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-desktop, desktop-kubernetes, docker-extensions, kubeadm, kind, kubectl-context, extension-sdk, local-kubernetes]
level: practitioner
status: docs-checked
description: "Enable and use Docker Desktop's built-in Kubernetes (kubeadm vs kind), reset or upgrade it, mirror its images, and install, develop, validate and restrict Desktop Extensions."
sources: ["https://docs.docker.com/desktop/use-desktop/kubernetes/", "https://docs.docker.com/extensions/", "https://docs.docker.com/extensions/extensions-sdk/quickstart/", "https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/", "https://docs.docker.com/extensions/extensions-sdk/extensions/labels/", "https://docs.docker.com/extensions/extensions-sdk/extensions/validate/", "https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Desktop Kubernetes and Extensions

## Built-in Kubernetes
Dashboard, **Kubernetes** view, **Create cluster**, then pick the provisioner:

| | `kubeadm` | `kind` |
|---|---|---|
| Nodes | single node | multi-node |
| Kubernetes version | set by Docker Desktop | you choose |
| Enhanced Container Isolation | not supported (cluster works, unprotected) | supported (unprivileged containers) |
| containerd image store | works | works |
| Classic Docker image store | works | does not work |

The docs describe kubeadm as the older, slower provisioner (about 1 minute vs about 30 seconds
for kind). Creating a cluster also installs `kubectl` (on Linux you must install it yourself
at `/usr/local/bin/kubectl`). **Show system containers (advanced)** exposes the control-plane
containers in Docker commands.

```bash
kubectl version
kubectl config use-context docker-desktop    # if kubectl points elsewhere
kubectl get nodes
```
If no contexts appear, try Command Prompt or PowerShell, or point `KUBECONFIG` at your
`.kube/config`.

Housekeeping:
- **Edit cluster** switches kubeadm/kind or changes node count; **Stop** removes the
  Kubernetes containers and the `kubectl` it installed.
- Clusters are **not** upgraded automatically with Desktop updates; select **Reset cluster**
  in the Kubernetes settings to move to a new version. Reset also helps with stuck or
  corrupted state after an update.
- If Kubernetes fails to start, check Settings, Resources for enough CPU and memory.
- Control-plane images come from Docker Hub by default. `docker desktop kubernetes images
  list` shows the tags the installed release needs; mirror them (matching tags) to your own
  registry and set the Settings Management key `KubernetesImagesRepository` to override the
  `[registry[:port]/][namespace]` part of each name (restart Desktop afterwards).
- Admins can enable Kubernetes through Settings Management (`kubernetes.enabled`,
  `showSystemContainers`). Under ECI the Kubernetes system containers mount the Docker
  socket, so they must be on the ECI images allow-list or Kubernetes will not start.

## Extensions
Extensions run third-party tools inside Desktop with elevated privileges: direct access to
the Engine, filesystem access, native binaries. Docker reviews Marketplace submissions but
does not guarantee their security; side-loaded extensions are unreviewed.
```bash
docker extension install <name-of-your-extension>
docker extension rm <name-of-your-extension>
```
- Settings Management keys: `extensionsEnabled` (value false disables Extensions) and
  `onlyMarketplaceExtensions` (value true blocks installing others from the command line).
  Organisations can also configure a private marketplace.

### Writing one
```bash
docker extension init <my-extension>        # scaffold; needs Node.js and Go
docker extension validate <name-of-your-extension>
docker extension validate /path/to/metadata.json     # before the image is built
docker extension dev ui-source <name> http://localhost:3000   # UI hot reload
docker extension dev debug <name>                       # Chrome DevTools
docker extension dev reset <name>
```
`metadata.json` at the image root has `ui`, `vm` and `host` sections (`vm` can name an image,
for example `${DESKTOP_PLUGIN_IMAGE}`; `host` lists binaries). Required image labels include
`org.opencontainers.image.title`, `.description`, `.vendor`,
`com.docker.desktop.extension.api.version` (semver), `com.docker.desktop.extension.icon`,
`com.docker.extension.screenshots`, `.detailed-description`, `.publisher-url` and
`.changelog`; `additional-urls`, `account-info` and `categories` are optional. Validation
checks the labels and the metadata against the JSON schema published on the
docker/extensions-sdk releases page.

## Verify
```bash
kubectl --context docker-desktop get nodes
docker desktop kubernetes images list
```

## Checked
Date: 2026-10-26. Documentation: docker/docs repository main (last commit 2026-10-23): Kubernetes
view, Extensions overview and SDK pages, Settings Management JSON reference. Confirmed: the
provisioner comparison table, kubectl install location, reset/upgrade behaviour, image
mirroring setting and `docker desktop kubernetes images list`, extension CLI verbs, the
required labels, metadata sections, Settings Management keys. Removed as unconfirmed or
wrong: "Kubernetes upgrades with Desktop upgrades" (docs say it does not), kind "needs
sign-in", LoadBalancer/NodePort localhost publishing, imagePullPolicy advice,
`docker extension ls/update`, the example extension tag, "several GB of RAM" claim.
Method: documentation only; no commands were run.
