---
id: computing-software.cloud-infrastructure-engineering.rancher.rancher-behind-http-proxy-kubernetes-install
name: rancher-behind-http-proxy-kubernetes-install
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [proxy, noproxy, cert-manager, helm, catalogs, rke2, k3s]
level: practitioner
status: docs-checked
description: "Install Rancher and cert-manager behind an HTTP proxy: proxy and no_proxy settings for cert-manager, the proxy and noProxy chart values, and why Rancher needs external access."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/rancher-behind-an-http-proxy/install-rancher
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In a proxied environment both cert-manager and Rancher need to know the proxy. cert-manager needs it to reach Let's Encrypt or other external issuers; Rancher needs it to talk to external application catalogs and to retrieve Kubernetes version update metadata.

After installing the Helm CLI, add the Jetstack repo, create the `cert-manager` namespace and apply the cert-manager CRDs. Then install cert-manager with the proxy passed as chart values:

```
helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --set http_proxy=http://${proxy_host} \
  --set https_proxy=http://${proxy_host} \
  --set no_proxy=127.0.0.0/8\\,10.0.0.0/8\\,cattle-system.svc\\,172.16.0.0/12\\,192.168.0.0/16\\,.svc\\,.cluster.local
```

Wait for the `cert-manager` and `cert-manager-webhook` deployments to finish rolling out before continuing.

Rancher itself is installed with `proxy` and `noProxy`:

```
helm upgrade --install rancher rancher-latest/rancher \
   --namespace cattle-system \
   --set hostname=rancher.example.com \
   --set proxy=http://${proxy_host} \
   --set noProxy=127.0.0.0/8\\,10.0.0.0/8\\,cattle-system.svc\\,172.16.0.0/12\\,192.168.0.0/16\\,.svc\\,.cluster.local
```

Note the `noProxy` list includes `cattle-system.svc` along with the private ranges and the in-cluster domains. The page assumes the underlying RKE2 or K3s cluster is already running.

Order matters: the cert-manager CRDs go in first, the cert-manager chart second with its proxy values, and only after the `cert-manager` and `cert-manager-webhook` deployments have rolled out should the Rancher chart be installed. Commas inside the Helm value are escaped with a double backslash.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Rancher behind an HTTP proxy: Install Rancher. Removed an unsupported advice sentence about keeping the two lists identical.

Method: documentation only; no commands were run.
