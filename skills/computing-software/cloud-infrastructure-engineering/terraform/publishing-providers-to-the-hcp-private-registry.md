---
id: computing-software.cloud-infrastructure-engineering.terraform.publishing-providers-to-the-hcp-private-registry
name: publishing-providers-to-the-hcp-private-registry
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, private-provider-registry, hcp-terraform, provider-publishing, registry-api, gpg-signing, tfe-registry-provider]
level: advanced
status: docs-checked
description: "Publish an in-house provider to the HCP Terraform/TFE private registry via the API: GPG key, provider, version, SHA256SUMS and signature, and per-platform zip uploads."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/registry/publish-providers", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/provider-versions-platforms", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/gpg-keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private provider registry publishing

Private providers have no VCS publishing; everything goes through the API. Build the
release artifacts the same way as for the public registry (GoReleaser + GPG), then push
them with a script run from CI on each tag.

## 1. Inputs
From a GoReleaser release of `terraform-provider-widget` version `1.2.0`:
- `terraform-provider-widget_1.2.0_<os>_<arch>.zip` per platform
- `terraform-provider-widget_1.2.0_SHA256SUMS` and `..._SHA256SUMS.sig`
- The GPG key ID (16 hex chars) of the signing key.

## 2. One-time setup
```bash
H="Authorization: Bearer $TFE_TOKEN"; CT="Content-Type: application/vnd.api+json"
# register the public key (namespace = organization name)
curl -sH "$H" -H "$CT" -X POST https://app.terraform.io/api/registry/private/v2/gpg-keys \
  -d "$(jq -n --arg k "$(gpg --armor --export $KEY_ID)" \
        '{data:{type:"gpg-keys",attributes:{namespace:"acme","ascii-armor":$k}}}')"
# create the provider shell
curl -sH "$H" -H "$CT" -X POST https://app.terraform.io/api/v2/organizations/acme/registry-providers \
  -d '{"data":{"type":"registry-providers","attributes":{"name":"widget","namespace":"acme","registry-name":"private"}}}'
```
The `tfe` provider can own these two steps (`tfe_registry_gpg_key`,
`tfe_registry_provider`); versions are still pushed by the release script.

## 3. Per release
```bash
BASE=https://app.terraform.io/api/v2/organizations/acme/registry-providers/private/acme/widget
# create version; protocols: "4.0", "5.0" and/or "6.0", matching what the provider serves
V=$(curl -sH "$H" -H "$CT" -X POST $BASE/versions -d \
  "{\"data\":{\"type\":\"registry-provider-versions\",\"attributes\":{\"version\":\"1.2.0\",\"key-id\":\"$KEY_ID\",\"protocols\":[\"6.0\"]}}}")
curl -sT terraform-provider-widget_1.2.0_SHA256SUMS     "$(jq -r '.data.links."shasums-upload"' <<<"$V")"
curl -sT terraform-provider-widget_1.2.0_SHA256SUMS.sig "$(jq -r '.data.links."shasums-sig-upload"' <<<"$V")"
# one platform per zip
for z in terraform-provider-widget_1.2.0_*.zip; do
  os_arch=${z#terraform-provider-widget_1.2.0_}; os_arch=${os_arch%.zip}
  P=$(curl -sH "$H" -H "$CT" -X POST $BASE/versions/1.2.0/platforms -d \
    "{\"data\":{\"type\":\"registry-provider-version-platforms\",\"attributes\":{\"os\":\"${os_arch%_*}\",\"arch\":\"${os_arch#*_}\",\"shasum\":\"$(sha256sum $z|cut -d' ' -f1)\",\"filename\":\"$z\"}}}")
  curl -sT "$z" "$(jq -r '.data.links."provider-binary-upload"' <<<"$P")"
done
```
The version response carries `shasums-upload` and `shasums-sig-upload` links, and each platform response a
`provider-binary-upload` link; upload each file to its own link.

## 4. Consuming
```hcl
terraform {
  required_providers {
    widget = { source = "app.terraform.io/acme/widget", version = "~> 1.2" }
  }
}
```
Laptops and other CI authenticate with `terraform login` or a `TF_TOKEN_<hostname>` variable.

## Gotchas
- Set `protocols` to the provider API versions your build serves (allowed values 4.0, 5.0, 6.0;
  Terraform 0.13+ needs 5.0 or later).
- Every version needs the SHA256SUMS file, its `.sig`, and a public GPG key (RSA or DSA format)
  registered in the namespace; GPG signing is required for private providers.
- To remove a failed version, use the documented delete endpoint
  (`DELETE $BASE/versions/1.2.0`).

## Verify
- [ ] Registry UI lists the version with every expected os/arch.
- [ ] `terraform init` in a fresh directory installs the provider.

## Checked
2026-10-28. Confirmed against the HCP Terraform "Publish private providers" page and the private registry API pages for provider versions/platforms and GPG keys: endpoints and request types, `registry-name`, `namespace`, `key-id`, `ascii-armor`, `protocols` values, platform attributes `os`/`arch`/`shasum`/`filename`, upload link names, delete endpoint, RSA or DSA keys, GPG signing required, and the `tfe_registry_gpg_key` / `tfe_registry_provider` resources.
Corrected: "framework providers serve 6.0" (the docs only list the allowed values 4.0, 5.0, 6.0).
Removed: single-use/short-lived upload links, the handshake and signature error behaviours, "version shells cannot be overwritten", automatic authentication inside HCP Terraform, `terraform providers lock` and `h1:` hash advice (not in the fetched pages).
Method: documentation only; no commands were run.
