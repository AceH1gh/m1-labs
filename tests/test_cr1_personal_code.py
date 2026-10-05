"""CR-1: personas koda pārbaude iesniegumā."""

import pytest


def post(client, payload, personal_code):
    payload["personalCode"] = personal_code
    return client.post("/submissions", json=payload)


def stored_code(client, response):
    return client.get(f"/submissions/{response.json()['id']}").json()["personalCode"]


def assert_rejected(response, issue):
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert {"field": "personalCode", "issue": issue} in error["details"]


def test_cr1_ac1_eleven_digits_accepted(client, valid_payload):
    response = post(client, valid_payload, "32000000001")
    assert response.status_code == 201
    assert stored_code(client, response) == "32000000001"


def test_cr1_ac2_hyphen_normalised(client, valid_payload):
    response = post(client, valid_payload, "320000-00001")
    assert response.status_code == 201
    assert stored_code(client, response) == "32000000001"


def test_cr1_ac3_spaces_trimmed(client, valid_payload):
    response = post(client, valid_payload, " 32000000001 ")
    assert response.status_code == 201
    assert stored_code(client, response) == "32000000001"


def test_cr1_ac4_ten_digits_rejected(client, valid_payload):
    assert_rejected(post(client, valid_payload, "3200000000"), "INVALID_FORMAT")


def test_cr1_ac5_twelve_digits_rejected(client, valid_payload):
    assert_rejected(post(client, valid_payload, "320000000012"), "INVALID_FORMAT")


def test_cr1_ac6_letter_o_rejected(client, valid_payload):
    assert_rejected(post(client, valid_payload, "32000000O01"), "INVALID_FORMAT")


def test_cr1_ac7_missing_field_required(client, valid_payload):
    del valid_payload["personalCode"]
    response = client.post("/submissions", json=valid_payload)
    assert_rejected(response, "REQUIRED")


def test_cr1_ac8_old_format_accepted(client, valid_payload):
    response = post(client, valid_payload, "311299-21233")
    assert response.status_code == 201
    assert stored_code(client, response) == "31129921233"


def test_cr1_ac9_hyphen_in_wrong_place_rejected(client, valid_payload):
    assert_rejected(post(client, valid_payload, "3200-0000001"), "INVALID_FORMAT")


def test_cr1_ac10_starts_with_00_rejected(client, valid_payload):
    assert_rejected(post(client, valid_payload, "00000000001"), "INVALID_FORMAT")


def test_cr1_ac11_starts_with_33_rejected(client, valid_payload):
    assert_rejected(post(client, valid_payload, "33000000001"), "INVALID_FORMAT")


@pytest.mark.parametrize("personal_code", ["", "   "])
def test_cr1_empty_or_spaces_required(client, valid_payload, personal_code):
    assert_rejected(post(client, valid_payload, personal_code), "REQUIRED")


def test_cr1_error_does_not_repeat_code(client, valid_payload):
    response = post(client, valid_payload, "32000000O01")
    assert "32000000O01" not in response.text
