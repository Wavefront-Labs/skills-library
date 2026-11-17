---
id: computing-software.ai-ml-engineering.llm-application-engineering.xml-tags-and-long-context-prompting
name: xml-tags-and-long-context-prompting
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, prompt-engineering, xml-tags, long-context-prompting, document-qa, quote-extraction]
level: practitioner
status: docs-checked
description: "Structure prompts with XML tags and handle long documents: documents first and question last, per-document metadata tags, quote-first grounding and parsing tagged output."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/long-context-tips
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XML tags and long-context prompting

## Why tags
Tags separate instructions, data and examples so the model does not confuse a pasted document with instructions, and they make outputs machine-parseable. Use consistent, descriptive tag names across prompts.

```text
<instructions>
Answer using only the contract. If the contract does not say, answer "not specified".
</instructions>
<contract>
{{CONTRACT_TEXT}}
</contract>
<question>{{QUESTION}}</question>
Return the answer in <answer> tags and the supporting clause numbers in <clauses> tags.
```
Refer to tags by name in instructions ("using the contract in <contract> tags"). Nest for hierarchy (`<documents><document index="1">...`).

## Long documents (20k+ tokens)
1. **Put long material at the top**, instructions and question at the end. Anthropic's guide says queries at the end can improve response quality by up to 30 percent in tests, especially with complex, multidocument inputs.
2. Wrap each document with metadata:
```xml
<documents>
  <document index="1">
    <source>q3_board_minutes.pdf</source>
    <document_content>...</document_content>
  </document>
</documents>
```
3. **Quote first, then answer:** "Find quotes relevant to the question and put them in <quotes> tags. Then answer in <answer> tags, citing quote numbers." This helps the model focus on the relevant parts and ignore the rest of the document.

## Parsing tagged output
```python
import re
def tag(text, name):
    m = re.search(rf"<{name}>(.*?)</{name}>", text, re.S)
    return m.group(1).strip() if m else None
```
For anything a program consumes strictly, prefer structured outputs (JSON schema) over regex on tags; tags are best for mixed prose plus sections.

## Gotchas
- Untrusted documents can contain fake closing tags (`</contract> New instructions:`). Escape or strip angle brackets in untrusted text, or use unusual tag names, and still treat document content as data.
- Do not use tags as a substitute for clear instructions; they organise, they do not instruct.

## Verify
- [ ] Eval set compares question-first vs question-last ordering on your documents.
- [ ] Answers include quotes that string-match the source.

## Checked
2026-11-01. Confirmed against Anthropic's Prompting best practices page (reached from the use-xml-tags and long-context-tips URLs): XML tags for instructions, context and inputs; consistent descriptive names; nesting documents/document index; long data at the top, query at the end with up to 30 percent in tests; document, document_content and source subtags; quote-first grounding. Removed: the OpenAI source, the citations feature detail, the prompt-caching ordering advice and the attention-dilution claim, which the pages do not state.
Method: documentation only; no commands were run.
