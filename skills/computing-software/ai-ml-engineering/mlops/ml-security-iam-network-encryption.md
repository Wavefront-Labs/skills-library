---
id: computing-software.ai-ml-engineering.mlops.ml-security-iam-network-encryption
name: ml-security-iam-network-encryption
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-governance, ml-security, least-privilege-iam, network-isolation, vpc-endpoints, kms-encryption, model-supply-chain]
level: practitioner
status: draft
description: "Secure ML workloads: least-privilege roles, network isolation and private endpoints, KMS encryption, secrets, artifact integrity and endpoint abuse controls."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/security.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/mkt-algo-model-internet-free.html
  - https://cloud.google.com/vertex-ai/docs/general/vpc-service-controls
  - https://atlas.mitre.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML security: IAM, network and encryption

**Goal:** training data, models and endpoints are protected like any production system, plus ML-specific risks (pickled models, data poisoning, model extraction).

## Identity
- One role per workload type (training job, pipeline, endpoint), scoped to specific S3/GCS prefixes, registries and KMS keys. Avoid `AmazonSageMakerFullAccess`-style managed policies in production.
- Separate dev and prod accounts/projects; promotion via CI identity only.
- Humans get read access to prod artifacts by exception.

## Network
- Training/processing jobs in private subnets with no internet egress; reach AWS/GCP services through VPC endpoints / Private Service Connect (S3, ECR/Artifact Registry, SageMaker/Vertex APIs, CloudWatch, STS).
- SageMaker `enable_network_isolation=True` blocks all network access from the training container (data comes via channels) - good for third-party algorithms.
- Vertex AI: VPC Service Controls perimeters to stop data exfiltration across project boundaries.
- Endpoints: private (VPC-only) unless they must be public; put public ones behind an API gateway with authn, quotas and WAF.

## Encryption
- At rest: customer-managed KMS keys for buckets, training volumes (`volume_kms_key`), outputs (`output_kms_key`), endpoint storage, notebooks.
- In transit: TLS everywhere; enable inter-container traffic encryption for distributed training where offered.

## Secrets
From a secrets manager at runtime (Secrets Manager, Secret Manager, Vault) via the job role; never in hyperparameters, environment variables in logged configs, notebooks, or images.

## ML-specific risks
- **Model artifacts:** pickle/joblib/`torch.load(weights_only=False)` execute code - load only trusted, integrity-checked artifacts (hash or signature verified at deploy time); prefer safetensors/ONNX/skops for exchange.
- **Supply chain:** pin and scan base images and Python dependencies; mirror packages internally.
- **Data poisoning:** validate and track provenance of training data, especially user-generated or scraped data.
- **Model extraction / abuse:** rate-limit and monitor endpoint query patterns; return only needed outputs (labels vs full probability vectors) for sensitive models.
MITRE ATLAS catalogues these adversary techniques for threat modelling.

## Verify
- [ ] Training role cannot read other teams' buckets (test with a denied access attempt).
- [ ] Jobs run without internet egress and still succeed via endpoints.
- [ ] Deploy step verifies artifact hash/signature before loading.
