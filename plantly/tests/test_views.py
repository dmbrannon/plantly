from bs4 import BeautifulSoup
from django import urls
from django_dynamic_fixture import G
import pytest

from journal.models import Plant


@pytest.mark.parametrize('url_name, url_kwargs', [
    ('plant-create', None),
    ('entry-create', {'pk': 1234}),
    ('profile', None)
])
def test_protected_views(client, url_name, url_kwargs):
    """Verify creation and profile views are protected from unauthenticated access"""
    url = urls.reverse(url_name, kwargs=url_kwargs)
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url.startswith(urls.reverse('login'))

@pytest.mark.django_db
def test_view_plants(authenticated_user, client):
    """Tests viewing plants of an authenticated user"""

    # Make some plants associated with the authenticated user
    G(Plant,
      owner=authenticated_user)
    G(Plant,
      owner=authenticated_user)

    # Make some plants for other users to help ensure the
    # plant page is only showing the plants of the authenticated
    # user
    G(Plant)
    G(Plant)

    # Render the plant page for the authenticated user
    show_memes_url = urls.reverse('journal-home')
    resp = client.get(show_memes_url)

    soup = BeautifulSoup(resp.content, 'html.parser')
    assert resp.status_code == 200
    assert len(soup.select('.plant-card')) == 2

@pytest.mark.django_db
def test_view_plants_none_created(authenticated_user, client):
    """Tests viewing plants of an authenticated user when no plants have been created"""

    # Render the home page for the authenticated user
    show_plants_url = urls.reverse('journal-home')
    resp = client.get(show_plants_url)

    soup = BeautifulSoup(resp.content, 'html.parser')
    assert resp.status_code == 200
    assert not soup.select('.plant-card')
    assert b'This is the front page of your new journal.' in resp.content