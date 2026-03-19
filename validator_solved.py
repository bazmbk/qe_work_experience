"""
SafeSend Payment Validator (starter implementation).

The exercise guidance expects a function with this contract:
  validate_payment(payment) -> (decision, reasons)

Where:
  decision is one of: APPROVE, REJECT, REFER
  reasons is a list of stable reason codes (strings)
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Tuple
import re


APPROVE = "APPROVE"
REJECT = "REJECT"
REFER = "REFER"


# Starter reason codes (stable strings so tests can assert on them)
INVALID_AMOUNT_LOW = "invalid_amount_low"
INVALID_AMOUNT_HIGH = "invalid_amount_high"
INVALID_SORT_CODE = "invalid_sort_code"
INVALID_ACCOUNT_NUMBER = "invalid_account_number"
REFER_HIGH_VALUE = "refer_high_value"
REFER_SCAM_KEYWORDS = "refer_scam_keywords"


SUSPICIOUS_KEYWORDS = ["crypto", "investment", "urgent"]


def _normalise_digits(value: Any) -> str:
    """
    Convert an input to digits-only by removing everything that isn't 0-9.
    This supports inputs like "12-34-56" -> "123456".
    """
    if value is None:
        return ""
    text = str(value)
    return re.sub(r"[^0-9]", "", text)


def _parse_amount_pounds(value: Any) -> Decimal | None:
    """
    Parse amount as pounds using Decimal for predictable comparisons.
    Returns None if parsing fails.
    """
    if value is None:
        return None

    try:
        # Convert to string to preserve user input like "10.50".
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


def validate_payment(payment: Dict[str, Any]) -> Tuple[str, List[str]]:
    """
    Validate a payment and return:
      (decision, reasons)

    decision:
      APPROVE: valid format, low risk
      REJECT: invalid format/limits
      REFER: valid format, but risk gates triggered

    reasons:
      Return ALL applicable reason codes (functional first, then risk).
    """
    reasons: List[str] = []

    # Extract inputs (use scenario key names)
    amount_raw = payment.get("amount")
    sort_code_raw = payment.get("sort_code")
    account_number_raw = payment.get("account_number")
    reference_raw = payment.get("reference")

    amount = _parse_amount_pounds(amount_raw)
    sort_code_digits = _normalise_digits(sort_code_raw)
    account_number_digits = _normalise_digits(account_number_raw)

    # --- Functional validity checks (REJECT reasons) ---
    # Amount must be at least 0.01
    if amount is None or amount < Decimal("0.01"):
        reasons.append(INVALID_AMOUNT_LOW)
    else:
        # Amount must be no more than 25000
        if amount > Decimal("25000"):
            reasons.append(INVALID_AMOUNT_HIGH)

    # Sort code must be exactly 6 digits
    if len(sort_code_digits) != 6:
        reasons.append(INVALID_SORT_CODE)

    # Account number must be exactly 8 digits
    if len(account_number_digits) != 8:
        reasons.append(INVALID_ACCOUNT_NUMBER)

    # If any functional reasons exist, REJECT takes priority.
    invalid_reasons = {
        INVALID_AMOUNT_LOW,
        INVALID_AMOUNT_HIGH,
        INVALID_SORT_CODE,
        INVALID_ACCOUNT_NUMBER,
    }
    has_invalid = any(r in invalid_reasons for r in reasons)

    if has_invalid:
        return (REJECT, reasons)

    # --- Risk gate checks (REFER reasons) ---
    # If amount is over 5000 -> REFER
    if amount is not None and amount > Decimal("5000"):
        reasons.append(REFER_HIGH_VALUE)

    # If reference contains suspicious terms -> REFER
    reference_text = "" if reference_raw is None else str(reference_raw)
    ref_lower = reference_text.lower()
    if any(keyword in ref_lower for keyword in SUSPICIOUS_KEYWORDS):
        reasons.append(REFER_SCAM_KEYWORDS)

    if reasons:
        # At this point, any reasons are risk reasons, so REFER
        return (REFER, reasons)

    return (APPROVE, [])

