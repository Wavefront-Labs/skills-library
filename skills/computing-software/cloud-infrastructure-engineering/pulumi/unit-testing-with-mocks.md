---
id: computing-software.cloud-infrastructure-engineering.pulumi.unit-testing-with-mocks
name: unit-testing-with-mocks
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-mocks, unit-testing, setmocks, mock-resources]
level: practitioner
status: docs-checked
description: "Unit test Pulumi programs without a cloud using runtime mocks (setMocks / set_mocks) with Mocha or Python unittest."
sources:
  - https://www.pulumi.com/docs/iac/concepts/testing/unit/
  - https://www.pulumi.com/docs/iac/concepts/testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit testing with mocks

Mocks answer your program from inside the same process instead of the Pulumi CLI. There are two handlers: `newResource` (each registered resource) and `call` (each provider function invoked, such as an AMI lookup).

```typescript
pulumi.runtime.setMocks({
    newResource: (args: pulumi.runtime.MockResourceArgs) => ({ id: args.name + "_id", state: args.inputs }),
    call: (args: pulumi.runtime.MockCallArgs) => {
        if (args.token === "aws:ec2/getAmi:getAmi") return { id: "ami-0eb1f3cdeeb8eed2a", architecture: "x86_64" };
        return args.inputs;
    },
}, "project", "stack", false);   // project name, stack name (both appear in mocked URNs), dryRun

describe("Infrastructure", function() {
    let infra: typeof import("../index");
    before(async function() {
        infra = await import("../index");   // import the program AFTER the mocks are defined
    });
    it("uses the looked-up AMI", function(done) {
        pulumi.all([infra.server.urn, infra.server.ami]).apply(([urn, ami]) =>
            ami !== "ami-0eb1f3cdeeb8eed2a" ? done(new Error(`Unexpected AMI ${ami} on ${urn}`)) : done());
    });
});
```

```python
class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + "_id", args.inputs]
    def call(self, args: pulumi.runtime.MockCallArgs):
        if args.token == "aws:ec2/getAmi:getAmi":
            return {"id": "ami-0eb1f3cdeeb8eed2a", "architecture": "x86_64"}
        return {}

class TestingWithMocks(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pulumi.runtime.set_mocks(MyMocks(), preview=False)
        program = runpy.run_path("__main__.py")   # run the program AFTER set_mocks
        self.server = program["server"]

    @pulumi.runtime.test
    def test_server_uses_looked_up_ami(self):
        def check(args):
            urn, ami = args
            self.assertEqual(ami, "ami-0eb1f3cdeeb8eed2a", f"unexpected AMI on server {urn}")
        return pulumi.Output.all(self.server.urn, self.server.ami).apply(check)
```
Run: `npx mocha --require tsx ec2tests.ts` (TypeScript; install `mocha @types/mocha tsx` as dev dependencies) or `python -m unittest`.

## Gotchas
- Python's runtime needs an asyncio event loop: subclass `unittest.IsolatedAsyncioTestCase`.
- Returned output property names from `new_resource` must be camelCase (`publicIp`), not snake_case.
- Mock provider functions (`aws.ec2.getAmi`) in `call` by token to pin a value and keep tests deterministic; mock `pulumi:pulumi:StackReference` resources in `newResource` to simulate another stack's outputs.
- A transform or hook does not run under mocks: return state that already reflects its effect.
- Mocks test your program logic, not whether the cloud accepts the inputs.

## Checked
2026-11-03. Confirmed against the Pulumi unit testing page (iac/concepts/testing/unit): the two handlers, `setMocks` positional arguments, import-after-mocks ordering, the `getAmi` token, the Python `set_mocks`/`@pulumi.runtime.test`/`IsolatedAsyncioTestCase` pattern, camelCase output names, the mocha/tsx and `python -m unittest` commands. Removed: Jest, pytest, `npm test`, `mocha -r ts-node/register`, the unconfirmed tags example and the "Verify" paragraph.
Method: documentation only; no commands were run.
