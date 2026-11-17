---
id: computing-software.ai-ml-engineering.mlflow.pyfunc-type-hints-and-responsesagent
name: pyfunc-type-hints-and-responsesagent
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, pyfunc-type-hints, responsesagent, pythonmodel, model-signature, genai-agents, chatagent]
level: practitioner
status: docs-checked
description: "Define pyfunc models with type-hint signatures (pydantic/list inputs) and package agents with ResponsesAgent: predict/predict_stream, logging and serving-compatible schemas."
sources:
  - https://mlflow.org/docs/latest/ml/model/python_model/
  - https://mlflow.org/docs/latest/genai/flavors/responses-agent-intro/
  - https://mlflow.org/docs/latest/ml/model/signatures/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Type-hint pyfunc signatures and ResponsesAgent

## Type hints instead of hand-written signatures (MLflow 2.20+)
```python
import mlflow, pydantic
class Query(pydantic.BaseModel):
    text: str
    top_k: int = 5

class Retriever(mlflow.pyfunc.PythonModel):
    def predict(self, model_input: list[Query], params=None) -> list[list[str]]:
        return [search(q.text, q.top_k) for q in model_input]

with mlflow.start_run():
    mlflow.pyfunc.log_model(name="retriever", python_model=Retriever(),
                            input_example=[{"text": "refund policy", "top_k": 3}])
```
- The signature is inferred from the annotations and inputs are validated against the hints.
- The input hint must be `list[...]` because `predict` receives batches. Supported element types include `str`, `int`, `float`, `bool`, `bytes`, `datetime.datetime`, nested lists, `dict[str, ...]`, unions and pydantic models (whose fields must be supported types). `Optional[...]` cannot be the direct element of `list[...]`, and optional pydantic fields need a default.
- Pass an `input_example` when logging, as the docs example does.

## ResponsesAgent for agents
Wraps an agent with an OpenAI Responses-compatible interface, so it can be served, traced and evaluated uniformly:
```python
from mlflow.pyfunc import ResponsesAgent
from mlflow.types.responses import ResponsesAgentRequest, ResponsesAgentResponse

class SupportAgent(ResponsesAgent):
    def predict(self, request: ResponsesAgentRequest) -> ResponsesAgentResponse:
        msgs = [m.model_dump() for m in request.input]
        text = run_my_agent(msgs)                    # LangGraph, raw SDK calls, etc.
        return ResponsesAgentResponse(output=[self.create_text_output_item(text=text, id="msg_1")])
    def predict_stream(self, request):
        ...                                          # yield ResponsesAgentStreamEvent deltas

mlflow.models.set_model(SupportAgent())             # models-from-code pattern
```
Log with `mlflow.pyfunc.log_model(name="agent", python_model="agent.py")` (models from code). MLflow infers a signature from the `ResponsesAgentRequest`/`ResponsesAgentResponse` schemas, adds `{"task": "agent/v1/responses"}` to the metadata and uses a default input example if you give none. The older `ChatModel` and `ChatAgent` interfaces still exist; the docs recommend `ResponsesAgent` instead.

## Verify
- [ ] `mlflow.models.predict(model_uri, input_data=..., env_manager="uv")` succeeds in a clean environment.
- [ ] Traces appear for agent calls when autologging is enabled.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Type-hint signatures from MLflow 2.20.0, `list[...]` requirement, supported element types, Optional and pydantic default rules: docs/classic-ml/model/python_model.mdx.
- `ResponsesAgent`, `ResponsesAgentRequest`/`ResponsesAgentResponse`, `create_text_output_item`, `ResponsesAgentStreamEvent`, `request.input` items with `model_dump()`, `set_model`, models-from-code logging with automatic signature, `agent/v1/responses` task metadata and recommendation over `ChatModel`/`ChatAgent`: docs/genai/flavors/responses-agent-intro.mdx.
- `mlflow.models.predict(..., env_manager=...)` with virtualenv (default), uv, conda, local: docs/classic-ml/model/index.mdx.
- Removed as unconfirmed: `resources=[...]` in the logging call, the guarantee that logging fails early on a bad input example, and the dict-to-pydantic conversion statement.

Method: documentation only; no commands were run.
