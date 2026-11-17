---
id: computing-software.ai-ml-engineering.mlops.sagemaker-pipelines-steps-and-conditions
name: sagemaker-pipelines-steps-and-conditions
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, pipeline-orchestration, sagemaker-pipelines, conditionstep, propertyfile, model-registration, aws]
level: practitioner
status: draft
description: "Build SageMaker Pipelines: processing/training/evaluation steps, parameters, PropertyFile + ConditionStep quality gates, model registration, step caching and runs."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html
  - https://sagemaker.readthedocs.io/en/stable/amazon_sagemaker_model_building_pipeline.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SageMaker Pipelines: steps and conditions

**Goal:** a reproducible train -> evaluate -> gate -> register pipeline that runs on schedule or on demand.

## Skeleton
```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.parameters import ParameterString, ParameterFloat
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CacheConfig
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.functions import JsonGet
from sagemaker.workflow.model_step import ModelStep
from sagemaker.workflow.fail_step import FailStep

sess = PipelineSession()                                 # makes job .run()/.fit() return step args, not start jobs
input_uri = ParameterString("InputData", default_value="s3://bucket/raw/")
min_auc = ParameterFloat("MinAuc", default_value=0.80)
cache = CacheConfig(enable_caching=True, expire_after="P30D")

prep = ProcessingStep("Preprocess", step_args=processor.run(code="prep.py", inputs=[...], outputs=[...]), cache_config=cache)
train = TrainingStep("Train", step_args=estimator.fit({"train": prep.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri}))
report = PropertyFile(name="EvalReport", output_name="evaluation", path="evaluation.json")
evaluate = ProcessingStep("Evaluate", step_args=eval_processor.run(code="evaluate.py", ...), property_files=[report])

register = ModelStep("Register", step_args=model.register(model_package_group_name="churn",
                     approval_status="PendingManualApproval", content_types=["text/csv"], response_types=["text/csv"]))
gate = ConditionStep("AucGate",
    conditions=[ConditionGreaterThanOrEqualTo(left=JsonGet(step_name=evaluate.name, property_file=report,
                json_path="metrics.auc.value"), right=min_auc)],
    if_steps=[register], else_steps=[FailStep("LowAuc", error_message="AUC below threshold")])

pipe = Pipeline(name="churn-train", parameters=[input_uri, min_auc], steps=[prep, train, evaluate, gate], sagemaker_session=sess)
pipe.upsert(role_arn=role)
execution = pipe.start(parameters={"MinAuc": 0.82})
```

## Key mechanics
- Data dependencies via step `.properties` (S3 URIs, model artifacts) build the DAG automatically; use `depends_on` only for ordering without data.
- `PropertyFile` + `JsonGet` lets a condition read a JSON file the evaluation step wrote - the evaluate script must write exactly that JSON path.
- Model registry approval status gates deployment: an EventBridge rule on approval change can trigger a deploy pipeline/CodePipeline.
- The `@step` decorator turns plain Python functions into pipeline steps for lighter workflows.

## Caching
Cached when step arguments are identical to a previous successful run within `expire_after`. Changing code files changes the arguments only if their S3 location/content hash changes - upload code to versioned paths. Don't cache steps whose output depends on "latest" external data.

## Gotchas
- Parameters are placeholders at definition time: you can't use their value in Python logic (`if min_auc > 0.8` fails); use conditions.
- Every step is a separate job with startup overhead (minutes); merge tiny steps.
- Debug a failing step by its job in the console/CloudWatch logs; `execution.list_steps()` shows failure reasons.

## Verify
- [ ] Pipeline runs end to end and a below-threshold run hits the FailStep.
- [ ] Registered model package carries evaluation metrics.
- [ ] Re-run with unchanged inputs reuses cached steps.
