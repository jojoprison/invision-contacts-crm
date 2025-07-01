import json


def test_create_contact_validation(tenant1_client):

    invalid_data = {
        'email': "test@example.com",
        'phone': "+79991234567"
    }
    
    response = tenant1_client.post(
        '/api/contacts/',
        json.dumps(invalid_data),
        content_type='application/json'
    )

    assert response.status_code in [400, 422]

    data = response.json()
    assert 'detail' in data or 'message' in data


def test_create_contact_with_invalid_email(tenant1_client):

    invalid_data = {
        'name': "Test Contact",
        # incorrect
        'email': "invalid-email",
        'phone': "+79991234567"
    }
    
    response = tenant1_client.post(
        '/api/contacts/',
        json.dumps(invalid_data),
        content_type='application/json'
    )

    assert response.status_code in [400, 422]


def test_get_nonexistent_contact(tenant1_client):

    nonexistent_id = "00000000-0000-0000-0000-000000000000"
    response = tenant1_client.get(f'/api/contacts/{nonexistent_id}')

    assert response.status_code == 404


def test_update_nonexistent_contact(tenant1_client):

    nonexistent_id = "00000000-0000-0000-0000-000000000000"
    
    update_data = {
        'name': "Updated Contact",
        'email': "updated@example.com",
        'phone': "+79991112233"
    }
    
    response = tenant1_client.put(
        f'/api/contacts/{nonexistent_id}',
        json.dumps(update_data),
        content_type='application/json'
    )

    assert response.status_code == 404
