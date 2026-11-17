---
id: computing-software.cloud-infrastructure-engineering.aws.aws-transform-for-dotnet-vmware-and-mainframe
name: aws-transform-for-dotnet-vmware-and-mainframe
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, aws-transform-jobs, vmware-migration, mainframe-modernization, dotnet-modernization, aws-transform]
level: practitioner
status: draft
description: "AWS Transform jobs: .NET Framework to cross-platform .NET, VMware discovery and network conversion feeding MGN, and mainframe code analysis and refactoring."
sources: ["AWS Transform User Guide - What is AWS Transform", "AWS Transform User Guide - Transformation jobs for .NET, VMware and mainframe", "AWS Mainframe Modernization User Guide - Overview", "AWS Application Migration Service User Guide - VMware migrations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AWS Transform for .NET, VMware and mainframe

**What it is:** an agent-driven service (launched 2025) that runs transformation **jobs** in a
web experience: humans approve plans and checkpoints, agents analyse and change code or plan migrations.

## Common setup
- Enable AWS Transform, connect users via IAM Identity Center, create a **workspace**.
- Add connectors: source repositories (GitHub, GitLab, Bitbucket, CodeCommit) for code jobs; an AWS
  account for target resources; for VMware, discovery data (export from RVTools or the discovery collector).
- Jobs have plans, worklogs and human-in-the-loop approval steps; outputs are branches/PRs, reports or migration artifacts.

## .NET
- Ports .NET Framework (Windows-only) applications to cross-platform .NET (Linux-capable) at
  repository scale: dependency analysis, code changes, unit test runs, a transformation summary.
- Result lands as a new branch; review like any PR. Remaining manual work: Windows-specific APIs (WCF server side, System.Web pieces, COM interop), third-party packages without .NET support.
- Benefit: Linux containers/Graviton instead of Windows licences.

## VMware
- Inputs inventory, then: application discovery and dependency grouping, **wave planning**,
  **network conversion** (NSX/vSphere networks to VPCs, subnets, security groups as IaC), and
  orchestration of server rehost via **Application Migration Service (MGN)**.
- Review generated network designs (CIDRs, segmentation) with your network team before deploying.

## Mainframe
- Analyses COBOL/JCL/CICS/DB2 codebases: inventory, dependency graphs, documentation generation,
  decomposition into domains, and refactoring to Java with AWS Blu Age-style patterns; test planning for equivalence.
- Run with **AWS Mainframe Modernization** offerings for the target runtime; check current service
  options, as the mainframe runtime choices have changed over time.

## Working practice
- Pilot on one representative application; measure how much manual work remains.
- Keep humans on approvals: plans, code reviews, network designs.
- Treat outputs like contractor work: tests, security scans, performance tests before production.

## Verify
- [ ] Pilot job completed with a written assessment of manual effort remaining.
- [ ] Generated code passes the existing test suite plus new equivalence tests.
