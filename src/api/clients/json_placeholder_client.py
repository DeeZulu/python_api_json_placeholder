from src.api.clients.api_client import ApiClient
from requests import Response


class JSONPlaceholderClient(ApiClient):
    """Клиент для работы с API https://jsonplaceholder.typicode.com"""
    BASE_URL = "https://jsonplaceholder.typicode.com/"

    def __init__(self):
        super().__init__(self.BASE_URL)

    def get_posts(self, params=None) -> list:
        """
        Возвращает список постов
        :param params: список параметров
        """
        return self.get("/posts", params).json()

    def get_post_by_id(self, post_id: int) -> dict:
        """
        Возвращает пост по его ID
        :param post_id: ID поста
        """
        return self.get(f"/posts/{post_id}").json()

    def get_comments_by_post_id(self, post_id: int) -> list:
        """
        Возвращает все комментарии к посту по ID поста
        :param post_id: ID поста
        """
        return self.get(f"/comments?postId={post_id}").json()

    def create_post(self, post_params: dict) -> Response:
        """
        Создаёт пост
        :param post_params: данные поста
        """
        return self.post("/posts", json=post_params)
