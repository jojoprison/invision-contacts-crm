def test_missing_schema_header(no_schema_client):

    response = no_schema_client.get('/api/contacts/')

    assert response.status_code == 400


def test_invalid_schema_header(invalid_schema_client):

    response = invalid_schema_client.get('/api/contacts/')

    assert response.status_code == 404


def test_schema_switching(tenant1_client, tenant2_client):

    response1 = tenant1_client.get('/api/contacts/')
    assert response1.status_code == 200

    response2 = tenant2_client.get('/api/contacts/')
    assert response2.status_code == 200
