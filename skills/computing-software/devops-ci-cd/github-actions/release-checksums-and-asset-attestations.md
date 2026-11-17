---
id: computing-software.devops-ci-cd.github-actions.release-checksums-and-asset-attestations
name: release-checksums-and-asset-attestations
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, checksums, sha256sums, asset-attestations, verify-download]
level: practitioner
status: gated
description: "Publish SHA256SUMS with release assets, sign or attest them, and give users copy-paste verification commands with sha256sum -c and gh attestation verify."
sources: ["https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds", "https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release checksums and asset attestations

Checksums prove integrity (download not corrupted / matches what was published); a signature or
attestation over them proves **who** built it.

## 1. Generate
```yaml
- name: Checksums
  working-directory: dist
  run: sha256sum *.tar.gz *.zip > SHA256SUMS      # relative names, run inside dist/
- uses: actions/attest-build-provenance@<version>   # v4+ is a wrapper on actions/attest; new workflows should use actions/attest
  with: { subject-path: 'dist/*.tar.gz, dist/*.zip' }   # input name (gated: unconfirmed, source is paywalled or blocked)
# job needs permissions: id-token: write and attestations: write
```
Run `sha256sum` inside the directory so the file lists bare names; users verify in their download folder.
macOS has no `sha256sum` by default: `shasum -a 256`.

## 2. Sign the checksum file (pick one)
The cosign sign-blob flags and gpg options below were not checked against their docs (gated: unconfirmed, source is paywalled or blocked); confirm them in the cosign and GnuPG manuals.
```bash
cosign sign-blob --yes --bundle SHA256SUMS.sigstore.json SHA256SUMS          # keyless, needs id-token: write
gpg --detach-sign --armor SHA256SUMS                                         # classic, key in secrets
```

## 3. Document verification for users
```bash
sha256sum --check --ignore-missing SHA256SUMS            # only checks files you downloaded
gh attestation verify tool_linux_amd64.tar.gz --repo my-org/tool
cosign verify-blob SHA256SUMS --bundle SHA256SUMS.sigstore.json \
  --certificate-identity-regexp 'https://github.com/my-org/tool/.github/workflows/release.yml@refs/tags/v.*' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
PowerShell: `(Get-FileHash .\tool.zip -Algorithm SHA256).Hash`.

## 4. Gotchas
The cosign docs read document `verify-blob --bundle` with `--certificate-identity` and `--certificate-oidc-issuer`; the regexp variant of the identity flag was not checked (gated: unconfirmed, source is paywalled or blocked).
- Generate checksums after the **final** artifact step (after compression, signing, notarisation) — any later mutation breaks them.
- `--ignore-missing` matters: without it users who download one file see failures for the rest.
- Windows line endings in SHA256SUMS break `sha256sum -c` — generate on Linux.
- Never publish MD5/SHA1 as the only digest.

## Verify
- [ ] Fresh download + `sha256sum -c --ignore-missing` prints `OK`.
- [ ] `gh attestation verify` succeeds for each asset.

## Checked

2026-11-02. Confirmed: gh attestation verify (--repo, --bundle, default OIDC issuer token.actions.githubusercontent.com) from the gh manual; cosign verify-blob with --bundle, --certificate-identity and --certificate-oidc-issuer from the Sigstore docs; id-token: write and attestations: write permissions from GitHub's attestation docs. Fixed: actions/attest-build-provenance@v2 is outdated (v4 is a wrapper on actions/attest and new work should use actions/attest). Gated: sign-blob and gpg flags, sha256sum --ignore-missing, --certificate-identity-regexp and the subject-path input name; not stated in the pages read.

Method: documentation only; no commands were run.
