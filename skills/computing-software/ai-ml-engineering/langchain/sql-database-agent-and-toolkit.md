---
id: computing-software.ai-ml-engineering.langchain.sql-database-agent-and-toolkit
name: sql-database-agent-and-toolkit
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, agents, sql-agent, sqldatabasetoolkit, text-to-sql, read-only-database, query-checker]
level: practitioner
status: docs-checked
description: "Let an LLM answer questions over a SQL database with LangChain's SQLDatabase and toolkit: chain vs agent, toolkit tools, narrow permissions, approval, proper nouns."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/tutorials/sql_qa.ipynb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL database agent and toolkit

**Goal:** natural-language questions answered by generated SQL, safely and with correct results.

## Security first
The tutorial warns that executing model-generated SQL has inherent risk: scope the database connection permissions as narrowly as possible for the chain or agent. This mitigates but does not eliminate the risk. Executing the query is called "the most dangerous part" of a SQL chain; consider a human approval step before execution. A system-prompt line such as "DO NOT make any DML statements" is an instruction to the model, not a permission boundary, so also use a connection that cannot write (design guidance).

## Setup (v0.3 era imports)
```python
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
db = SQLDatabase.from_uri("sqlite:///Chinook.db")   # SQLAlchemy-driven
print(db.dialect, db.get_usable_table_names())
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
agent = create_react_agent(llm, tools, prompt=system_message)
```
`db.get_table_info()` returns the schema text used in prompts; `db.run(sql)` executes.

## Two designs
- **Chain** (LangGraph sequence): write_query (structured output giving a query) -> execute_query (`QuerySQLDatabaseTool`) -> generate_answer. Predictable, but it runs a query for any input (even "hello") and cannot do multi-query questions.
- **Agent**: can query repeatedly, recover from errors by regenerating a failed query, and answer questions about the schema itself. Less predictable than the chain.

Human approval for the chain: compile with a checkpointer (`MemorySaver`) and `interrupt_before=["execute_query"]`, give a `thread_id` in config, then resume by streaming `None` with the same config once approved.

## Toolkit tools
The toolkit's tools, as named in the tutorial's traces: `sql_db_query` (run a query; returns an error message if wrong), `sql_db_schema` (input: comma-separated table names; returns schema plus sample rows), `sql_db_list_tables`, `sql_db_query_checker` (an LLM pass that rechecks the query for common mistakes such as NOT IN with NULLs, UNION vs UNION ALL, BETWEEN for exclusive ranges, type mismatches, identifier quoting, wrong join columns).

## System prompt (from the tutorial)
Include: the dialect and a `top_k` result limit unless the user asks for a number; order by a relevant column; never select all columns, only relevant ones; double-check the query before executing and rewrite on error; no DML (INSERT, UPDATE, DELETE, DROP); always list tables first, then query the schema of the most relevant tables.

## Proper nouns and high-cardinality columns
Filters on names (artists, songs, addresses) fail on misspellings. The tutorial builds a vector store of the distinct values, wraps its retriever with `create_retriever_tool(retriever, name="search_proper_nouns", description=...)`, adds it to `tools`, and tells the agent in the system prompt to always look up proper nouns first, never guess. In its example "alis in chain" resolved to "Alice In Chains".

## Further techniques the tutorial points to
Few-shot prompting strategies, query checking and error handling, and large-database techniques each have their own how-to guide (not read for this skill).

## Evaluate
Compare execution results against gold answers rather than SQL text, and track error and retry rates (practice advice, not from the tutorial).

## Verify
- [ ] The DB credentials cannot write (try an INSERT as that role; it must fail).
- [ ] A result limit is applied in the prompt and, if possible, enforced by the database.
- [ ] Questions with misspelled names resolve through the lookup tool.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 sql_qa tutorial: security warning wording and approval step, SQLDatabase usage, chain steps and limits, interrupt_before pattern, agent advantages, toolkit tool names and checker mistake list, system prompt contents, create_react_agent call, proper-noun retriever tool.
- Removed as unconfirmed: the Postgres URI, include_tables and sample_rows_in_table_info arguments, statement_timeout, curated-view advice, column-comment advice, claims that few-shot examples beat model upgrades, large-schema table-selection step, ambiguity-of-column-names claim, SELECT * and LIMIT 50 specifics, the LangGraph SQL-agent tutorial and toolkit API reference sources (not read), and the python.langchain.com URL (no longer serves docs).
Method: documentation only; no commands were run.
