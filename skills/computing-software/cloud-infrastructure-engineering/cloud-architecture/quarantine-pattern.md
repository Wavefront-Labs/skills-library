---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.quarantine-pattern
name: quarantine-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, quarantine-pattern, supply-chain-security, artifact-validation, malware-scanning, data-ingestion]
level: practitioner
status: docs-checked
description: "Quarantine third-party artifacts before use: segmented untrusted store, validation checks, promotion only on pass with a report, re-scanning, and managed upload malware scanning."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/quarantine", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-storage-malware-scan", "https://docs.aws.amazon.com/guardduty/latest/ug/gdu-malware-protection-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarantine

Per the Azure Architecture Center, treat all external artifacts (open-source binaries, public container images, vendor OS images, packages, external IaC modules) as untrusted. A quarantine process moves an artifact from untrusted to trusted through checkpoints, without changing its composition. Consumers block use of the artifact until it passes.

## Workflow
1. The consumer signals intent, names the source and blocks use of the artifact. Signalling should be automated (for example on ingestion into the developer environment, a repository commit or an image added to a private registry).
2. The process validates the origin of the request and fetches the artifact from the named store into a **quarantine store**.
3. Custom verification runs: input constraints, attributes, source and type against standards; vulnerability scanning, malware detection and other checks. Checks depend on artifact type (an OS image differs from a NuGet package). Azure's example also runs SBOM evaluation and image signing checks.
4. On success, publish to a trusted store with clear annotations and a report of the checks and their criticality, with an expiry after which the report is invalid and the artifact is considered unsafe. On failure the artifact stays unavailable (in the example it is deleted from quarantine).
5. End by signalling an event with state and report; what consumers then do is outside the pattern.

## Design points from the page
- Choose sources that meet organisation-approved standards; check vendors' responsible disclosure plans.
- Segment trusted and untrusted stores with identity and network controls. In the example, Azure Policy for Kubernetes limits container pulls to the trusted registry, and alerts flag imports from unexpected sources.
- Automate ingestion and publishing; validation can take a long time, so the automation must run to completion.
- Quarantine is a first-opportunity check. Passing does not make an artifact trustworthy forever: continue scanning and pipeline validation. Defender for Containers continuously scans registries in the Azure example.
- Agree validation rules per artifact type; inconsistent rules per ingestion weaken the process. Centralise if many teams run variants.
- Alternative: a push model where the orchestrator decides, or a pull model where the workload team reviews published results and pulls from quarantine (more practical for teams with different risk tolerances).
- Not worthwhile for artifacts from your own team or a trusted partner, or where the risk costs less than the process.
- Keep an audit trail of requester, lineage and validation results.

## Managed upload scanning
- **Defender for Storage** (Azure): on-upload scanning of blobs when uploaded or modified, and on-demand scanning of existing blobs. It uses Microsoft Defender Antivirus, scans all file types including archives up to 50 GB per blob, writes results as blob index tags and Defender for Cloud alerts, and can soft-delete malicious blobs. Scan time varies with size, type and load, so applications depending on results must tolerate delay.
- **GuardDuty Malware Protection for S3** (AWS): scans new objects and new versions in a selected bucket in your own account and Region. Results go to EventBridge and a CloudWatch namespace by default; optional tagging records the result on the object. Used independently of GuardDuty there is no detector ID, so no GuardDuty finding is created.
- Use scan results (tags or events) to drive promotion and make the pipeline idempotent.

## Verify
- [ ] No workload identity can read the quarantine store.
- [ ] Consumption is enforced from the trusted store only (policy, not convention).
- [ ] A known-bad test artifact is rejected end to end and the report expiry is honoured.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Quarantine pattern (last updated 2026-11-07); Defender for Storage, Introduction to malware scanning; AWS GuardDuty User Guide, Malware Protection for S3 (overview page).
Removed as unconfirmed: ClamAV in a sandboxed function, cosign and SLSA provenance specifics (the SLSA source was a landing page), Kyverno/Gatekeeper admission examples, scanner archive-depth limits for GuardDuty, presigned-URL bypass and EICAR test claims.
Method: documentation only; no commands were run.
