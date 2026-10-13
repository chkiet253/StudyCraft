---
name: coding-conventions
description: Use when implementing, changing, or refactoring StudyCraft application code, including AI/model integrations, and when deciding code placement or project-specific implementation patterns. For review-only work use code-review; for diagnosis without implementation use systematic-debugging.
---

# StudyCraft coding conventions

Follow [AGENTS.md](../../../AGENTS.md). This skill connects implementation work to StudyCraft's accepted requirements, documented coding rules, and actual repository state.

## Ground the change

- Read [coding standards](../../../docs/guides/coding-standards.md) before implementation. Read [docs/README.md](../../../docs/README.md) for the documentation map and conflict rules, then inspect the requirements, SPEC, API/database contracts, and ADRs relevant to the task.
- Inspect the current source, manifests, tests, and CI before deciding where code belongs or which commands and tools apply. Follow nearby code patterns where they remain consistent with accepted requirements.
- Distinguish implemented behavior from proposed architecture, assumptions, and TODOs. The planned stack and paths in documentation do not prove code, dependencies, model runtimes, or checks exist.
- Preserve unrelated work and inspect repository status before editing. Keep changes focused and use the smallest sufficient design.

## Apply project rules

- Use docs/guides/coding-standards.md as the source for naming, formatting, Python/FastAPI boundaries, errors, logging, and manual review conventions; do not duplicate or override its details here.
- Use the coding guide for Python 3.12/FastAPI style. Confirm each other stack component from manifests and source; treat documentation-only choices as proposed until code or configuration confirms them.
- The coding guide says linting, formatting tools, hooks, and CI are intentionally unconfigured. Do not add or reintroduce them unless the project owner requests that change.
- Keep code in its owning module and preserve API, persistence, and versioning contracts. Update related schemas, OpenAPI, migrations, tests, and documentation when an authorized behavior change requires it.

## Protect AI and learning-data boundaries

- Treat learner materials, submissions, external content, and model output as untrusted data. Validate output against the operation's schema and semantic constraints in application code before storing or acting on it. Prompts do not enforce authorization or state transitions.
- Keep model work bounded to the requested operation and approved context. Do not add agents, vector search, cloud model calls, fine-tuning, or external integrations unless the user and current project decisions authorize them.
- Preserve original submissions and learning records; store corrections separately and retain journal revisions as required by the current contracts. In the MVP, model output must not silently change a learner's goals, activity status, or claims of mastery.
- Keep raw learner content, chat, prompts, and model replies out of technical logs. Send only task-relevant, bounded context to a model.
- Separate deterministic application checks using a fake model adapter from real local-model evaluation. Report the model, hardware, evaluation inputs, and human review actually used; fake tests do not establish model quality.

## Verify and report

- Derive validation commands from current project configuration. Exercise relevant success and failure paths for behavior changes; use isolated test data and deterministic model doubles for routine automated checks.
- Keep real model runs separate from routine tests and within the task's authorization for cost and effects. Report what ran, what did not, and any remaining uncertainty.
- Inspect the final diff, including new files. For documentation-only changes, validate content, links, and the diff without inventing application tests.
## Reference

This workflow takes inspiration from the public [Clean Code Skills](https://github.com/btseee/clean-code-skills) project. StudyCraft's coding guide and contracts remain the source for project-specific rules.
