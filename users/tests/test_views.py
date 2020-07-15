from django import urls
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django_dynamic_fixture import G
import pytest

@pytest.mark.parametrize('view_name', ['register', 'login', 'journal-about'])
def test_public_views(view_name, client):
    """
    Verify that the registration and login views are publicly accessible
    """
    url = urls.reverse(view_name)
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_login_and_logout(client):
    """Tests logging in and logging out"""
    # Create a fake user
    user = G(User, username='my_username')
    user.set_password('my_password123')
    user.save()

    login_url = urls.reverse('login')
    resp = client.post(login_url, {
        'username': 'my_username',
        'password': 'my_password123'
    })

    # The login url should redirect to the home page
    assert resp.status_code == 302
    assert resp.url == urls.reverse('journal-home')

    # Logged in users have a session created for them
    assert Session.objects.count() == 1

    # Log out the user
    logout_url = urls.reverse('logout')
    resp = client.get(logout_url)

    # The logout view shows a successful logout message with no redirect
    assert resp.status_code == 200
    assert resp.template_name[0] == 'users/logout.html'

    # There should be no more sessions left after logging out
    assert not Session.objects.exists()