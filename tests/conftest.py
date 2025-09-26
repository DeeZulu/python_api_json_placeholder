from pytest import fixture

from src.api.clients.json_placeholder_client import JSONPlaceholderClient


@fixture(scope="function")
def client() -> JSONPlaceholderClient:
    """API клиент для сервиса JSONPlaceholder"""
    return JSONPlaceholderClient()


@fixture(scope="function")
def post_params(request):
    """Данные для нового поста"""
    title, body, user_id = request.param
    return {
        "title": title,
        "body": body,
        "userId": user_id
    }