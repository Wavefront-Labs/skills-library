---
id: computing-software.ai-ml-engineering.mastra.agent-level-skills
name: agent-level-skills
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, skill, skillmd, createskill, agent-skills, requestcontext, dynamic-skills]
level: practitioner
status: docs-checked
description: "Attach Agent Skills to a Mastra agent: createSkill inline, filesystem paths, per-request resolvers, merging with workspace skills, getSkill/listSkills, validation."
sources:
  - https://mastra.ai/docs/skills
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: give one Mastra agent reusable skills without needing a workspace.

Agent-level skills belong to one agent and can be defined in code; workspace skills are discovered from the filesystem and shared by every agent on that workspace. Skills follow the Agent Skills specification.

## Inline
```typescript
import { Agent } from '@mastra/core/agent'
import { createSkill } from '@mastra/core/skills'

const codeReview = createSkill({
  name: 'code-review',
  description: 'Use when reviewing code changes.',
  instructions: `When reviewing code: 1. Check correctness ...`,
  references: { 'changelog-format.md': '# Changelog Format ...' }, // optional
})

export const reviewer = new Agent({
  id: 'reviewer',
  model: 'your-model-id',
  instructions: 'You are a code review assistant.',
  skills: [codeReview],
})
```
The agent automatically gets `skill`, `skill_read` and `skill_search` tools to discover and load skills during conversation. `references` bundles supporting documents the agent reads with `skill_read`, like `references/` files in a filesystem skill.

## Filesystem paths
`skills` can mix paths and inline skills: `['./skills/code-review', './skills/testing', createSkill({...})]`. Each path points at a directory containing `SKILL.md` (read through `LocalSkillSource`, same format as workspace skills).

## Dynamic (per request)
Pass a function: `skills: ({ requestContext }) => requestContext.get('userRole') === 'developer' ? [devSkill] : [supportSkill]`.
- It receives `{ requestContext, tracingContext }` and returns `SkillInput[]` or a Promise of it.
- It runs once per `RequestContext`, inside a `resolve-skills` span during execution.
- It also runs on metadata reads such as `agent.listSkills()` and the server's agent endpoints, where `tracingContext.currentSpan` is `undefined`. Keep it fast and guard span use: `tracingContext?.currentSpan?.createChildSpan({ type: 'generic', name: '...' })`, then `span?.end()`.

## Merging with a workspace
If the agent has both `skills` and a workspace with skills, they merge; the agent-level skill wins on a name conflict.

## Programmatic access
`await agent.getSkill('code-review')` returns the skill (check it is truthy, then use `.instructions`); `await agent.listSkills()` returns entries with `name` and `description`.

## Validate before saving SKILL.md
```typescript
import { validateSkillContent } from '@mastra/core/skills'
const result = validateSkillContent({ content: skillMarkdown, directoryName: 'code-review' })
if (!result.valid) throw new Error(`Invalid skill:\n${result.errors.join('\n')}`)
// result.warnings lists non-blocking issues, such as very long instructions
```
It applies the same rules used at load time, including that `name` matches the directory name, and returns results instead of throwing. For an already-parsed frontmatter object use `validateSkillMetadata({ metadata, directoryName })`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. Removed unsupported agentskills.io attribution. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
