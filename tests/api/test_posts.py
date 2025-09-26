import pytest
import json

from src.api.models import Post, Comment


def test_get_posts_returns_posts(client):
    response = client.get_posts()
    assert len(response) > 0, "метод get_posts не вернул ни одного поста"
    for post in response:
        Post(**post)


@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post_by_id_returns_correct_post(client, post_id):
    response = client.get_post_by_id(post_id)
    assert response.get("id") == post_id, f"Неправильный ID поста {response.get('id')}, ожидался: {post_id}"
    Post(**response)


@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_comments_by_post_id(client, post_id):
    response = client.get_comments_by_post_id(5)
    assert len(response) > 0, "метод get_comments_by_post_id не вернул ни одного поста"
    for comment in response:
        Comment(**comment)


@pytest.mark.parametrize("post_params", [
    ("First time at Elbrus", "That is gonna be fantastic", 5),
    ("First time at Kazbek", "Fantastic as well", 5)
], indirect=True)
def test_new_post_can_be_created(client, post_params):
    params = {
        "title": post_params["title"],
        "body": post_params["body"],
        "userId": post_params["userId"]
    }
    response = client.create_post(params)
    Post(**json.loads(response.text))
