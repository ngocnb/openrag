# AGENT_LOOPS.md

This document defines the automated workflow the agent follows during the **Night Shift** — the period when the human operator is away and the agent works autonomously through specs and bugs.

---

## Prerequisites Before Starting

- The human has placed completed spec documents in `./planning/planning/specs/`.
- Codebase documents are in `./planning/codebase`. Read it first to understand the project structure.
- Specs prefixed with `draft-` are **ignored** — do not pick them up.
- The working tree should be on the correct branch before the loop begins.

---

## The Loop

### Step 0 — Prep

1. Inspect the current working tree.
2. If there are uncommitted changes:
   - If they are coherent and complete: **commit** them with a descriptive message.
   - If they are incomplete or unclear: **stash** them.
3. Run the **entire test suite**.
4. Fix any pre-existing test failures before proceeding.
5. Do not move forward until the baseline is clean and all tests pass.

---

### Step 1 — Select a Task

- Check for **open bugs** first from `./planning/bugs/`. Bugs have priority over features.
- If no bugs remain, pick the next **feature spec** from `./planning/specs/` (non-draft).
- Work on one task at a time. Do not parallelize tasks across iterations.

---

### Step 2 — Load and Analyze the Spec

- Read the full spec document for the selected task.
- Understand the feature, all described edge cases, and any constraints.
- Note anything unclear — do not invent requirements; flag gaps as TODOs for human review.

---

### Step 3 — Load Relevant Documentation and Code

- Consult `@AGENTS.md` to identify which docs apply to this task.
- Load all relevant workflow docs, skill docs, and system docs.
- Read the relevant source code to understand current implementation context.

---

### Step 4 — Develop a Testing Plan

This step is **critical**. A robust testing plan is non-negotiable.

- Define all test cases: happy paths, edge cases, error conditions.
- Identify which parts of the system are affected and need regression coverage.
- Document the plan clearly (for your own reasoning, not for the human).

---

### Step 5 — Write Tests (Expect Failures)

- Write all tests based on the testing plan.
- Run the tests — they should **fail** at this point. That is expected and correct.
- A test suite that passes before implementation is a broken test suite.

---

### Step 6 — Develop an Implementation Plan

- Capture context using `/gsd:discuss-phase`.
- Build a detailed implementation plan using `/gsd:plan-phase`.
- The human will **never read this**. It is for your own reasoning and structure.
- Be thorough. Consider the full impact on the system.

---

### Step 7 — Run Review Agents (Pre-Implementation)

- Invoke each of the six review personas defined in `REVIEW_PERSONAS.md`:
  - Designer
  - Architect
  - Domain Expert
  - Code Expert
  - Performance Expert
  - Human Advocate
- Each persona loads their assigned documentation and reviews the plan against it.
- Each persona also flags any gaps or outdated sections in their own docs.

---

### Step 8 — Adapt Plan Based on Reviews

- Incorporate feedback from all review agents.
- If any reviewer does not give a **green light**, revise the plan and **loop back to Step 7**.
- Continue until all six reviewers give a green light.

---

### Step 9 — Implement

- Execute the implementation plan using `/gsd:execute-phase`.
- Update all affected documentation in-place (docs live in the codebase under `Docs/`).
- Follow existing conventions exactly unless a doc explicitly states otherwise.

---

### Step 10 — Static Analysis and Tests

Run all of the following, fix any issues, and iterate:

- Type checking (strict mode)
- Linting (strict mode)
- Compiler / build
- Bundle size reporter (if applicable)
- Any other configured static analysis tools
- The relevant feature/bug tests written in Step 5

Do not proceed until everything passes cleanly.

---

### Step 11 — Full Regression Suite

- Run the **entire test suite**.
- Fix any regressions introduced by this change.
- Do not skip or suppress failures.

---

### Step 12 — Run Review Agents (Post-Implementation)

- Run all six review agents again, this time against the **implementation diff**.
- If any reviewer does not give a green light, loop back to Step 10.
- Continue until all six reviewers approve the implementation.

---

### Step 13 — Capture Unrelated TODOs

- Note any unrelated issues, tech debt, or concerns noticed along the way.
- Add them to the `TODOS.md` file under a section marked **NEEDS INPUT FROM USER**.
- Do **not** fix unrelated issues during this task. Stay focused.

---

### Step 14 — Wrap Up the Task

1. Write a `CHANGELOG` entry for this task.
2. Commit with a **detailed commit message** written for human context:
   - What changed and why.
   - Any non-obvious decisions made.
   - References to the spec.
3. Move it to `./.planning/specs-done/` folder.

---

### Step 15 — Loop

- Return to **Step 1** and select the next task.
- Continue until all bugs are resolved and all completed specs are implemented.

---

### Step 16 — Final Report

When all tasks are complete:

- Write a **concise summary report** for human review.
- Keep it brief — detailed context lives in the commit messages.
- Cover: what was completed, what was skipped and why, and anything requiring human input.

---

### Step 17 — Go Silent

- The Night Shift is complete.
- Do **not** start new work.
- Wait silently for the human to review in the morning.

---

## Important Principles

- **Never wait for human input** mid-loop. If blocked, log it as a TODO and move on.
- **Strictness is good.** Strict type checking and linting catch agent errors that would otherwise reach human review.
- **Tokens are cheap. Human time is not.** Run as many validation passes as needed before a human ever looks at it.
- **Do not fix unrelated things.** Capture them and move on.
- **Docs are living artifacts.** Update them as part of implementation, not after.
