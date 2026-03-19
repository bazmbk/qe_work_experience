"""
SafeSend Payment Validator tests (solved version).

Run with:
  python test_validator_solved.py
"""

from __future__ import annotations

from validator_solved import (
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

    # Amount boundary tests
    d, reasons = validate_payment(_base_payment(amount="0.00"))
    assert d == REJECT
    assert reasons == [INVALID_AMOUNT_LOW]

    d, reasons = validate_payment(_base_payment(amount="0.01"))
    assert d == APPROVE
    assert reasons == []

    d, reasons = validate_payment(_base_payment(amount="25000"))
    assert d == REFER
    assert reasons == [REFER_HIGH_VALUE]

    d, reasons = validate_payment(_base_payment(amount="25000.01"))
    assert d == REJECT
    assert reasons == [INVALID_AMOUNT_HIGH]

    # Sort code format/normalisation tests
    d, reasons = validate_payment(_base_payment(sort_code="12-34-56"))
    assert d == APPROVE
    assert reasons == []

    d, reasons = validate_payment(_base_payment(sort_code="12 34 56"))
    assert d == APPROVE
    assert reasons == []

    d, reasons = validate_payment(_base_payment(sort_code="12345"))  # 5 digits
    assert d == REJECT
    assert reasons == [INVALID_SORT_CODE]

    # Account number length tests
    d, reasons = validate_payment(_base_payment(account_number="1234567"))  # 7 digits
    assert d == REJECT
    assert reasons == [INVALID_ACCOUNT_NUMBER]

    d, reasons = validate_payment(_base_payment(account_number="123456789"))  # 9 digits
    assert d == REJECT
    assert reasons == [INVALID_ACCOUNT_NUMBER]

    # Risk gates: high value vs threshold edge
    d, reasons = validate_payment(_base_payment(amount="5000.00"))
    assert d == APPROVE
    assert reasons == []

    d, reasons = validate_payment(_base_payment(amount="5000.01"))
    assert d == REFER
    assert reasons == [REFER_HIGH_VALUE]

    # Risk gates: scam keywords (case-insensitive)
    d, reasons = validate_payment(_base_payment(reference="Urgent payment required"))
    assert d == REFER
    assert reasons == [REFER_SCAM_KEYWORDS]

    # Risk gates: multiple risk triggers -> REFER with BOTH reasons
    d, reasons = validate_payment(_base_payment(amount="6000.00", reference="crypto transfer"))
    assert d == REFER
    assert reasons == [REFER_HIGH_VALUE, REFER_SCAM_KEYWORDS]

    # Mixed invalid inputs: reasons should include functional reasons in order
    d, reasons = validate_payment(_base_payment(amount="0.00", sort_code="12345"))
    assert d == REJECT
    assert reasons == [INVALID_AMOUNT_LOW, INVALID_SORT_CODE]

    # Blank reference should not trigger REFER
    d, reasons = validate_payment(_base_payment(reference=""))
    assert d == APPROVE
    assert reasons == []


if __name__ == "__main__":
    run_tests()
    print("All SafeSend validator tests passed.")

