---
id: computing-software.cloud-infrastructure-engineering.azure.devsecops-advanced-security-dependency-and-secret-scanning
name: devsecops-advanced-security-dependency-and-secret-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, devsecops, defender-for-devops, ghas-azure-devops, github-advanced-security, advanced-security, dependency-scanning, secret-scanning, push-protection, code-scanning, codeql, sbom, sbom-tool, microsoft-security-devops, msdo, iac-scanning, container-image-scanning, trivy, checkov, template-analyzer, sarif, build-break, security-gates, supply-chain-security, slsa, provenance, dependency-scanning-task, dependency-alerts, devops-connectors, devops-security]
level: advanced
status: draft
description: "Shift security into Azure DevOps pipelines: GHAS for Azure DevOps (secret push protection, dependency scanning, CodeQL), MSDO IaC/container scans, SBOM, SARIF, build-break gates, Defender posture."
sources: ["Microsoft Learn - GitHub Advanced Security for Azure DevOps (secret, dependency, code scanning)", "Microsoft Learn - Microsoft Security DevOps Azure DevOps extension (MSDO) and supported tools", "Microsoft Learn - Microsoft Defender for Cloud DevOps security (Azure DevOps/GitHub connectors, posture)", "GitHub - microsoft/sbom-tool (SPDX SBOM generation)", "Microsoft Learn - Publish SARIF results and build-break configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DevSecOps in Azure DevOps — scans that run on every PR and gates that mean it

**Goal:** no secret lands in a repo, no vulnerable dependency ships unnoticed, IaC
and container images are scanned before deploy, an SBOM accompanies every release,
and findings surface as PR annotations and Defender for Cloud posture — with
build-break only where the team agreed.

## 1. Enable GitHub Advanced Security for Azure DevOps
Project settings → Repositories → (repo) → Settings → **Advanced Security** on (billed
per active committer; org-level default for new repos). Three capabilities:
- **Secret scanning**: repo history scan + **push protection** (blocks pushes containing known
  secret patterns — Azure keys, PATs, GitHub tokens, AWS, Slack…; bypass by `git push`
  with a reason or a repo setting). Alerts under *Repos > Advanced Security > Secrets*.
- **Dependency scanning**: task `AdvancedSecurity-Dependency-Scanning@1` after restore; reads the
  dependency graph (npm, NuGet, Maven, pip, Go, Cargo…) and raises vulnerability alerts with
  severity/fix version; dedupes across pipelines.
- **Code scanning (CodeQL)**: `AdvancedSecurity-Codeql-Init@1` (`languages: csharp, javascript`, `querysuite: security-extended`) → build → `AdvancedSecurity-Codeql-Analyze@1`; results as alerts with data-flow paths; `AdvancedSecurity-Publish@1` for third-party SARIF.
```yaml
steps:
  - task: AdvancedSecurity-Codeql-Init@1
    inputs: { languages: 'csharp', querysuite: 'security-extended' }
  - script: dotnet build -c Release
  - task: AdvancedSecurity-Dependency-Scanning@1
  - task: AdvancedSecurity-Codeql-Analyze@1
```
- There is no "Advanced Security" branch policy; gate with build validation plus a **status check** posted by the pipeline (fail the build on new critical alerts via the REST `alerts` API, or let the task fail on error severity), and triage in the *Alerts* blade with dismissal reasons.
- Prefer the **Build service** identity with *Advanced Security: View/Manage alerts* permissions; alerts are per repo, per branch (default branch is the source of truth).

## 2. Microsoft Security DevOps (MSDO) for IaC, containers and more
Extension *Microsoft Security DevOps* → task `MicrosoftSecurityDevOps@1` wrapping: **Template Analyzer** (ARM/Bicep), **Checkov**/**Terrascan** (Terraform, K8s, Dockerfile), **Trivy** (container images, filesystem), **ESLint** security, **Bandit** (Python), **BinSkim** (binaries), **Credscan**-style secret detection (now GHAS), **AntiMalware** (Windows agents).
```yaml
  - task: MicrosoftSecurityDevOps@1
    displayName: 'MSDO IaC + container scan'
    inputs:
      categories: 'IaC,containers'
      tools: 'templateanalyzer,checkov,trivy'
      break: true            # fail on errors (configure severity in gdn config)
      # config: .gdn/msdo.gdnconfig for per-tool options (e.g. Checkov skip-checks)
  - task: PublishBuildArtifacts@1
    inputs: { pathToPublish: $(Build.ArtifactStagingDirectory)/.gdn/msdo.sarif, artifactName: CodeAnalysisLogs }   # SARIF SAST Scans tab in the run
```
- Container images: scan the built image before `push` (`trivy image --exit-code 1 --severity CRITICAL,HIGH <image>`), then rely on Defender for Containers' registry scanning after push for continuous coverage (new CVEs on old images).
- IaC: Checkov/Template Analyzer on the PR build; PSRule for Azure (`PSRule.Rules.Azure`) is the Well-Architected-aligned alternative with Bicep/ARM support — one of them, not both.
- Results tab **Scans** (SARIF SAST Scans extension) shows findings per run; `break: true` turns errors into build failures — start with `false` + a dashboard, then break on *new* criticals once the baseline is clean.

## 3. SBOM and provenance
- `sbom-tool` (SPDX 2.2 JSON): `sbom-tool generate -b $(Build.ArtifactStagingDirectory) -bc $(Build.SourcesDirectory) -pn orders -pv $(Build.BuildNumber) -ps "Example Ltd" -nsb https://sbom.example.com` → `_manifest/spdx_2.2/manifest.spdx.json`; publish as a pipeline artifact and **attach to the container image** as an OCI referrer (`oras attach --artifact-type application/spdx+json`) or in the release.
- Syft/Grype for CycloneDX if a customer mandates it; feed SBOMs to Defender/Dependency-Track for continuous CVE matching against shipped versions.
- Provenance: sign images with Notation/cosign using a Key Vault key in the pipeline (keyless not supported for Notation; cosign keyless via OIDC works with Azure DevOps federated tokens); record `Build.BuildId`/commit in image labels; verify at admission (AKS skill) — the SLSA L2–L3 story.

## 4. Defender for Cloud DevOps security
Defender for Cloud → Environment settings → **Add environment → Azure DevOps** (OAuth authorisation by an org admin; or GitHub/GitLab connectors) → auto-discovers orgs/projects/repos; shows **DevOps posture**: repos without GHAS, pipelines with plaintext secrets, missing branch protection, IaC misconfig findings from MSDO runs (via the task's `Defender` publishing), secret findings, and an attack-path view linking a vulnerable repo → pipeline → service connection → production subscription. Recommendations become Secure Score items; findings route to Sentinel with the Defender connector. The connector needs *Project Collection Administrator* at setup and a service hook for continuous updates.

## 5. Pipeline integrity (the part scanners miss)
- Governed templates + required-template checks (pipelines/environments skills); pinned task versions (`@2` is a major; pin via template); no `curl | bash` installers — vendored or feed-hosted tools (Universal Packages).
- Agents: ephemeral per job (Managed DevOps Pools with *tear down after each job*, or container jobs) so a compromised build can't persist; no shared workspace between repos.
- Fork PRs: `pr.autoCancel`, *Build fork PRs with no secrets*, require a maintainer comment (`/AzurePipelines run`) for first-time contributors.
- Dependency sources: feed with upstreams only (artifacts skill); `npm ci` with lockfile; `dotnet` lock files (`RestorePackagesWithLockFile` + `--locked-mode`); pip hashes (`--require-hashes`).
- Audit stream to SIEM; alert on `Pipelines.PipelineModified` for prod pipelines, new service connections, policy bypasses.

## Gotchas
- Dependency scanning only sees what the build **restored** on that agent — scan the real build, not a separate "security" pipeline with a different restore.
- CodeQL for compiled languages must observe the build (`Init` → build → `Analyze`); a cached/incremental build with nothing compiled produces an empty database and a clean report.
- Push protection blocks patterns for *known* providers; generic high-entropy strings and custom tokens need custom patterns (preview) or a gitleaks rule in the PR build.
- MSDO `break: true` on Checkov with its default policy set fails on dozens of benign checks on day one; baseline with `skip-checks` in `.gdn` config per repo and widen gradually.
- Trivy's DB download on every run needs internet (or a mirrored DB via `TRIVY_DB_REPOSITORY` pointing at your ACR) — the first thing that breaks on firewalled agents.
- Advanced Security billing counts *unique committers in the last 90 days* across enabled repos; enabling on an archive of old repos costs money for nothing.
- Dismissing alerts without a reason in bulk silences the signal — require *Won't fix/False positive* with a comment and review monthly.

## Verify
- [ ] Pushing a commit with a fake-but-valid-looking Azure storage key is rejected by push protection; the repo's *Secrets* alerts list is empty on `main`.
- [ ] PR build shows dependency alerts for a deliberately pinned vulnerable package (e.g. an old `lodash`), with fix version; CodeQL finds a planted SQL-injection test case; both annotate the PR.
- [ ] MSDO run publishes SARIF to the *Scans* tab; a Bicep template with a public storage account fails the build with `break: true`; the SBOM artifact exists for the release and is attached to the image.
- [ ] Defender for Cloud DevOps security lists the Azure DevOps org with repos and no "Advanced Security disabled" recommendations for in-scope repos; findings appear in the Defender inventory within a day.
