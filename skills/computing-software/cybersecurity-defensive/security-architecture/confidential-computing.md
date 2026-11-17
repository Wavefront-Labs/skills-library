---
id: computing-software.cybersecurity-defensive.security-architecture.confidential-computing
name: confidential-computing
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-protection, confidential-computing, tee, amd-sev-snp, intel-tdx, sgx, remote-attestation, data-in-use]
level: advanced
status: draft
description: "Protect data in use with confidential computing: TEEs (SEV-SNP, TDX, SGX, Nitro Enclaves), confidential VMs and containers, attestation-gated key release, and limits."
sources: ["https://confidentialcomputing.io/resources/white-papers-reports/", "https://learn.microsoft.com/en-us/azure/confidential-computing/overview", "https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Confidential computing

Encryption at rest and in transit leave data exposed in memory to the host OS, hypervisor and cloud
operator. Trusted execution environments (TEEs) encrypt memory with keys held by the CPU and prove
what code is running via attestation.

## Options
| Technology | Granularity | Notes |
|---|---|---|
| AMD SEV-SNP | Whole VM | Confidential VMs on Azure (DCasv5/ECasv5), GCP (N2D/C3D), AWS (some instance types) |
| Intel TDX | Whole VM | Azure DCesv5, GCP C3 confidential VMs |
| Intel SGX | Process enclave | Strong isolation, requires app partitioning (Gramine, Occlum, Open Enclave SDK) |
| AWS Nitro Enclaves | Isolated VM carved from an EC2 instance | No network/storage, vsock only; KMS attestation integration |
| Confidential containers | Pods in confidential VMs (Kata/CoCo, AKS confidential nodes) | |
| Confidential GPUs | NVIDIA H100 CC mode | AI workloads |

## Attestation is the point
The TEE produces a signed report (measurement of firmware, kernel, app). A relying party (key
service) verifies it before releasing secrets:
- Azure: Microsoft Azure Attestation + Key Vault Managed HSM "secure key release" policy.
- AWS: KMS key policy condition `kms:RecipientAttestation:ImageSha384` for Nitro Enclaves.
- GCP: Confidential Space with attestation-based workload identity.
Without attestation-gated key release you have memory encryption but no proof of what runs.

## Use cases
Multi-party analytics on shared data, processing regulated data in public cloud with operator-exclusion
requirements, key management and signing services, protecting AI model weights and prompts.

## Limits
- Side channels: TEEs have had many (Foreshadow, SGAxe, CacheOut); patch microcode, follow vendor
  TCB recovery, and treat TEEs as defence in depth.
- Guest OS inside a confidential VM is still yours to secure; a vulnerable app leaks data regardless.
- Performance overhead (a few % for SEV-SNP/TDX; more for SGX with paging).
- Debugging and monitoring are harder (no host-level introspection), which also blinds some security tools.

## Gotchas
- "Confidential VM" with platform-managed disk keys still trusts the provider's key management;
  use customer-managed keys bound to attestation for operator exclusion.
- Measurement changes on every image update; automate policy updates or key release breaks.

## Verify
Fetch and verify an attestation report from the workload (e.g. `snpguest`/Azure attestation client),
confirm measurements match the expected image, and that key release fails from a non-attested VM.
