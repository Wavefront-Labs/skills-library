---
id: computing-software.cloud-infrastructure-engineering.aws.private-ca-short-lived-certificates-and-connectors
name: private-ca-short-lived-certificates-and-connectors
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, acm-pca, private-ca, short-lived-certificates, pca-connector, cert-manager]
level: advanced
status: docs-checked
description: "Run AWS Private CA in short-lived certificate mode and issue certs to Active Directory via Connector for AD and to Kubernetes via the aws-privateca-issuer."
sources: ["https://docs.aws.amazon.com/privateca/latest/userguide/short-lived-certificates.html", "https://docs.aws.amazon.com/privateca/latest/userguide/connector-for-ad.html", "https://docs.aws.amazon.com/privateca/latest/userguide/PcaKubernetes.html", "https://cert-manager.github.io/aws-privateca-issuer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private CA short-lived mode and connectors

## 1. Short-lived certificate mode
```bash
aws acm-pca create-certificate-authority --certificate-authority-type SUBORDINATE \
  --usage-mode SHORT_LIVED_CERTIFICATE --certificate-authority-configuration file://ca-config.json
aws acm-pca issue-certificate --certificate-authority-arn <CA_ARN> --csr fileb://svc.csr \
  --signing-algorithm SHA256WITHRSA --validity Value=1,Type=DAYS
```
- A short-lived-mode CA issues only certificates with a maximum validity of seven days. Set the `UsageMode` parameter
  (CLI `--usage-mode`) when you create the CA. The default is general-purpose mode (any validity period).
- Such certificates expire so quickly that they can be deployed without a revocation mechanism.
- A short-lived-mode CA must be the last CA in the hierarchy, and the private CA itself must be renewed every seven
  days, which the AWS page calls significant overhead.
- It costs less than a general-purpose CA (see the AWS Private CA pricing page for figures).
- AWS Certificate Manager cannot issue certificates signed by a short-lived-mode private CA. The page names Amazon
  AppStream and Amazon WorkSpaces as supported users of short-lived certificates.

## 2. Connector for Active Directory
Replaces on-premises enterprise or third-party CAs with a managed private CA, providing certificate enrollment to
users, groups and machines managed by your AD. It works with AWS Managed Microsoft AD and integrates with AWS Managed
Microsoft AD Connector for on-premises AD.
- Reached through the console, AWS CLI and APIs; no additional cost beyond the CAs and certificates you issue.
- Follow the AWS guide sections "Set up Connector for AD" and "Get started" for the template and enrollment steps;
  this skill does not restate them.
```bash
aws pca-connector-ad create-connector --directory-id d-1234567890 --certificate-authority-arn <CA_ARN> \
  --vpc-information SecurityGroupIds=sg-0abc
```

## 3. Kubernetes (cert-manager + aws-privateca-issuer)
The open source `aws-privateca-issuer` plugin for cert-manager requests certificates, distributes them to Kubernetes
secrets and automates renewal. It works with Amazon EKS, self-managed clusters on AWS and on-premises clusters, on x86
and ARM. On EKS, AWS recommends the cert-manager and `aws-privateca-connector-for-kubernetes` add-ons instead.
Install cert-manager first, then:
```bash
helm repo add awspca https://cert-manager.github.io/aws-privateca-issuer
helm install awspca/aws-privateca-issuer --generate-name
```
```yaml
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata: {name: pca}
spec: {arn: <CA_ARN>, region: <REGION>}
```
- Minimal IAM policy on the CA ARN: `acm-pca:DescribeCertificateAuthority`, `acm-pca:GetCertificate`,
  `acm-pca:IssueCertificate`. Credentials can come from IRSA, an EC2 instance role, Kubernetes secrets, KIAM v4.0 or
  IAM Roles Anywhere.
- From v1.12.0 an `AWSPCAIssuer` (namespaced) no longer uses the controller pod's own credentials (IRSA, Pod Identity,
  instance profile) unless the chart value `enableIssuerAmbientCredentials: true` is set; otherwise give each issuer
  a `secretRef` or `serviceAccountRef`. `AWSPCAClusterIssuer` ambient credentials default to allowed.
- AWS Private CA backdates NotBefore by 1 hour by default. For short-lived certificates set `spec.notBeforeOffset`
  (whole seconds, minutes or hours, not negative, at most 24 hours); from v1.10.0 the issuer backdates 15 minutes
  when it is unset.
- Use the `cert-manager.io/issuer` annotation on Ingress, not `cert-manager.io/cluster-issuer`, to point at an
  `AWSPCAClusterIssuer`.
- Helm does not upgrade CRDs: apply the chart's `crds/` directory before upgrading.

## Troubleshooting (from the issuer README)
- Secret credentials `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` must be base64 encoded.
- A CertificateRequest with no events usually means an old cert-manager without the approval check; the issuer's
  `-disable-approved-check` flag turns the check off (cert-manager before v1.3).

## Checked
2026-11-08. Confirmed against the AWS Private CA pages (CA modes, Connector for AD, Kubernetes) and the
aws-privateca-issuer README; CLI commands and flags checked against the botocore model. Removed: claims that the
usage mode cannot be changed, that clients must rotate automatically, the GPO autoenrollment steps, the certutil
check, the helm namespace flags, and the `kubectl get certificate` check, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
