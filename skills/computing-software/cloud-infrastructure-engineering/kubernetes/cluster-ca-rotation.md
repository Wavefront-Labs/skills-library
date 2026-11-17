---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-ca-rotation
name: cluster-ca-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ca-rotation, pki, kubeadm, certificates, service-account-keys, trust-bundle]
level: advanced
status: docs-checked
description: "Rotate a kubeadm cluster's root CA without downtime by running old and new CAs side by side as a trust bundle, re-issuing leaf certs, then removing the old CA."
sources: ["https://kubernetes.io/docs/tasks/tls/manual-rotation-of-ca-certificates/", "https://kubernetes.io/docs/setup/best-practices/certificates/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rotating the cluster CA

`kubeadm certs renew` only renews **leaf** certificates signed by the existing CA. Replacing
`ca.crt` itself (compromise, 10-year expiry, key policy) is a manual multi-phase job.
Doing it in one step breaks kubelets, controllers and kubeconfigs at once.

The upstream task assumes an HA control plane with several API servers and graceful API
server termination so clients can reconnect to another instance. A single API server is
unavailable while it restarts.

## Phases (per the upstream task, "Manual Rotation of CA Certificates")
1. **Back up** the certificate directory, configuration files and kubeconfigs on every
   control-plane node, plus an etcd snapshot.
2. **Distribute the new CA material** (`ca.crt`, `ca.key`, and the front-proxy CA files if
   rotating that too) to all control-plane nodes in the certificates directory.
3. **Trust both CAs everywhere that verifies.** Set kube-controller-manager
   `--root-ca-file` to a file holding old and new CA, then restart it: ServiceAccount
   objects created after this point carry both CAs. Wait until the controller manager has
   updated the CA data for existing ServiceAccounts.
   - The files named by kube-controller-manager `--client-ca-file` and
     `--cluster-signing-cert-file` **cannot be CA bundles**. If they point at the same
     `ca.crt` as `--root-ca-file`, copy the new CA to a separate file for those two flags
     until the bundle is no longer needed.
4. **Restart workloads that read CA data from their ServiceAccount** (kube-proxy, CoreDNS
   and any other in-cluster client) so they pick up the bundle, and check they work.
5. **Append both CAs** to the files behind `--client-ca-file` and
   `--kubelet-certificate-authority` on kube-apiserver and behind `--client-ca-file` on
   kube-scheduler. Update user client certificates and the `certificate-authority-data` in
   kubeconfig files (bundle of old and new). Update `--root-ca-file` for
   cloud-controller-manager if you run one.
6. **Roll through the rest, one node or component at a time:** restart aggregated API
   servers and webhook handlers so they trust the new CA; restart kubelets with
   `clientCAFile` and the `kubelet.conf` CA data holding both CAs (if kubelet client
   certificate rotation is off, replace the kubelet client certificate and key too);
   restart the API servers with `apiserver.crt`, `apiserver-kubelet-client.crt` and
   `front-proxy-client.crt` signed by the new CA, then the scheduler.
7. **Trigger a rolling restart of Deployments and DaemonSets** (the task patches a pod
   template annotation such as `ca-rotation: "1"`) and consider StatefulSets too; use
   PodDisruptionBudgets to limit disruption.
8. **If bootstrap tokens are used to join nodes**, update `certificate-authority-data` in
   the `cluster-info` ConfigMap in the `kube-public` namespace with the new CA.
9. **Verify**, then **remove the old CA** from ServiceAccount CA data (pods using an
   in-cluster kubeconfig must eventually restart), from kubeconfig files, from the
   `--client-ca-file` and `--root-ca-file` files, and from each kubelet's `clientCAFile`
   and kubeconfig, restarting components in a rolling fashion.

```bash
# confirm which CA signed what
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -issuer -enddate
# count certificates in a bundle file (2 during the overlap)
grep -c BEGIN <path-to-ca-bundle>
```

## Gotchas
- Service-account tokens are signed by `sa.key`, **not** the CA, so CA rotation does not
  invalidate tokens. The kube-apiserver `--service-account-key-file` flag accepts several
  keys (and can be repeated), so add the new public key there first, then switch
  `--service-account-signing-key-file`, and remove the old key later.
- Webhooks and aggregated APIs whose `caBundle` holds the cluster CA must be updated too.
- Managed clusters rotate credentials through the provider; follow the provider's
  documentation rather than this procedure.

## Verify
- [ ] Control-plane logs, kubelet and kube-proxy logs show no TLS errors, and aggregated API
      servers and in-cluster clients work.
- [ ] Every kubeconfig and ServiceAccount CA bundle contains only the new CA at the end.
- [ ] Old CA key destroyed or archived per policy.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: upstream task page 'Manual Rotation of CA Certificates' (HA assumption, --root-ca-file bundle and the client-ca-file and cluster-signing-cert-file restriction, apiserver/scheduler/kubelet CA bundles, cloud-controller-manager, aggregated API and webhook restarts, rolling restart, cluster-info ConfigMap, final removal of the old CA) and the kube-apiserver reference (--service-account-key-file accepts multiple keys). Removed unconfirmed managed-service commands, the kubelet certificate deletion step and the kube-root-ca.crt ConfigMap claims.

Method: documentation only; no commands were run.
