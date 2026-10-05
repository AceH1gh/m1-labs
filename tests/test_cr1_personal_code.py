"""CR-1: personas koda pārbaude (tracker/CR-1.md).

Viena kritēriju tabulas rinda = viens tests (test_cr1_ac<rinda>_...).
Testi test_cr1_clarif_... izriet no sadaļas "Precizējumi".
Kļūdas forma: docs/openapi.yaml, components.schemas.Error un
components.responses.ValidationError.
"""

import logging


def _submit(client, payload, personal_code):
    payload["personalCode"] = personal_code
    return client.post("/submissions", json=payload)


def _stored_code(client, response):
    submission_id = response.json()["id"]
    return client.get(f"/submissions/{submission_id}").json()["personalCode"]


def _assert_issue(response, issue):
    """400 pēc līguma kļūdu shēmas ar personalCode lauka kļūdu `issue`."""
    assert response.status_code == 400
    body = response.json()
    assert set(body) == {"error"}
    error = body["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert isinstance(error["message"], str)
    assert isinstance(error["details"], list)
    for detail in error["details"]:
        assert {"field", "issue"} <= set(detail)
        assert detail["issue"] in {"REQUIRED", "INVALID_FORMAT", "TOO_LONG"}
    assert {"field": "personalCode", "issue": issue} in error["details"]


# --- Pieņemšanas kritēriji (rindas 1-9) ---


def test_cr1_ac1_new_format_accepted(client, valid_payload):
    response = _submit(client, valid_payload, "32000000001")
    assert response.status_code == 201
    assert _stored_code(client, response) == "32000000001"


def test_cr1_ac2_hyphen_normalised(client, valid_payload):
    response = _submit(client, valid_payload, "320000-00001")
    assert response.status_code == 201
    assert _stored_code(client, response) == "32000000001"


def test_cr1_ac3_outer_spaces_removed(client, valid_payload):
    response = _submit(client, valid_payload, " 32000000001 ")
    assert response.status_code == 201
    assert _stored_code(client, response) == "32000000001"


def test_cr1_ac4_10_digits_invalid_format(client, valid_payload):
    _assert_issue(_submit(client, valid_payload, "3200000000"), "INVALID_FORMAT")


def test_cr1_ac5_12_digits_invalid_format(client, valid_payload):
    _assert_issue(_submit(client, valid_payload, "320000000012"), "INVALID_FORMAT")


def test_cr1_ac6_letter_o_invalid_format(client, valid_payload):
    _assert_issue(_submit(client, valid_payload, "32000000O01"), "INVALID_FORMAT")


def test_cr1_ac7_missing_field_required(client, valid_payload):
    del valid_payload["personalCode"]
    _assert_issue(client.post("/submissions", json=valid_payload), "REQUIRED")


def test_cr1_ac8_old_format_accepted(client, valid_payload):
    response = _submit(client, valid_payload, "311299-21233")
    assert response.status_code == 201
    assert _stored_code(client, response) == "31129921233"


def test_cr1_ac9_hyphen_wrong_place_invalid_format(client, valid_payload):
    _assert_issue(_submit(client, valid_payload, "3200-0000001"), "INVALID_FORMAT")


# --- Precizējumi ---


def test_cr1_clarif_empty_string_required(client, valid_payload):
    _assert_issue(_submit(client, valid_payload, ""), "REQUIRED")


def test_cr1_clarif_only_spaces_required(client, valid_payload):
    _assert_issue(_submit(client, valid_payload, "   "), "REQUIRED")


def test_cr1_clarif_error_response_does_not_echo_input(client, valid_payload):
    response = _submit(client, valid_payload, "320000000012")
    assert response.status_code == 400
    assert "320000000012" not in response.text


def test_cr1_clarif_error_log_does_not_echo_input(client, valid_payload, caplog):
    with caplog.at_level(logging.DEBUG):
        response = _submit(client, valid_payload, "320000000012")
    assert response.status_code == 400
    assert "320000000012" not in caplog.text
