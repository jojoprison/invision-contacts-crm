import json


def test_create_contact(tenant1_client, create_contact):

    response = create_contact(tenant1_client)

    assert response.status_code == 201

    data = response.json()
    assert 'id' in data
    assert data['name'] == "Test Contact"
    assert data['email'] == "test@example.com"
    assert data['phone'] == "+79991234567"


def test_get_contact_list(tenant1_client, create_contact):

    create_contact(tenant1_client, name="Contact 1", email="contact1@example.com")
    create_contact(tenant1_client, name="Contact 2", email="contact2@example.com")

    response = tenant1_client.get('/api/contacts/')

    assert response.status_code == 200

    data = response.json()
    assert 'items' in data
    assert len(data['items']) >= 2


def test_get_contact_by_id(tenant1_client, create_contact):

    create_response = create_contact(tenant1_client)
    contact_id = create_response.json()['id']

    response = tenant1_client.get(f'/api/contacts/{contact_id}')

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == contact_id
    assert data['name'] == "Test Contact"
    assert data['email'] == "test@example.com"


def test_update_contact(tenant1_client, create_contact):

    create_response = create_contact(tenant1_client)
    contact_id = create_response.json()['id']

    update_data = {
        'name': "Updated Contact",
        'email': "updated@example.com",
        'phone': "+79991112233"
    }
    
    response = tenant1_client.put(
        f'/api/contacts/{contact_id}', 
        json.dumps(update_data),
        content_type='application/json'
    )

    assert response.status_code == 200

    data = response.json()
    assert data['name'] == "Updated Contact"
    assert data['email'] == "updated@example.com"
    assert data['phone'] == "+79991112233"


def test_delete_contact(tenant1_client, create_contact):

    create_response = create_contact(tenant1_client)
    contact_id = create_response.json()['id']

    response = tenant1_client.delete(f'/api/contacts/{contact_id}')

    assert response.status_code == 204

    get_response = tenant1_client.get(f'/api/contacts/{contact_id}')
    assert get_response.status_code == 404


def test_filter_contacts_by_email(tenant1_client, create_contact):

    create_contact(tenant1_client, name="Contact 1", email="test1@example.com")
    create_contact(tenant1_client, name="Contact 2", email="test2@example.com")
    create_contact(tenant1_client, name="Contact 3", email="other@example.com")

    response = tenant1_client.get('/api/contacts/?email=test')

    assert response.status_code == 200

    data = response.json()
    assert len(data['items']) == 2
