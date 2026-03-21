# Phase 3: Implement the Validator (Small Steps) (50-60 mins)

## Goal of Phase 3
By the end of this phase you should have:
- A working validator function/script that returns a `decision` and a list of `reasons`
- Implemented checks in the right order (normalise -> functional validity -> risk gates)
- Evidence you can explain: what each check does and how it maps to your tests
- Confidence you didn’t “accidentally” stop after the first error (you should return **all** reasons)

This phase is about **building the thing you designed in Phases 1 and 2**.

## Timebox (suggested)
- 0:00-0:10 Turn your design into an implementation plan
- 0:10-0:35 Implement in small steps + run manual checks
- 0:35-1:00 Wire up/confirm reason codes + update micro gaps with tests
- 1:05-1:15 Prepare for Phase 4 (automated test run)

## Step-by-step guidance

### 1) Start from your design, not from random code (0:00-0:10)
Before you touch “real” logic:
1. Re-check your chosen function contract:
   - Example: `validate_payment(payment) -> (decision, reasons)`
2. Confirm your output shape:
   - `decision`: `APPROVE` / `REJECT` / `REFER`
   - `reasons`: a list of reason codes (stable strings)
3. Confirm your check order:
   - Normalise inputs first
   - Functional validity checks next (these can produce `REJECT`)
   - Risk gates last (these can produce `REFER`)

### AI Chat Mode Guidance: Function Contract & Output Design
Use chat mode to help design your function interface:
- "Help me design the function signature for validate_payment that takes a payment dict and returns decision and reasons."
- "What should the output structure be for the SafeSend validator - decision string and reasons list?"
- "Review my function contract: validate_payment(payment) -> (decision, reasons) - is this testable?"

Why this matters:
- In bank-style logic, `REJECT` should take priority over `REFER` when validity fails.

4. Make your output deterministic (so tests don't flake)
   - Decide a consistent ordering for `reasons`.
   - A simple rule: append **functional validity reasons first**, then **risk gate reasons**.
   - Keep reason codes stable (never depend on long free-text messages for tests).

### AI Chat Mode Guidance: Reason Code Design
Use chat mode to help design stable reason codes:
- "Suggest stable reason codes for SafeSend validator that are short and machine-readable."
- "How should I order reasons in the list - functional validity first, then risk gates?"
- "Help me define reason codes that won't change when I update error messages."

5. Write a short “rule to behaviour” mapping (one line per rule)
   - For each rule ID in your Phase 1/2 requirements list, write:
     - what it is checking
     - which reason code it adds
     - which decision it can influence (`REJECT` or `REFER`)

### AI Chat Mode Guidance: Rule Mapping
Use chat mode to help create your rule-to-behavior mapping:
- "Help me create a mapping table showing each validation rule, its reason code, and decision outcome."
- "Review my rule mapping - does each rule have a clear reason code and appropriate decision?"

6. Create a tiny implementation plan you can tick off
   - Tick items in the order you will code them:
     - [ ] Normalise inputs (sort code formatting)
     - [ ] Run functional validity checks and populate `reasons`
     - [ ] If any functional reasons exist, set `decision = REJECT`
     - [ ] Otherwise, run risk gates and populate additional reasons
     - [ ] If any risk reasons exist, set `decision = REFER`
     - [ ] If `reasons` is empty, set `decision = APPROVE`

### AI Chat Mode Guidance: Implementation Planning
Use chat mode to help create your implementation roadmap:
- "Help me create a step-by-step checklist for implementing the SafeSend validator in the right order."
- "What should be the implementation sequence: normalisation, functional checks, risk gates?"
- "Review my implementation plan - does the check order match the decision precedence rules?"

Template you can copy into your notes (fill in the blanks)

```text
Function contract:
  Input fields: amount, sort_code, account_number, recipient_name, reference
  Output:
    decision = APPROVE | REJECT | REFER
    reasons = [reason_code_1, reason_code_2, ...]  (ordered: functional first, then risk)

Decision precedence:
  REJECT wins over REFER when functional validity fails

Check order:
  1) Normalise sort_code
  2) Functional validity checks -> may add invalid_* reasons
  3) If any invalid_* reasons: decision REJECT (skip risk gates)
  4) Else risk gates -> may add refer_* reasons -> decision REFER

Rule mapping:
  invalid_amount_low      -> adds invalid_amount_low  -> decision REJECT
  invalid_amount_high     -> adds invalid_amount_high -> decision REJECT
  invalid_sort_code       -> adds invalid_sort_code  -> decision REJECT
  invalid_account_number  -> adds invalid_account_number -> decision REJECT
  refer_high_value        -> adds refer_high_value  -> decision REFER
  refer_scam_keywords     -> adds refer_scam_keywords -> decision REFER
```

7. Use AI to sanity-check, not to replace your thinking
   - Ask AI: “Is my decision precedence and reason-code ordering testable?”
   - Ask AI: “Any missing checks or ambiguous assumptions that would break my reason codes?”
### AI Chat Mode Guidance: Planning Validation
Use chat mode to validate your design before coding:
- "Review my rule mapping - do all rules have appropriate reason codes and decision outcomes?"
- "Is my check order correct: normalisation -> functional validity -> risk gates?"
- "Will my reason code ordering (functional first, then risk) make tests reliable?"### AI Chat Mode Guidance: Generate Implementation Plan
Use VS Code's chat mode to help create your implementation plan:
- "Help me create a step-by-step implementation checklist for the SafeSend validator based on these rules and reason codes."
- "Review my function contract and suggest any improvements for testability."
### 2) Represent a payment cleanly (0:10-0:15)
Use a simple structure so tests are easy to write later:
- Represent a payment as a dictionary/object with keys:
  - `amount`
  - `sort_code`
  - `account_number`
  - `recipient_name`
  - `reference`

Even if you can code without it, using a consistent structure helps reduce bugs.

### 3) Implement input normalisation first (0:15-0:25)
Normalisation is “making inputs consistent” before checks:
- Example task: remove hyphens/spaces from `sort_code` before checking digit length.

Implementation approach:
1. Write a small normalisation helper (or inline it):
   - Input: raw `sort_code`
   - Output: normalised string containing digits only (if that’s your design)
2. Run a quick manual check using 2-3 sample payments.

Manual validation example ideas:
- sort code like `12-34-56` should become `123456`
- sort code with spaces should also become `123456`
### AI Chat Mode Guidance: Generate Normalisation Code
Use chat mode to help implement input normalisation:
- "Write a Python function to normalise a UK sort code by removing hyphens and spaces, keeping only digits."
- "Show me how to handle sort code normalisation in the validator function."
### 4) Implement functional validity checks next (0:25-0:40)
These checks can trigger `REJECT`.

Recommended pattern:
1. Create a list called `reasons` (initially empty)
2. For each functional validity rule:
   - If it fails, add the appropriate reason code to `reasons`
3. After all functional checks:
   - If `reasons` is not empty, set `decision` to `REJECT`
   - Skip risk gates (optional depending on your design, but scenario priority implies REJECT wins)

Functional validity rules to implement:
- `amount` >= 0.01
- `amount` <= 25000
- `sort_code` exactly 6 digits (after normalisation)
- `account_number` exactly 8 digits

### AI Chat Mode Guidance: Generate Functional Validity Code
Use chat mode to help implement functional checks:
- "Write Python code to validate amount is between 0.01 and 25000, adding 'invalid_amount_low' or 'invalid_amount_high' to reasons list."
- "Write code to validate sort code has exactly 6 digits after normalisation, adding 'invalid_sort_code' if it fails."
- "Write code to validate account number has exactly 8 digits, adding 'invalid_account_number' if it fails."

### 5) Implement risk gates last (0:40-0:55)
Risk gates only matter when the payment is already functionally valid.

Recommended pattern:
1. Start risk gating with the assumption:
   - `decision` is currently “valid so far”
2. Evaluate each risk rule:
   - high value amount gate (amount over 5000)
   - suspicious keywords in `reference`
3. If any risk gate triggers:
   - set `decision` to `REFER`
   - add all applicable risk reason codes to `reasons`

Important requirement:
- Return **all reasons**, not just the first one.

### AI Chat Mode Guidance: Generate Risk Gate Code
Use chat mode to help implement risk checks:
- "Write Python code to check if amount > 5000 and add 'refer_high_value' to reasons if true."
- "Write code to check if reference contains suspicious keywords like 'crypto', 'investment', 'urgent' and add 'refer_scam_keywords' if found."
- "Show me how to implement risk gates that only run after functional validity passes."

### 6) Manual run before you automate (0:50-1:00)
Run the validator manually with:
- 1 good low-risk example -> should be `APPROVE`
- 1 invalid example (format/limits) -> should be `REJECT`
- 1 valid but risky example -> should be `REFER`

When you run it, check both:
- the `decision`
- the `reasons` list contains the expected reason codes

### 7) Debugging when something breaks (every time you hit errors)
If you hit an error:
1. Read the error message carefully
2. Ask AI to explain it in plain English
3. Identify the exact line/type/assumption causing the problem
4. Fix the code and re-run the same manual checks

### AI Chat Mode Guidance: Debug and Fix Issues
Use chat mode for debugging help:
- "Explain this Python error: [paste error message] and suggest how to fix it."
- "My validator is returning REFER instead of REJECT for invalid amounts. Help me debug the decision logic."
- "Help me test my validator manually with sample data to verify it works correctly."

Micro gap checks while coding:
- After each rule is implemented, confirm you have (or will have) a matching test for it.
- If your tests show a mismatch with the scenario, update assumptions (Phase 1), not your expectations silently.

## Helpful visualisations (optional)

### A) Implementation pipeline

```mermaid
flowchart TD
  Start[Payment input] --> N[Normalise inputs]
  N --> F[Functional validity checks]
  F -->|Failures| R[REJECT + reasons]
  F -->|Passes| K[Risk gate checks]
  K -->|Triggers| S[REFER + reasons]
  K -->|No triggers| A[APPROVE]
```

### B) Reasons list (return all errors)

```mermaid
flowchart TD
  A[Payment] --> B[Run all checks]
  B --> C[Collect reason codes]
  C --> D[Set decision from rules]
  D --> E[Return decision and reasons]
```

## AI Chat Mode Prompts (Organized by Implementation Step)

### Planning & Design
- "Help me design the function signature for validate_payment that takes a payment dict and returns decision and reasons."
- "What should the output structure be for the SafeSend validator - decision string and reasons list?"
- "Review my function contract: validate_payment(payment) -> (decision, reasons) - is this testable?"
- "Suggest stable reason codes for SafeSend validator that are short and machine-readable."
- "How should I order reasons in the list - functional validity first, then risk gates?"
- "Help me define reason codes that won't change when I update error messages."
- "Help me create a mapping table showing each validation rule, its reason code, and decision outcome."
- "Review my rule mapping - does each rule have a clear reason code and appropriate decision?"
- "Help me create a step-by-step checklist for implementing the SafeSend validator in the right order."
- "What should be the implementation sequence: normalisation, functional checks, risk gates?"
- "Review my implementation plan - does the check order match the decision precedence rules?"
- "Review my rule mapping - do all rules have appropriate reason codes and decision outcomes?"
- "Is my check order correct: normalisation -> functional validity -> risk gates?"
- "Will my reason code ordering (functional first, then risk) make tests reliable?"
- "Is my decision precedence and reason-code ordering testable?"
- "Any missing checks or ambiguous assumptions that would break my reason codes?"

### Input Normalisation
- "Write a Python function to normalise a UK sort code by removing hyphens and spaces, keeping only digits."
- "Show me how to handle sort code normalisation in the validator function."

### Functional Validity Checks
- "Write Python code to validate amount is between 0.01 and 25000, adding 'invalid_amount_low' or 'invalid_amount_high' to reasons list."
- "Write code to validate sort code has exactly 6 digits after normalisation, adding 'invalid_sort_code' if it fails."
- "Write code to validate account number has exactly 8 digits, adding 'invalid_account_number' if it fails."

### Risk Gate Checks
- "Write Python code to check if amount > 5000 and add 'refer_high_value' to reasons if true."
- "Write code to check if reference contains suspicious keywords like 'crypto', 'investment', 'urgent' and add 'refer_scam_keywords' if found."
- "Show me how to implement risk gates that only run after functional validity passes."

### Debugging & Testing
- "Explain this Python error: [paste error message] and suggest how to fix it."
- "My validator is returning REFER instead of REJECT for invalid amounts. Help me debug the decision logic."
- "Help me test my validator manually with sample data to verify it works correctly."
- “Review my check order: REJECT should be decided from functional validity before risk gates.”
- “Suggest a minimal normalisation approach for sort code while keeping it testable.”

## End-of-Phase 3 checklist
- [ ] Normalisation is implemented (e.g., sort code spaces/hyphens removed if your design includes this)
- [ ] Functional validity checks produce `REJECT` with reason codes
- [ ] Risk gates produce `REFER` only after functional validity passes
- [ ] The validator returns **all** reasons (not only the first)
- [ ] You can run 2-3 manual examples and explain the outcomes
- [ ] Your implementation aligns with Phase 2 expected `decision` and `reasons`

