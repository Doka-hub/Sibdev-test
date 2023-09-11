from apps.accounts.models import CustomUser


def test_register(db, register_url, anon_client):
    register_data = {
        'email': 'unique@mail.ru',
        'password': '123test123',
        'password2': '123test123',
    }
    assert CustomUser.objects.filter(email=register_data['email']).exists() is False

    response = anon_client.post(register_url, data=register_data)

    assert response.status_code == 201
    assert CustomUser.objects.filter(email=register_data['email']).exists() is True


def test_login(db, login_url, user, anon_client):
    login_data = {
        'email': user.email,
        'password': '123test123',
    }
    response = anon_client.post(login_url, data=login_data)

    assert response.status_code == 200
    assert response.json().get('access') is not None
