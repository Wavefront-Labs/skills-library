---
id: computing-software.cybersecurity-defensive.threat-modelling.cicd-pipeline-threat-modelling
name: cicd-pipeline-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, cicd-threat-modelling, owasp-top-10-cicd, poisoned-pipeline-execution, build-integrity, supply-chain-security]
level: advanced
status: docs-checked
description: "Threat model a CI/CD pipeline using the OWASP Top 10 CI/CD Security Risks and the recommendations each risk page gives."
sources: ["https://owasp.org/www-project-top-10-ci-cd-security-risks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD pipeline threat modelling

OWASP's Top 10 CI/CD Security Risks project says CI/CD systems deliver code from an engineer's
workstation to production and give attackers an efficient path to an organisation's crown
jewels. Use the ten risks as the checklist when walking the pipeline: source control, CI
systems and runners, package and artifact repositories, third-party services, CD and the
credentials joining them. For each, ask who or what can change it and with which identity.

## The ten risks and OWASP's recommendations
- **CICD-SEC-1 Insufficient flow control mechanisms:** no single human or programmatic entity
  should ship sensitive code or artifacts without external verification. Configure branch
  protection on production branches and avoid exclusions; keep accounts that can push
  unreviewed code from triggering deployment pipelines; limit auto-merge rules and review
  them so they cannot be bypassed; require approval before accounts trigger production
  pipelines; let artifacts flow only if created by a pre-approved CI service account; detect
  drift between production and its CI/CD origin.
- **CICD-SEC-2 Inadequate identity and access management:** continuously map all identities,
  the permissions granted and those actually used; remove unneeded permissions and stale
  accounts; prefer a central identity provider over local accounts; give external
  collaborators least privilege and expiring permissions; block non-organisation email
  domains; avoid self-registration, broad base permissions and shared accounts.
- **CICD-SEC-3 Dependency chain abuse:** pull packages through an internal proxy and, where
  possible, only from internal repositories of pre-vetted packages; enable checksum and
  signature verification; avoid "latest" in favour of pinned or ranged vetted versions;
  register private packages under the organisation's scope, reference them by scope and force
  scoped fetches to the internal registry; run package install scripts in a context without
  secrets.
- **CICD-SEC-4 Poisoned pipeline execution (PPE):** run pipelines that execute unreviewed code
  on isolated nodes without secrets; evaluate whether to run pipelines from forks and consider
  manual approval; for sensitive pipelines make sure each branch that triggers CI has a
  matching branch protection rule; review CI configuration files before the pipeline runs, or
  keep them in a separate protected remote branch; remove unneeded repository permissions; give
  each pipeline only the credentials it needs, with minimum privileges.
- **CICD-SEC-5 Insufficient pipeline-based access controls (PBAC):** do not share nodes between
  pipelines of different sensitivity; scope secrets per pipeline and step; return the
  execution node to a pristine state after each run; give the job's OS user least privilege;
  limit job permissions on the controller; patch execution nodes; segment the network and avoid
  unlimited internet access from build nodes.
- **CICD-SEC-6 Insufficient credential hygiene:** map credentials from code to deployment;
  least privilege and no sharing across contexts; prefer temporary over static credentials and
  rotate and detect stale static ones; restrict use to conditions such as source IP or
  identity; scan for secrets in IDE, on push and in history; stop secrets printing to build
  logs; make sure artifacts (container layers, binaries, Helm charts) contain no secrets.
- **CICD-SEC-7 Insecure system configuration:** inventory systems and versions with owners,
  check for known vulnerabilities and patch (or remove or restrict what cannot be patched);
  keep network access to least privilege; review configurations periodically.
- **CICD-SEC-8 Ungoverned usage of third-party services:** govern the whole lifecycle:
  approval before access, at least privilege; visibility of integration method (marketplace
  apps, plugins, OAuth apps, tokens), granted and actually used permissions; scoped context
  and strict ingress and egress filters for third parties in the build; periodic review and
  removal.
- **CICD-SEC-9 Improper artifact integrity validation:** sign resources as they are generated
  and validate them before consumption downstream. Options named: commit signing, artifact
  verification tools (in-toto, SLSA, Sigstore), configuration drift detection, and checking the
  hash of third-party scripts fetched in the pipeline against the provider's published hash.
- **CICD-SEC-10 Insufficient logging and visibility:** inventory every CI/CD system instance
  (especially self-managed ones such as Jenkins), enable the relevant audit and application
  logs (not on by default), ship them to a central location such as a SIEM, and alert on
  anomalies in each system and in the code shipping process across systems.

## Verify
- [ ] Each of the ten risks has an owner and a status for each pipeline stage.
- [ ] A test pull request from an untrusted source cannot reach secrets (judgement, a check of
  CICD-SEC-4 and 5).

## Checked
Confirmed 2026-11-09 against the OWASP Top 10 CI/CD Security Risks landing page and the Recommendations section of each of the ten risk pages (CICD-SEC-01 to 10), from local text copies.
Removed as unconfirmed: the platform-specific controls (GitHub `pull_request` versus `pull_request_target`, CODEOWNERS on pipeline files, OIDC to cloud, SHA-pinned actions, cosign), the "ephemeral runner" and cache poisoning gotchas, and the table's scenario column. The SLSA threats page (fetched but not used) and the CISA guidance (not read) were dropped from `sources`.
Method: docs-checked 2026-11-09 against owasp.org Top 10 CI/CD Security Risks and pages CICD-SEC-01 to CICD-SEC-10
