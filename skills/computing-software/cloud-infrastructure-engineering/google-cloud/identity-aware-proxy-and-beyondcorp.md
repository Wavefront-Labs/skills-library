---
id: computing-software.cloud-infrastructure-engineering.google-cloud.identity-aware-proxy-and-beyondcorp
name: identity-aware-proxy-and-beyondcorp
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, identity-aware-proxy, iap, beyondcorp, beyondcorp-enterprise, chrome-enterprise-premium, context-aware-access, access-levels, access-context-manager, zero-trust, iap-tcp-forwarding, iap-jwt, x-goog-iap-jwt-assertion, oauth-consent, iap-web, load-balancer-auth, httpsresource-accessor]
level: practitioner
status: docs-checked
description: "Put Identity-Aware Proxy in front of web apps and SSH/RDP on GCP: IAP-secured Web App User role, access levels for device and IP context, and JWT verification in the backend."
sources: ["https://cloud.google.com/iap/docs/concepts-overview", "https://cloud.google.com/iap/docs/enabling-compute-howto", "https://cloud.google.com/iap/docs/signed-headers-howto", "https://cloud.google.com/iap/docs/using-tcp-forwarding", "https://cloud.google.com/beyondcorp-enterprise/docs/overview", "https://cloud.google.com/access-context-manager/docs/create-access-level"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity-Aware Proxy and BeyondCorp

**Goal:** internal apps reachable from anywhere without a VPN, where every request is
authenticated by Google identity, authorised by IAM, optionally gated on device posture,
and the backend cannot be reached except through the proxy.

## 1. Enable IAP on an HTTPS load-balanced app
1. Backend must be behind an **external or internal Application Load Balancer** (IAP is a
   backend-service feature). App Engine and Cloud Run are supported directly.
2. Set up the OAuth consent screen and OAuth client as the *Enabling IAP for Compute Engine* guide describes (a
   Google-managed or a custom OAuth client; see *Sharing OAuth clients* for the custom case).
3. `gcloud compute backend-services update <BACKEND> --global --iap=enabled` (console: Security → IAP → toggle).
4. Grant access: `gcloud iap web add-iam-policy-binding --resource-type=backend-services --service=<BACKEND> --member=group:app-users@example.com --role=roles/iap.httpsResourceAccessor`.
5. **Lock the backend** so IAP cannot be bypassed: firewall rules that allow only the load balancer and health-check
   ranges Google documents for your load balancer type to reach the instance port, and for
   Cloud Run set ingress to `internal-and-cloud-load-balancing`.

## 2. Verify identity in the backend (do not trust `X-Goog-Authenticated-User-*` alone)
IAP adds `X-Goog-IAP-JWT-Assertion`; verify it with Google's public keys
(`https://www.gstatic.com/iap/verify/public_key-jwk`; the JSON-map form is `.../public_key`), checking `iss` =
`https://cloud.google.com/iap` and `aud` by product: Compute Engine and GKE
`/projects/<PROJECT_NUMBER>/global/backendServices/<SERVICE_ID>`, App Engine `/projects/<PROJECT_NUMBER>/apps/<PROJECT_ID>`,
Cloud Run `/projects/<PROJECT_NUMBER>/locations/<REGION>/services/<SERVICE_NAME>`. Allow 30 seconds of clock skew on
`iat`/`exp`. If an attacker bypasses IAP they can forge `x-goog-authenticated-user-*`, so verify the JWT.

## 3. Context-aware access (BeyondCorp Enterprise / Chrome Enterprise Premium)
- Create an **access level** in Access Context Manager: IP ranges, regions, device policy
  (encrypted disk, screen lock, OS version, corporate-owned via Endpoint Verification).
  ```bash
  gcloud access-context-manager levels create corp_devices --policy=<POLICY_ID> \
    --title="Corp managed" --basic-level-spec=level.yaml
  ```
  `level.yaml`: `- devicePolicy: {requireScreenlock: true, allowedEncryptionStatuses: [ENCRYPTED]}` (field names from the Access Context Manager `DevicePolicy` schema).
- Bind it as an IAM **condition** on the IAP role:
  `"accessPolicies/<POLICY_ID>/accessLevels/corp_devices" in request.auth.access_levels`.
- Device-based levels depend on device data such as Endpoint Verification; test with one device before binding to a group.

## 4. IAP TCP forwarding (SSH/RDP without public IPs)
- Firewall: allow `35.235.240.0/20` to tcp:22/3389.
- Role `roles/iap.tunnelResourceAccessor` on the project or the VM (conditions can use `destination.port` and access levels).
- `gcloud compute ssh <VM> --tunnel-through-iap` or `gcloud compute start-iap-tunnel <VM> 3389 --local-host-port=localhost:3389`.
- Google states TCP forwarding is not intended for bulk data transfer and IAP may rate-limit abusers — fine for admin, not for file transfer.

## Gotchas
- Programmatic clients send an ID token whose audience is the IAP OAuth client ID
  (`gcloud auth print-identity-token --audiences=<CLIENT_ID>` or a service account), in `Authorization` or
  `Proxy-Authorization`; the caller also needs `roles/iap.httpsResourceAccessor`.
- Grant access on each IAP-protected resource you enable (`gcloud iap web add-iam-policy-binding ...`).

## Verify
- [ ] Hitting the instance IP directly is refused by the firewall; via the LB a Google sign-in appears.
- [ ] Backend logs show the verified JWT `email` claim, and a request with a forged `X-Goog-Authenticated-User-Email` but no JWT is rejected.
- [ ] A user outside the access level is refused.
- [ ] `gcloud compute ssh --tunnel-through-iap` works with no external IP on the VM.

## Checked

- Date: 2026-10-27
- Confirmed against the IAP signed-headers guide (JWT header, public key URLs, `iss`, `aud` forms per product, 30-second skew), IAP TCP forwarding guide (35.235.240.0/20, bulk-transfer limitation, `request.auth.access_levels` condition form), the roles reference (`roles/iap.httpsResourceAccessor`, `roles/iap.tunnelResourceAccessor`), gcloud references for `compute backend-services update --iap=enabled`, `iap web add-iam-policy-binding`, `access-context-manager levels create`, `compute ssh --tunnel-through-iap`, `compute start-iap-tunnel`, and the Access Context Manager `DevicePolicy` schema (`requireScreenlock`, `allowedEncryptionStatuses`).
- Removed or corrected: the 130.211.0.0/22 and 35.191.0.0/16 ranges (not confirmed on the pages read), manual-OAuth-client history, Endpoint-Verification lock-out claim, gRPC, WebSocket and CORS statements, internal load balancer note, per-backend 403 note and the audit-log field. Corrected the `aud` value, which differs by product.

Method: documentation only; no commands were run.
