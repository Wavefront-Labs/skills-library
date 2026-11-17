---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-aws-lambda-credentials-and-payload
name: argo-events-trigger-aws-lambda-credentials-and-payload
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, aws-lambda, accesskey, secretkey, payload, policy, region, functionname]
level: practitioner
status: docs-checked
description: "Invoke AWS Lambda from non-AWS event sources with the awsLambda trigger, using Secrets for keys, a payload mapping and a status policy."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/aws-lambda.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger aws lambda credentials and payload

The AWS Lambda trigger lets any EventSource invoke a function, since native event-driven invocation covers only SNS, SQS and a few others.

Create a Secret with base64-encoded `accesskey` and `secretkey` (`aws-secret`), make sure the account may execute Lambda, then:

```yaml
awsLambda:
  functionName: hello
  accessKey:
    name: aws-secret
    key: accesskey
  secretKey:
    name: aws-secret
    key: secretkey
  namespace: argo-events
  region: us-east-1
  payload:
    - src:
        dependencyName: test-dep
        dataKey: body.name
      dest: name
```

POSTing `{"name":"foo"}` to the webhook EventSource invokes `hello` with `{"name": "foo"}`; verify in CloudWatch logs. `payload` lists `src` and `dest` pairs and you can add as many as needed.

Parameterization can replace fields such as the function name from event data:

```yaml
parameters:
  - src:
      dependencyName: test-dep
      dataKey: body.function_name
    dest: functionName
```

Policy: `policy.status.allow: [200, 201]` treats the invocation as successful only for those statuses.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/aws-lambda.md. Confirmed: Secret keys accesskey/secretkey, awsLambda fields, payload src/dest, parameters example, policy.status.allow. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
