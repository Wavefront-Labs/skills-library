---
id: computing-software.cloud-infrastructure-engineering.harbor.notation-signing
name: notation-signing
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [notation, notary, trust-policy, notation-verify, harbor]
level: practitioner
status: docs-checked
description: "Sign and verify Harbor artifacts with the Notation CLI: test certificate, registry credentials, notation sign, trust policy import and verify."
sources:
  - https://goharbor.io/docs/main/working-with-projects/working-with-images/sign-images/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Notation signs OCI artifacts using distribution spec v1.1 mode and stores signatures in Harbor.

1. Install: `brew install notation` (other platforms are in the Notation installation guide).
2. Test key and self-signed certificate, for development only: `notation cert generate-test --default "wabbit-networks.io"`. Use a CA-issued certificate in production.
3. Authenticate with environment variables: `export NOTATION_USERNAME="YOUR_REGISTRY_USERNAME"` and `export NOTATION_PASSWORD="YOUR_REGISTRY_PASSWORD"`.
4. Sign an image already pushed over HTTPS: `notation sign <harbor-domain>/<image-reference>`. The signed status in Harbor turns to a green tick.
5. Create `trustpolicy.json` and import it with `notation policy import ./trustpolicy.json`:
```json
{
  "version": "1.0",
  "trustPolicies": [
    {
      "name": "wabbit-networks-images",
      "registryScopes": ["*"],
      "signatureVerification": { "level": "strict" },
      "trustStores": ["ca:wabbit-networks.io"],
      "trustedIdentities": ["*"]
    }
  ]
}
```
6. Verify: `notation verify <harbor-domain>/<image-reference>`. Inspect signatures and certificates with `notation inspect $IMAGE`.

To make Harbor itself refuse unsigned pulls, tick **Notation** under project Configuration.

A signed artifact shows its status in the Harbor UI once the signature is pushed. The self-signed test certificate from `generate-test` is for testing or development only, so for production import the CA-issued certificate into a trust store and reference that store name in `trustStores`.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Sign Artifacts with Cosign and Notation.
Method: documentation only; no commands were run.
