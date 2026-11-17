---
id: computing-software.cloud-infrastructure-engineering.aws.acm-exportable-certificates-and-nitro-enclaves
name: acm-exportable-certificates-and-nitro-enclaves
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, acm, certificate-manager, exportable-certificates, certificate-export, export-certificate, nitro-enclaves-acm, nitro-enclaves, tls-on-ec2, nginx, private-key, certificate-renewal]
level: advanced
status: docs-checked
description: "ACM certificates on your own servers: export exportable public certificates, or use ACM for Nitro Enclaves so the private key stays in the enclave with NGINX or Apache."
sources: ["https://docs.aws.amazon.com/acm/latest/userguide/export-public-certificate.html", "https://docs.aws.amazon.com/acm/latest/userguide/acm-exportable-certificates.html", "https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave-refapp.html", "https://docs.aws.amazon.com/enclaves/latest/user/install-acm.html", "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateEnclaveCertificateIamRole.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACM certificates on EC2: exportable certificates and ACM for Nitro Enclaves

**Goal:** an EC2 instance, container or on-prem server terminates TLS with an ACM-issued
certificate, and you know which parts of renewal and deployment are yours.

## 1. Choose the path
| Need | Use |
|---|---|
| Public cert on your own server, container or on-prem host | **Exportable public certificate** (extra charge; see the ACM pricing page) |
| Key must stay isolated from the instance and its users; NGINX or Apache on EC2 (Linux) | **ACM for Nitro Enclaves** |

## 2. Exportable public certificate
Flow per the page: request an exportable certificate, validate the domain with DNS validation, export the
certificate, private key and chain, deploy them, and ACM manages renewals and notifies you.

```bash
aws acm request-certificate --domain-name api.example.com --validation-method DNS \
  --options Export=ENABLED
# after ISSUED; the passphrase file must not end in a line terminator
aws acm export-certificate --certificate-arn <CERT_ARN> \
  --passphrase fileb://path-to-passphrase-file \
  | jq -r '"\(.Certificate)\(.CertificateChain)\(.PrivateKey)"' > export.txt
```
- `Options.Export` takes `ENABLED` or `DISABLED` at request time. Per the export page, ACM public
  certificates created before 17 June 2025 cannot be exported.
- The output is PEM: certificate, chain, then an `ENCRYPTED PRIVATE KEY` protected by your passphrase.
  The console exports `.pem` files and asks for a passphrase for the private key.
- Per the exportable-certificates page: certificates have a 198-day validity period, ACM renews them 45
  days before expiry, and **you** manage deployment of exported certificates. ACM notifies you when a new
  certificate is ready (Amazon EventBridge); automate the re-export and server reload, and begin
  using the renewed certificate immediately.
- Protect exported private keys with secure storage and access controls, and use ACM's revocation feature
  if you suspect key compromise (`RevokeCertificate` exists in the ACM API).

## 3. ACM for Nitro Enclaves (key stays in an enclave)
Considerations per the user guide: RSA certificates only, Linux instances only, and some Regions are
unsupported (the page lists them; check it). Public and private certificates are supported.
1. Launch an enclave-enabled parent instance, e.g. `aws ec2 run-instances ... --enclave-options 'Enabled=true'`,
   either from the ACM for Nitro Enclaves AMI in AWS Marketplace or by installing the
   `aws-nitro-enclaves-acm` package from Amazon Linux Extras (the page shows `yum install aws-nitro-enclaves-acm`).
2. Create an IAM role that EC2 can assume (the page names it `acm-role`).
3. Associate the role with the certificate:
```bash
aws ec2 associate-enclave-certificate-iam-role --certificate-arn <CERT_ARN> --role-arn <ROLE_ARN>
# returns CertificateS3BucketName, CertificateS3ObjectKey, EncryptionKmsKeyId
```
   Up to 16 IAM roles can be associated with one certificate (API reference).
4. Give the role `s3:GetObject` on the returned bucket, `kms:Decrypt` on the returned KMS key, and
   `iam:GetRole` on itself; attach it to the instance through an instance profile.
5. Configure the web server (NGINX shown): rename `/etc/nitro_enclaves/acm.example.yaml` to `acm.yaml`
   and set `certificate_arn` in the `Acm` section; add `ssl_engine pkcs11;` to `/etc/nginx/nginx.conf`;
   remove the `ssl_certificate`, `ssl_certificate_key` and `ssl_ciphers` lines from the TLS server block;
   add `include "/etc/pki/nginx/nginx-acm.conf";`. For Apache the guide renames `acm-httpd.example.yaml`
   and edits `/etc/httpd/conf.d/httpd-acm.conf`.
6. `sudo systemctl start nitro-enclaves-acm.service` and `sudo systemctl enable nitro-enclaves-acm`.
7. Renewal: the service continuously polls ACM and updates the web server; `journalctl -u nitro-enclaves-acm.service`
   shows update announcements.

## Gotchas
- For private certificates the guide's test needs the hostname in `/etc/hosts` and `curl --cacert <chain.pem>`.
- Amazon Linux 2023 also needs the `pkcs11` engine entries in `/etc/pki/tls/openssl.cnf` (see the guide).

## Verify
- [ ] Public certificate: `curl https://<host_name_or_IP>` returns the NGINX or Apache index page (guide's test).
- [ ] `journalctl -u nitro-enclaves-acm.service` shows the service running and updating after a renewal.

## Checked
Date: 2026-11-07. Pages read in full: export-public-certificate (console and CLI sections), acm-exportable-certificates,
nitro-enclave-refapp (ACM for Nitro Enclaves overview, considerations), install-acm (steps 1-7 including NGINX
and Apache, read to the end), API_AssociateEnclaveCertificateIamRole. Botocore model checked for the
`Options.Export` enum and the RevokeCertificate operation. Not opened: the Java ExportCertificate sample page,
the Nitro region list was not copied.
Trimmed because no page states them: wildcard pricing, "private CA certs always exportable", the openssl
decrypt/modulus recipe, SSM Run Command renewal hook, passphrase special-character gotcha, vCPU/memory
allocator advice, the IAM action name and CloudTrail verify step. Replaced a dead source (export-certificate.html)
with export-public-certificate.html.
Method: documentation only; no commands were run.
