"""CR-0: tēma "Parki un skvēri" un tēmu saraksts."""

EXPECTED_TOPICS = [
    {"code": "ROADS", "name": "Ceļi un ielas"},
    {"code": "WASTE", "name": "Atkritumi"},
    {"code": "PLANNING", "name": "Teritorijas plānošana"},
    {"code": "PARKS", "name": "Parki un skvēri"},
    {"code": "OTHER", "name": "Cits"},
]


def test_cr0_ac1_topics_list(client):
    response = client.get("/topics")
    assert response.status_code == 200
    assert response.json() == EXPECTED_TOPICS


def test_cr0_ac2_parks_submission_created(client, valid_payload):
    valid_payload["topic"] = "PARKS"
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 201
    stored = client.get(f"/submissions/{response.json()['id']}").json()
    assert stored["topic"] == "PARKS"


def test_cr0_ac3_unknown_topic_rejected(client, valid_payload):
    valid_payload["topic"] = "ZOO"
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert "topic" in [detail["field"] for detail in error["details"]]


def test_cr0_ac4_existing_topics_unchanged(client, valid_payload):
    existing = [
        {"code": "ROADS", "name": "Ceļi un ielas"},
        {"code": "WASTE", "name": "Atkritumi"},
        {"code": "PLANNING", "name": "Teritorijas plānošana"},
        {"code": "OTHER", "name": "Cits"},
    ]
    topics = client.get("/topics").json()
    for topic in existing:
        assert topic in topics
        valid_payload["topic"] = topic["code"]
        assert client.post("/submissions", json=valid_payload).status_code == 201
