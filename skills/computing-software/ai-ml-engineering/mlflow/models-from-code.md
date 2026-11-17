---
id: computing-software.ai-ml-engineering.mlflow.models-from-code
name: models-from-code
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, models-from-code, mlflow-models, pyfunc, set-model, langchain, genai]
level: practitioner
status: gated
description: "Log MLflow models as Python source instead of pickles: set_model, python_model as a file path, model_config, and loading behaviour for GenAI chains and agents."
sources:
  - https://mlflow.org/docs/latest/ml/model/models-from-code/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.models.html#mlflow.models.set_model
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html#mlflow.pyfunc.log_model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLflow Models from Code

**Goal:** log a model whose definition is a Python file, so nothing has to be pickled - essential for LangChain/LlamaIndex chains, agents, and any object holding clients or locks that `cloudpickle` cannot serialise.

## Write the model file
`agent_model.py`:
```python
import mlflow
from mlflow.pyfunc import PythonModel

cfg = mlflow.models.ModelConfig(development_config="config.yaml")   # module level, not in load_context

class Agent(PythonModel):
    def predict(self, context, model_input, params=None):
        return [f"{cfg.get('llm_model')}:{q}" for q in model_input["question"]]

mlflow.models.set_model(Agent())   # required: tells MLflow which object is the model
```

## Log it
```python
with mlflow.start_run():
    info = mlflow.pyfunc.log_model(
        name="agent",                       # MLflow 3; `artifact_path=` still works but warns it is deprecated (tested on 3.17.1)
        python_model="agent_model.py",      # a path, not an instance
        model_config="config.yaml",         # or a dict
        input_example={"question": ["What is MLflow?"]},
        pip_requirements=["mlflow", "openai"],
    )
loaded = mlflow.pyfunc.load_model(info.model_uri)
loaded.predict({"question": ["a", "b"]})   # tested: the input example gives schema Array(string), so a column of bare strings is rejected
```
Flavour equivalents accept code paths too (LangChain and LlamaIndex not run here (gated: unconfirmed, source is paywalled or blocked)): `mlflow.langchain.log_model(lc_model="chain.py", ...)`, `mlflow.llama_index.log_model(...)`.

## How it behaves
- The file is copied into the model artifact and **executed** at load time; `set_model` must be called at module level.
- Create `ModelConfig(development_config=...)` at **module level** (tested). It reads the local file during development; once logged, the `model_config` passed to `log_model` is used instead, so the same code works in both places. Calling it inside `load_context` (as an earlier version of this skill did) kept reading `config.yaml` from the working directory even though a different `model_config` was logged, and raised `FileNotFoundError` when that file was absent.
- Imports in the file must be satisfiable at serving time: declare them in `pip_requirements`/`extra_pip_requirements`. Helper modules go in `code_paths=["utils/"]`.

## Gotchas
- Executing the file means any top-level side effects (API calls, reading local paths) run during `load_model`; keep the module import-safe.
- Secrets: never hard-code keys in the file or config; read them from env vars at `load_context` time.
- Relative paths inside the file resolve against the serving working directory, not your repo; load data via `context.artifacts`.
- Validate before deploying: `mlflow.models.predict(model_uri=info.model_uri, input_data=..., env_manager="uv")` builds a clean env and runs the model (ran with `env_manager="local"`, which returned `{"predictions": [...]}`; the `uv` environment build was not run here (gated: unconfirmed, source is paywalled or blocked)).

## Verify
- [ ] `load_model` works in a fresh environment (not just the notebook that logged it).
- [ ] No API keys appear in the logged artifacts.
- [ ] The model's signature/input example match what the serving layer sends.
