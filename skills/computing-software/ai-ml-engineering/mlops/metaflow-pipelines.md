---
id: computing-software.ai-ml-engineering.mlops.metaflow-pipelines
name: metaflow-pipelines
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, metaflow, ml-pipelines, pipeline-orchestration, argo-workflows, step-functions, resume]
level: practitioner
status: docs-checked
description: "Build ML pipelines with Metaflow: FlowSpec steps and artifacts, branch and foreach fan-out, parameters, resume, and deployment to production schedulers."
sources:
  - https://docs.metaflow.org/metaflow/basics
  - https://docs.metaflow.org/production/introduction
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Metaflow pipelines

**Strength:** data scientists write plain Python; Metaflow follows the dataflow paradigm, persists the artifacts of every run, and can deploy flows to production workflow orchestrators.

## Flow structure
A flow is a directed graph of steps. Every flow needs a `start` step and an `end` step; a run starts at `start` and succeeds if `end` finishes successfully.
```python
from metaflow import FlowSpec, step

class LinearFlow(FlowSpec):
    @step
    def start(self):
        self.my_var = "hello world"      # assigning an instance variable creates a data artifact
        self.next(self.a)

    @step
    def a(self):
        print("the data artifact is: %s" % self.my_var)
        self.next(self.end)

    @step
    def end(self):
        print("still: %s" % self.my_var)

if __name__ == "__main__":
    LinearFlow()
```
```bash
python linear.py run
```
- Artifacts are persisted, so they can be analysed later with the Client API, visualised with Cards, used across flows, and help debugging and resuming past executions.
- Three transition types: linear, branch (`self.next(self.a, self.b)`) and foreach.
- Every branch must be joined: the join step takes an extra argument (for example `inputs`). Read a specific branch with `inputs.a.x`, or iterate over `inputs`. Branches can be nested, and each must be joined.
- Foreach branches over data at run time: it is initialised with the `foreach` keyword argument to `self.next`. Foreach loops must be joined like static branches.

## Parameters
Define parameters by assigning a `Parameter` object to a class variable; pass them on the command line, for example `python parameter_flow.py run --alpha ...`. Parameters are typed from the type of their default value, and `run --help` lists them.

## Resume
Failed runs can be resumed after fixing the bug (`python flow.py resume`), reusing earlier results instead of starting over; the basics page links to the debugging section for the details.

## Production
The production page describes deployments that run automatically without a human in the loop and reliably. Metaflow can schedule flows on production orchestrators, with the page naming Argo Workflows (suggested when running on Kubernetes), AWS Step Functions (minimal operational overhead), Airflow and Kubeflow (to stay compatible with existing deployments). It also supports event triggering, and `@project` is listed for isolating deployments. Results such as fresh predictions can be written to a data warehouse or cache, or models deployed.

## Checked
Method: docs-checked 2026-11-09 against the Metaflow "Creating Flows" and "Deploying to Production" pages (downloaded HTML, searched for the sections above). Dropped the foreach example, @resources, @retry, @card, --with kubernetes, @schedule/@trigger decorator syntax, @pypi/@conda, the Client API snippet, gotchas about pickling and datastore configuration, and the docs home source, none of which appear on the pages read.
