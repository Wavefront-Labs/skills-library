---
id: computing-software.cloud-infrastructure-engineering.google-cloud.artifact-analysis-notes-and-occurrences
name: artifact-analysis-notes-and-occurrences
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, software-supply-chain, notes-occurrences, artifact-analysis-api, grafeas, vulnerability-scanning]
level: advanced
status: docs-checked
description: "Work with the Artifact Analysis (Grafeas) API: notes vs occurrences, listing vulnerability, provenance, SBOM and attestation occurrences for an image digest, plus Pub/Sub."
sources: ["https://docs.cloud.google.com/artifact-analysis/docs/investigate-vulnerabilities", "https://docs.cloud.google.com/artifact-analysis/docs/pub-sub-notifications", "https://docs.cloud.google.com/artifact-analysis/docs/reference/rest", "https://containeranalysis.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Artifact Analysis notes and occurrences

- **Note**: a definition (a CVE, a build type, an attestor authority). Owned by a provider project (Google's `goog-vulnz` for CVEs, or yours).
- **Occurrence**: an instance of a note on a specific resource URI (an image digest).
Kinds: `VULNERABILITY`, `BUILD` (provenance), `DISCOVERY` (scan status), `ATTESTATION`, `SBOM_REFERENCE`, `PACKAGE`, `DEPLOYMENT`.

## 1. Query occurrences for an image
```bash
gcloud artifacts docker images describe <AR>/app@sha256:<D> --show-all-metadata --format=json
gcloud artifacts docker images list-vulnerabilities <AR>/app@sha256:<D> \
  --format='table(vulnerability.effectiveSeverity,vulnerability.shortDescription,vulnerability.packageIssue[0].affectedPackage)'
# raw API
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://containeranalysis.googleapis.com/v1/projects/<P>/occurrences?filter=resourceUrl%3D%22https%3A%2F%2F<AR>%2Fapp%40sha256%3A<D>%22%20AND%20kind%3D%22VULNERABILITY%22"
```

## 2. Create your own note/occurrence
```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  "https://containeranalysis.googleapis.com/v1/projects/<P>/notes?noteId=qa-passed" \
  -d '{"attestation": {"hint": {"humanReadableName": "QA passed"}}}'
```
Binary Authorization attestations are ATTESTATION occurrences on such notes.

## 3. React to new findings
Topics `container-analysis-notes-v1` and `container-analysis-occurrences-v1` (auto-created when the API is
enabled) publish changes; subscribe and filter for `kind=VULNERABILITY` with severity CRITICAL to open tickets.

## Gotchas
- Filters use the full resource URL with `https://` prefix and the digest, not the tag.
- Automatic scanning metadata has a 30-day continuous analysis window; push the image to Artifact Registry again to rescan (scan status is in the DISCOVERY occurrence).
- IAM: listing occurrences needs the Container Analysis Occurrences Viewer role (`roles/containeranalysis.occurrences.viewer`) on the project. Check the Container Analysis IAM docs for the roles that let someone create notes and occurrences.

## Verify
- [ ] DISCOVERY occurrence shows `analysisStatus: FINISHED_SUCCESS`; vulnerability list matches the console; a test Pub/Sub subscription receives occurrence messages.

## Checked
2026-10-31. Confirmed in the Artifact Analysis "Investigate vulnerabilities" and Pub/Sub notifications pages and the Container Analysis v1 discovery document: occurrence `kind` values, `goog-vulnz` notes, filter form with `https://` and digest, `humanReadableName` on an attestation hint, `FINISHED_SUCCESS`, the two auto-created topics, the 30-day analysis window and rescan by push, the occurrences viewer role, and the gcloud commands and flags (via check_commands). Removed: the `notes.attacher` role name (not on the pages read) and the "not pulled in 30 days" reading of the window.
Method: documentation only; no commands were run.
