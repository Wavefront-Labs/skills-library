---
id: computing-software.cloud-infrastructure-engineering.azure.aks-application-routing-add-on-and-ingress
name: aks-application-routing-add-on-and-ingress
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, app-routing, aks-ingress, ingress-nginx, application-routing-add-on, gateway-api, key-vault-certificates]
level: practitioner
status: docs-checked
description: "Expose AKS services with the application routing add-on (managed NGINX): internal/external controllers, Key Vault TLS certs, Azure DNS integration and alternatives."
sources: ["https://learn.microsoft.com/azure/aks/app-routing", "https://learn.microsoft.com/azure/aks/app-routing-dns-ssl", "https://learn.microsoft.com/azure/aks/app-routing-nginx-configuration", "https://learn.microsoft.com/azure/aks/app-routing-gateway-api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS application routing add-on and ingress

**Goal:** HTTP(S) ingress managed by AKS (upgrades, scaling), TLS certificates from Key Vault
and DNS records created automatically.

## Options
| Option | Use when |
|---|---|
| **Application routing add-on** (managed NGINX) | Default for most clusters; Microsoft upgrades the controller |
| Application routing Gateway API implementation | Long-term AKS direction for ingress: Gateway API is the standard AKS aligns with |
| Self-managed ingress-nginx (Helm) | Avoid for new work: the upstream Ingress NGINX project is retired (maintenance ended March 2026) |
| Application Gateway for Containers | Outside the cluster; supports both the Ingress API and the Gateway API |
| Istio add-on gateway | Already using the service mesh (Gateway API ingress without sidecars is possible) |

The add-on's NGINX Ingress support is limited to critical security patches through November 2026; plan the migration to the Gateway API implementation or Application Gateway for Containers. The rest of this skill covers the NGINX flavour for existing clusters.

## Enable
```bash
az aks approuting enable -g rg -n aks1
kubectl get nginxingresscontroller   # the default controller; AnnotationControlled gives it a public load balancer
```
Internal-only controller:
```yaml
apiVersion: approuting.kubernetes.azure.com/v1alpha1
kind: NginxIngressController
metadata: { name: nginx-internal }
spec:
  ingressClassName: nginx-internal
  controllerNamePrefix: nginx-internal
  loadBalancerAnnotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
```
Control the default controller with `az aks approuting update --nginx <type>`: `None` (not created, and not deleted if it exists), `Internal`, `External` or `AnnotationControlled` (the default: external load balancer, editable through annotations).

## TLS from Key Vault + DNS
```bash
az aks approuting update -g rg -n aks1 --enable-kv --attach-kv <keyvault-id>
az aks approuting zone add -g rg -n aks1 --ids <azure-dns-zone-id> --attach-zones
```
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: orders
  annotations:
    kubernetes.azure.com/tls-cert-keyvault-uri: https://kv-tls.vault.azure.net/certificates/orders-contoso-com
spec:
  ingressClassName: webapprouting.kubernetes.azure.com
  rules: [{ host: orders.contoso.com, http: { paths: [{ path: /, pathType: Prefix, backend: { service: { name: orders, port: { number: 80 } } } }] } }]
  tls: [{ hosts: [orders.contoso.com], secretName: keyvault-orders }]
```
The add-on uses the Key Vault provider for the Secrets Store CSI driver to fetch the certificate; enable the driver's secret autorotation so the add-on reloads certificates that change in Key Vault. DNS records are managed in the zones attached with `az aks approuting zone add`.

## Gotchas
- The add-on's managed identity needs the Key Vault Certificate User role on the vault and DNS Zone Contributor on the zones; `--attach-kv` and `--attach-zones` assign them using your own role-assignment permissions (for a vault on the access-policy model the grant works differently).
- Custom NGINX configuration is limited to the `NginxIngressController` properties and per-Ingress annotations the add-on supports.
- Upgrading from self-managed NGINX: run both classes in parallel and move Ingresses one by one.

## Verify
- [ ] `kubectl get ingress -A` shows ADDRESS populated; `curl -v https://orders.contoso.com` presents the Key Vault cert.
- [ ] The DNS record for the host exists in the attached zone.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (app-routing, app-routing-dns-ssl, app-routing-nginx-configuration, ingress-nginx-retirement include dated 14 October 2026; main branch).
- Confirmed: `az aks approuting enable`, `update --enable-kv --attach-kv`, `zone add --ids --attach-zones`; `NginxIngressController` (`approuting.kubernetes.azure.com/v1alpha1`) properties `ingressClassName`, `controllerNamePrefix`, `loadBalancerAnnotations` and the internal annotation; `--nginx` values and default; ingress class `webapprouting.kubernetes.azure.com`; the `kubernetes.azure.com/tls-cert-keyvault-uri` annotation and `keyvault-<ingress>` secret name; roles granted by the attach flags; ingress-nginx retirement and add-on NGINX support window (November 2026); Gateway API as the long-term standard.
- Removed as unconfirmed: the add-on identity name, `configuration-snippet` being disabled, ExternalDNS and TXT ownership records, landing-zone policy remark.
Method: documentation only; no commands were run.
