"""SafeSend Payment Validator tests (starter set).

This file contains a small set of assertions that check your validator logic.

Run with:
  python test_validator.py

If an assertion fails, Python will raise an AssertionError and stop on the first
failure. Use the failure message and the test input to decide what to fix.
"""

from __future__ import annotations

from validator import (
    validate_payment,
    APPROVE,
    REJECT,
    REFER,
    INVALID_AMOUNT_LOW,
    INVALID_AMOUNT_HIGH,
    INVALID_SORT_CODE,
    INVALID_ACCOUNT_NUMBER,
    REFER_HIGH_VALUE,
    REFER_SCAM_KEYWORDS,
)


def _base_payment(**overrides):
    payment = {
        "amount": "100.00",
        "sort_code": "12-34-56",
        "account_number": "12345678",
        "recipient_name": "Test Recipient",
        "reference": "invoice 123",
    }
    payment.update(overrides)
    return payment


def run_tests() -> None:
    # Happy path
    d, reasons = validate_payment(_base_payment())
    assert d == APPROVE
    assert reasons == []

    # Blank reference should not trigger REFER
    d, reasons = validate_payment(_base_payment(reference=""))
    assert d == APPROVE
    assert reasons == []

    # Add more tests as you enhance the validator.
    # For example, add tests for:
    # - amounts below 0.01 and above 25000
    # - invalid sort code formats
    # - invalid account number lengths
    # - risk conditions that should return REFER


if __name__ == "__main__":
    run_tests()
    print("All SafeSend validator tests passed.")

