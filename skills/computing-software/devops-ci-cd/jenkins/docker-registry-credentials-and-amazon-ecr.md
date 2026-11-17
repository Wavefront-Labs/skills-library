---
id: computing-software.devops-ci-cd.jenkins.docker-registry-credentials-and-amazon-ecr
name: docker-registry-credentials-and-amazon-ecr
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, amazon-ecr-plugin, docker-withregistry, docker-pipeline-plugin]
level: practitioner
status: docs-checked
description: "Push images from Jenkins to private registries and Amazon ECR with docker.withRegistry, the Amazon ECR plugin or aws ecr get-login-password, avoiding credential leaks."
sources: ["https://github.com/jenkinsci/docker-workflow-plugin/blob/master/docs/docker-workflow.md", "https://github.com/jenkinsci/amazon-ecr-plugin", "https://github.com/aws/aws-cli/blob/develop/awscli/examples/ecr/get-login-password.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry credentials and Amazon ECR

## Generic private registry
```groovy
docker.withRegistry('https://registry.example.com', 'registry-creds') {   // username/password credential
  def img = docker.build("team/app:${env.GIT_COMMIT}")
  img.push()
  img.push('latest')
}
```
`withRegistry(url, credentialsId)` selects the registry and uses a Username/Password credential for it (docker-workflow plugin docs).

## Amazon ECR with the plugin
Store an "AWS Credentials" entry (or rely on the agent's instance role), then:
```groovy
docker.withRegistry('https://123456789012.dkr.ecr.eu-west-1.amazonaws.com', 'ecr:eu-west-1:aws-creds-id') {
  docker.build('app').push(env.GIT_COMMIT)
}
```
The `ecr:<region>:<credentialsId>` form makes the Amazon ECR plugin convert the AWS credential into a Docker registry token (it is a Docker Token producer for the Docker Commons API). If you see authentication problems, the plugin README suggests removing the user Docker configuration files on the agent before running Docker commands.

## ECR without plugins (instance role / IRSA)
```groovy
sh '''
  aws ecr get-login-password --region eu-west-1 |
    docker login --username AWS --password-stdin 123456789012.dkr.ecr.eu-west-1.amazonaws.com
  docker push 123456789012.dkr.ecr.eu-west-1.amazonaws.com/app:$GIT_COMMIT
'''
```
Prefer IRSA/instance profiles over long-lived access keys on agents.

## Gotchas
- `docker login` stores credentials in the agent user's Docker config on shared agents, where
  other jobs can reuse them. Prefer `withRegistry` and clean up any config you create.
- ECR login tokens are time-limited; for long builds log in again before pushing (see the AWS
  ECR documentation for the current token lifetime).
- The target repository must exist in ECR unless your registry setup creates repositories on push.

## Verify
- [ ] The image appears in the registry and no Docker config with credentials is left in the agent home after the build.

## Checked
2026-10-25, Jenkins plugin READMEs and AWS CLI reference examples on GitHub. Confirmed: `docker.withRegistry(url, credentialsId)` usage and the `ecr:<region>:<credential-id>` prefix (docker-workflow and amazon-ecr plugin READMEs); the `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com` form (AWS CLI `ecr get-login-password` example). Removed the token-lifetime figure, the repository-creation note and the config-file location claims, which no current source read confirmed.
Method: documentation only; no commands were run.
