# SafeSend Validator: Code Flow (Mermaid Diagram)

This diagram explains the detailed logic in `validator_solved.py` (and the student starter `validator.py`). It shows how inputs are parsed, validated, and how the decision (`APPROVE` / `REJECT` / `REFER`) is produced.

**Narrative summary:**
1. Normalize inputs (strip punctuation, parse numbers).
2. Reject immediately if any required field is invalid (REJECT + reason codes).
3. If valid, check risk gates (high value and scam keywords) to decide REFER.
4. Otherwise, return APPROVE.

> Note: Reason codes are stable strings used by the tests.

```mermaid
flowchart TD
  Start([Start]) --> Normalize[Extract & normalise inputs]
  Normalize --> ParseAmount[Parse amount]
  Normalize --> NormaliseSort[Normalise sort code]
  Normalize --> NormaliseAcc[Normalise account number]
  Normalize --> PrepareRef[Prepare reference text]

  subgraph FunctionalValidity
    direction TB
    F1["Amount missing/invalid OR < 0.01?"] -->|Yes| INVALID_LOW[invalid_amount_low]
    F1 -->|No| F2["Amount > 25000?"]
    F2 -->|Yes| INVALID_HIGH[invalid_amount_high]
    F2 -->|No| F3[Sort code length != 6?]
    F3 -->|Yes| INVALID_SORT[invalid_sort_code]
    F3 -->|No| F4[Account number length != 8?]
    F4 -->|Yes| INVALID_ACC[invalid_account_number]
  end

  INVALID_LOW --> CheckReject
  INVALID_HIGH --> CheckReject
  INVALID_SORT --> CheckReject
  INVALID_ACC --> CheckReject
  F4 --> CheckReject
  CheckReject{Any REJECT reasons?} -->|Yes| REJECT[REJECT + reasons]
  CheckReject -->|No| RiskCheck["Risk checks (REFER)"]

  subgraph RiskGates
    direction TB
    R1["Amount > 5000?"] -->|Yes| R_HIGH[refer_high_value]
    R1 -->|No| R2[Reference has scam keywords?]
    R2 -->|Yes| R_SCAM[refer_scam_keywords]
    R2 -->|No| NO_RISK[No risk reasons]
  end

  R_HIGH --> CheckRisk
  R_SCAM --> CheckRisk
  NO_RISK --> CheckRisk
  CheckRisk{Any risk reasons?} -->|Yes| REFER[REFER + reasons]
  CheckRisk -->|No| APPROVE[APPROVE]

  style APPROVE fill:#22c55e,stroke:#16a34a,color:#052e16
  style REJECT fill:#ef4444,stroke:#dc2626,color:#7f1d1d
  style REFER fill:#f59e0b,stroke:#d97706,color:#7c2d12
```

## Key helper functions

- `_normalise_digits(value)`
  - Removes anything that isn't `0-9` (e.g., `"12-34-56"` → `"123456"`).

- `_parse_amount_pounds(value)`
  - Converts input to `Decimal` and returns `None` for invalid values.

## Suspicious keywords (risk triggers)

The validator considers the `reference` unsafe if it contains any of:
- `crypto`
- `investment`
- `urgent`

These are checked case-insensitively (e.g., `"Crypto"` matches).
