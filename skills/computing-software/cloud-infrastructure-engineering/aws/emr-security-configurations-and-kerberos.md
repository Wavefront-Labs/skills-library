---
id: computing-software.cloud-infrastructure-engineering.aws.emr-security-configurations-and-kerberos
name: emr-security-configurations-and-kerberos
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, emr, security-configuration, emr-kerberos, emr-encryption, runtime-roles, lake-formation]
level: practitioner
status: draft
description: "Secure Amazon EMR clusters with security configurations: at-rest and in-transit encryption, Kerberos with a cluster KDC or AD trust, runtime roles per step, and Lake Formation."
sources: ["Amazon EMR Management Guide - Use security configurations to set up cluster security", "Amazon EMR Management Guide - Use Kerberos authentication", "Amazon EMR Management Guide - Runtime roles for Amazon EMR steps"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EMR security configurations and Kerberos

A **security configuration** is a reusable JSON object referenced at cluster creation; it cannot
be changed on a running cluster.

## Encryption
```json
{"EncryptionConfiguration":{
  "EnableAtRestEncryption":true,"EnableInTransitEncryption":true,
  "AtRestEncryptionConfiguration":{
    "S3EncryptionConfiguration":{"EncryptionMode":"SSE-KMS","AwsKmsKey":"arn:aws:kms:...:key/..."},
    "LocalDiskEncryptionConfiguration":{"EncryptionKeyProviderType":"AwsKms","AwsKmsKey":"arn:aws:kms:...","EnableEbsEncryption":true}},
  "InTransitEncryptionConfiguration":{"TLSCertificateConfiguration":{
    "CertificateProviderType":"PEM","S3Object":"s3://emr-certs/certs.zip"}}}}
```
- In-transit uses certificates you supply (zip of PEM files, or a custom provider class); the
  certificate must cover the cluster's internal DNS names (wildcard for `*.ec2.internal` / `*.<region>.compute.internal`).
- The EC2 instance profile needs the KMS keys.

## Kerberos
```json
"AuthenticationConfiguration":{"KerberosConfiguration":{"Provider":"ClusterDedicatedKdc",
  "ClusterDedicatedKdcConfiguration":{"TicketLifetimeInHours":24,
    "CrossRealmTrustConfiguration":{"Realm":"CORP.EXAMPLE.COM","Domain":"corp.example.com",
      "AdminServer":"corp.example.com","KdcServer":"corp.example.com"}}}}
```
```bash
aws emr create-cluster ... --security-configuration secure-emr \
  --kerberos-attributes Realm=EC2.INTERNAL,KdcAdminPassword=...,CrossRealmTrustPrincipalPassword=...
```
- Options: cluster-dedicated KDC, external KDC, or cluster KDC with one-way cross-realm trust to Active Directory so AD users authenticate.
- Users need Linux accounts and principals; with AD trust, SSSD maps them.
- Kerberos is the entry ticket for Hadoop-native authz (Ranger plugins, HDFS permissions).

## Authorization
- **Runtime roles:** each step submitted with its own IAM role (`--execution-role-arn`) so jobs on a shared cluster access only their data; requires `"AuthorizationConfiguration":{"IAMConfiguration":{"EnableApplicationScopedIAMRole":true}}`.
- **Lake Formation** integration for table/column/row-level access from Spark and Hive.
- EMRFS role mappings (older) map users/groups to IAM roles for S3 access.

## Also
Block public access setting for EMR (account level) prevents clusters with SGs open to 0.0.0.0/0; IMDSv2 required via launch settings; private subnets.

## Verify
- [ ] `describe-cluster` shows the security configuration; local disks and S3 output encrypted.
- [ ] `kinit` as an AD user works; a step with a restricted runtime role cannot read other prefixes.
