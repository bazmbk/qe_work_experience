"""SafeSend Payment Validator (student starter file).

This file is where you build the core validation logic for the SafeSend exercise.

Your job is to implement `validate_payment(payment)` so it returns a tuple:
  (decision, reasons)

- decision must be one of: APPROVE, REJECT, REFER
- reasons must be a list of stable string codes (so tests can assert on them)

See `safesend_qe_exercise_one_pager_and_guidance.md` and the phase files for the detailed requirements.

When you are ready to check your work, run:
  python test_validator.py

"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

# Decisions
APPROVE = "APPROVE"
REJECT = "REJECT"
REFER = "REFER"

# Reason codes (use these exact strings in your output)
INVALID_AMOUNT_LOW = "invalid_amount_low"
INVALID_AMOUNT_HIGH = "invalid_amount_high"
INVALID_SORT_CODE = "invalid_sort_code"
INVALID_ACCOUNT_NUMBER = "invalid_account_number"
REFER_HIGH_VALUE = "refer_high_value"
REFER_SCAM_KEYWORDS = "refer_scam_keywords"

# Risk keywords for the reference field (case-insensitive).
SUSPICIOUS_KEYWORDS = ["crypto", "investment", "urgent"]


def validate_payment(payment: Dict[str, Any]) -> Tuple[str, List[str]]:
    """Validate a payment and return (decision, reasons).

    The function should:
      1) Check the input format and limits (REJECT reasons).
      2) If the input is valid, check risk gates (REFER reasons).
      3) Otherwise, return APPROVE.

    The starter tests in `test_validator.py` expect stable reason codes.
    """

    # TODO: Implement the validator logic here.
    # - Validate amount, sort code, account number.
    # - Return APPROVE / REJECT / REFER.
    # - Return a list of reason codes for any failures or referrals.

    raise NotImplementedError("Implement validate_payment in validator.py")


if __name__ == "__main__":
    print("Run `python test_validator.py` to verify your solution.")
