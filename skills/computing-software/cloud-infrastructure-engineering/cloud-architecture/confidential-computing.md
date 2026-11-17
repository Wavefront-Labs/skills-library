---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.confidential-computing
name: confidential-computing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, confidential-computing, tee, sev-snp, tdx, nitro-enclaves, attestation]
level: practitioner
status: draft
description: "Decide when and how to use confidential computing: TEE options (SEV-SNP, TDX, Nitro Enclaves, confidential GPUs), attestation, key release and performance trade-offs."
sources: ["https://confidentialcomputing.io/", "https://learn.microsoft.com/azure/confidential-computing/overview", "https://cloud.google.com/confidential-computing/docs", "https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Confidential computing

## When
Protecting data in use from the cloud operator, other tenants or privileged insiders: multi-party
analytics, regulated data processing, key management, AI inference on sensitive data. Encryption
at rest and in transit does not cover data in memory.

## Steps
1. **Pick the TEE granularity**:
   - Confidential VMs (AMD SEV-SNP, Intel TDX): lift-and-shift, whole VM memory encrypted;
     available on Azure, Google Cloud and AWS (SEV-SNP on selected instance types).
   - Enclaves (AWS Nitro Enclaves, Intel SGX): small isolated process, no network/storage,
     strongest isolation, needs app refactoring.
   - Confidential containers/Kubernetes nodes and confidential GPUs (NVIDIA H100 CC mode) for
     AI workloads.
2. **Attestation is the point**: the workload proves its measurement (image hash, firmware)
   to a verifier (Azure Attestation, Google Confidential Space, Nitro attestation documents
   with KMS condition keys) before keys are released.
3. **Secure key release**: KMS policy grants decrypt only to attested measurements.
4. **Measure performance**: typically single-digit percent overhead for CPU TEEs; more for
   I/O-heavy and enclave transitions.
5. **Threat model honestly**: side channels and the TCB you trust (CPU vendor, firmware).

## Gotchas
- Confidential VMs without attestation-gated keys give little beyond memory encryption.
- Debug-mode enclaves have different measurements; never release prod keys to them.

## Verify
- [ ] Keys released only after successful attestation.
- [ ] Performance benchmarked against non-confidential baseline.
