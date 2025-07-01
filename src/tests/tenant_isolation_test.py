def test_tenant_data_isolation(tenant1_client, tenant2_client, create_contact):

    create_response = create_contact(tenant1_client)
    contact_id = create_response.json()['id']

    get_response1 = tenant1_client.get(f'/api/contacts/{contact_id}')
    assert get_response1.status_code == 200

    get_response2 = tenant2_client.get(f'/api/contacts/{contact_id}')
    assert get_response2.status_code == 404


def test_email_uniqueness_per_tenant(tenant1_client, tenant2_client, create_contact):

    import uuid

    unique_id1 = str(uuid.uuid4())[:8]
    email_tenant1 = f"tenant1-{unique_id1}@example.com"

    unique_id2 = str(uuid.uuid4())[:8]
    email_tenant2 = f"tenant2-{unique_id2}@example.com"

    create_response1 = create_contact(tenant1_client, email=email_tenant1)
    assert create_response1.status_code == 201
    contact1_id = create_response1.json()["id"]

    create_response2 = create_contact(tenant2_client, email=email_tenant2)
    assert create_response2.status_code == 201

    get_response1 = tenant2_client.get(f'/api/contacts/{contact1_id}')
    assert get_response1.status_code == 404


def test_contact_count_isolation(tenant1_client, tenant2_client, create_contact):

    for i in range(3):
        create_contact(
            tenant1_client,
            name=f"Contact {i+1} in Tenant 1",
            email=f"contact{i+1}@tenant1.com"
        )

    create_contact(
        tenant2_client,
        name="Contact 1 in Tenant 2",
        email="contact1@tenant2.com"
    )

    response1 = tenant1_client.get('/api/contacts/')
    data1 = response1.json()
    assert len(data1['items']) >= 3

    response2 = tenant2_client.get('/api/contacts/')
    data2 = response2.json()
    assert len(data2['items']) == 1
