# Agent Instructions

This file is a reusable entry point for projects that copy the shared `.ai/` rules.
When working in a project, use that project's own `.ai/` directory as the source of
personal workflow guidance.

## Select the relevant guidance

- For requirements, business context, plans, or knowledge artifacts, read
  `.ai/planning.md`.
- For implementing, debugging, or changing code, read `.ai/coding.md`.
- For code review, audit, or diagnosis, read `.ai/review.md`. Do not implement a
  proposed fix unless the user asks for it.
- Before Git mutations or pull request preparation, read `.ai/git-workflow.md`.
- If a task spans several areas, read each applicable file. Skip unrelated rules
  instead of loading the whole `.ai/` directory by default.

## Apply the rules

- Treat `.ai/` as reusable workflow guidance, not as evidence about the project's
  current architecture or business behavior. Verify project facts from its source,
  configuration, and documentation.
- Follow applicable project instructions and the user's current request. Keep work
  within the requested scope, preserve unrelated changes, and report what was
  actually verified.
- If a referenced `.ai/` file is missing, do not invent its contents; continue with
  the available project instructions and mention the gap when it affects the work.

## Copying this template

Copy this `AGENTS.md` into each project's root alongside that project's own `.ai/`
copy. A parent-level `AGENTS.md` is not automatically inherited across independent
Git repositories.
