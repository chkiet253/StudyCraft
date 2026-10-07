---
name: testing
description: Test or verify behavior changes, bug fixes, refactors, and integrations with focused regression checks and red-green-refactor where appropriate. Use for test design or execution; documentation-only edits need reference and diff validation rather than application tests.
---

# Testing

Follow [AGENTS.md](../../../AGENTS.md). Derive acceptance cases from the requested behavior, project requirements, and existing contracts; distinguish draft design choices from implemented tests. Discover the project's test and release criteria rather than assuming a fixed spec filename.

## Choose meaningful checks

Discover the actual runner, fixtures, scripts, and CI commands. Start with the narrowest test that exercises the changed behavior through a public boundary. Add integration or interface checks when the failure depends on storage, transactions, or user interaction. Use the target database engine when testing engine-specific semantics, with a dedicated test database and isolated fixtures rather than operational data.

For new testable behavior and bug fixes, use red-green-refactor:

1. Write a case for the intended outcome and observe the expected failure. A setup error does not demonstrate the missing behavior.
2. Implement the minimum change and observe the case pass.
3. Simplify within scope, then rerun the relevant checks.

For a behavior-preserving refactor, establish a passing baseline and compare it after the change. If automation is unavailable, use a repeatable manual check or minimal reproducer and explain its limits. Documentation and formatting changes need output/diff inspection. Do not delete existing work just because a test was written later.

## Cover the affected project invariant

Select cases relevant to the change rather than running this list as a universal checklist:

- Valid, invalid, missing, and boundary inputs; serialization, encoding, and output contracts.
- State transitions, permissions, duplicate operations, and concurrency where the behavior depends on them.
- Persistence, partial failure, external errors, interruption, and resource cleanup where applicable.
- Observable interface behavior and recovery; include browser or other platform checks for changes that require them.

Assert observable records, state, and user outcomes. Test doubles control external responses while the application path still runs; assertions only about mock calls are insufficient.

## External systems and completion

Keep routine automated checks deterministic and independent of live external services, including malformed responses and external errors. When no harness exists, add only the minimal setup necessary for an authorized behavior change; a verification-only task should report missing prerequisites.

Run live integration checks within the task's authorization for external effects and cost. For AI features, separately evaluate quality using recorded model and evaluation-criteria versions, representative inputs, repeated runs when needed, and human judgments where appropriate. Passing test-double checks does not establish real service integration or live AI quality.

Run relevant downstream checks after focused checks pass. Inspect the final diff and report commands, results, skipped or blocked cases, and the scope of the evidence. Report pre-existing failures separately; do not weaken assertions or bypass checks to produce a green result.

Workflow inspiration: [Superpowers test-driven development](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md).
