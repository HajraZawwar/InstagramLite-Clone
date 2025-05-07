def test_signup(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200
   

def test_login(client):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200