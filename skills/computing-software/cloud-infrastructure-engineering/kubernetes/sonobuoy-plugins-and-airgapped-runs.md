---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sonobuoy-plugins-and-airgapped-runs
name: sonobuoy-plugins-and-airgapped-runs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, sonobuoy, sonobuoy-plugins, sonobuoy-airgap, kube-bench, conformance, cluster-validation]
level: practitioner
status: docs-checked
description: "Extend Sonobuoy with custom plugins (job and daemonset, e.g. kube-bench on every node), run it in air-gapped clusters with image remapping, and collect results."
sources: ["https://sonobuoy.io/docs/main/plugins/", "https://sonobuoy.io/docs/main/airgap/", "https://github.com/vmware-tanzu/sonobuoy-plugins", "https://github.com/vmware-tanzu/sonobuoy/blob/main/site/content/docs/main/cli/sonobuoy_images_push.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sonobuoy plugins and air-gapped runs

## Plugin model
A plugin is a YAML: `sonobuoy-config` (`plugin-name`, `driver` `Job` = one pod or `DaemonSet` = one per
node, `result-type`: raw/junit/gojson/manual) + a pod `spec`. The sidecar waits for a "done file"
(default `/tmp/results/done`, set by `ResultsDir`) containing the path of the results file and uploads it.
```yaml
sonobuoy-config:
  driver: DaemonSet
  plugin-name: kube-bench-node
  result-type: junit
spec:
  name: plugin
  image: <your-plugin-image>      # replace with your own image
  command: ["/bin/sh","-c"]
  args: ["my-check --junit > /tmp/results/out.xml; echo -n /tmp/results/out.xml > /tmp/results/done"]
  volumeMounts: [{name: results, mountPath: /tmp/results}]
```
Example plugins are collected in `vmware-tanzu/sonobuoy-plugins`.
```bash
sonobuoy gen plugin --name=my-check --image=myorg/check:1.0 --type=daemonset --format=junit > my-check.yaml   # scaffold (defaults: job, raw)
sonobuoy run -p e2e -p my-check.yaml --wait
sonobuoy status --json; sonobuoy results $(sonobuoy retrieve) --plugin my-check
sonobuoy delete --all --wait
```
DaemonSet plugins run on every node including control-plane nodes; customise the PodSpec (`podSpec`
in the plugin definition) for tolerations.

## Air-gapped
```bash
sonobuoy images list --kubernetes-version <version>                  # images for a given cluster version (default: auto-detect)
sonobuoy images pull                                                 # to the local docker client (connected side)
sonobuoy images download                                             # save pulled images to a tar file
sonobuoy gen default-image-config > custom-repos.yaml                # edit: map registries to your private registry
sonobuoy images push --e2e-repo-config custom-repos.yaml             # or --e2e-repo <registry>, or --custom-registry <registry>
sonobuoy run --sonobuoy-image <registry>/sonobuoy:<version> \
  --kube-conformance-image <registry>/conformance:<cluster-version> \
  --systemd-logs-image <registry>/sonobuoy-plugin-systemd-logs:<tag> \
  --e2e-repo-config custom-repos.yaml
```
The docs say to push the Sonobuoy, conformance and systemd-logs images yourself (pull, tag, push)
and to supply the registry mapping to both `images push` and `sonobuoy run` (`--e2e-repo` for a
single registry). `images pull` may report some images that cannot be pulled; the docs say these
are used by non-conformance tests.

## Gotchas
- To skip the `systemd-logs` plugin, pass `-p e2e` (plugins are chosen with `--plugin`).

## Verify
- [ ] `sonobuoy status` shows all plugins complete and passed; tarball archived per run.

## Checked

2026-10-26, against Sonobuoy docs in vmware-tanzu/sonobuoy (site/content/docs/main, CLI reference auto-generated 1-Jul-2026; sonobuoy run default image v0.57.5; repo last pushed 2026-10-14). Confirmed: `result-type` values, default done file `/tmp/results/done`, Job/DaemonSet drivers, `gen plugin` flags and defaults, run flags (`--sonobuoy-image`, `--kube-conformance-image`, `--systemd-logs-image`, `--e2e-repo`, `--e2e-repo-config`, `-p`), `images list/pull/download/push` and `--custom-registry`, `gen default-image-config`. Wrong: `result-format` key (it is `result-type`), `/tmp/sonobuoy/results` as the default, `sonobuoy images save` (the command is `images download`). Removed the unconfirmed kube-bench image and args, pinned versions, PSA/Gatekeeper claim and the ImagePullBackOff claim.

Method: documentation only; no commands were run.
