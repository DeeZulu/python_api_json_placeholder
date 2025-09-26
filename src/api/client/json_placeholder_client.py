from typing import Dict, Any, List

import requests.exceptions

from requests import Response

class JSONPlaceholderClientError(Exception):
    """Базовое исключение для клиента"""
    pass

class PostNotFoundError(JSONPlaceholderClientError):
    """Пост не найден"""
    pass

class CommentsNotFoundError(JSONPlaceholderClientError):
    """Комментарии не найдены"""
    pass

class JSONPlaceholderClient:
    """Клиент для работы с API https://jsonplaceholder.typicode.com"""

    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com/"
        self.session = requests.Session()  # для reuse connection

    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        """
        Универсальный метод запроса к API
        :param method: Метод запроса
        :param endpoint: Путь внутри API
        :return: Ответ от сервера в виде объекта класса Response
        """
        try:
            url = self.base_url + endpoint.lstrip("/")
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout as e:
            raise JSONPlaceholderClientError("Request timeout") from e
        except requests.exceptions.ConnectionError as e:
            raise JSONPlaceholderClientError("Connection error") from e
        except requests.exceptions.RequestException as e:
            raise JSONPlaceholderClientError(f"Request failed: {e}") from e

    def get_post_by_id(self, post_id: int) -> Dict[str, Any]:
        """
        Возвращает пост по ID
        :param post_id:
        :return: Пост в виде словаря
        """
        try:
            response = self._request("GET", f"/posts/{post_id}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise PostNotFoundError(f"Пост с ID {post_id} не найден") from e
            raise JSONPlaceholderClientError(f"HTTP Error {e.response.status_code}") from e


    def get_posts(self) -> List[Dict[str, Any]]:
        """
        Возвращает список постов
        :return: Список словарей с постами
        """
        return self._request("GET", "/posts").json()

    def get_comments_by_post_id(self, post_id: int) -> List[Dict[str, Any]]:
        """
        Возвращает все комментарии к посту по ID поста
        :param post_id: ID поста
        :return: Список словарей с комментариями
        """
        params = {
            "postId": post_id
        }
        try:
            response = self._request("GET", f"/comments", params=params)
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise CommentsNotFoundError(f"Комментарии к посту {post_id} не найдены") from e
            raise JSONPlaceholderClientError(f"HTTP Error {e.response.status_code}") from e

    def create_post(self, post_params: dict) -> Dict[str, Any]:
        """
        Создаёт пост
        :param post_params: данные поста
        :return: Ответ от сервера в виде объекта класса Response
        """
        return self._request("POST", "/posts", json=post_params).json()

    def edit_post(self, post_id: int, post_params: dict) -> Dict[str, Any]:
        """
        Редактирование поста (PUT)
        :param post_id: ID поста
        :param post_params: Словарь с новыми данными
        :return: Ответ от сервера в виде объекта класса Response
        """
        try:
            response = self._request("PUT", f"/posts/{post_id}", json=post_params)
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise PostNotFoundError(f"Пост с ID {post_id} не найден") from e
            raise JSONPlaceholderClientError(f"HTTP Error {e.response.status_code}") from e

    def partial_edit_post(self, post_id: int, post_params: dict) -> Dict[str, Any]:
        """
        Частичное редактирование поста (PATCH)
        :param post_id: ID поста
        :param post_params: Словарь с новыми данными
        :return: Ответ от сервера в виде объекта класса Response
        """
        try:
            response = self._request("PATCH", f"/posts/{post_id}", json=post_params)
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise PostNotFoundError(f"Пост с ID {post_id} не найден") from e
            raise JSONPlaceholderClientError(f"HTTP Error {e.response.status_code}") from e

    def delete_post(self, post_id: int) -> int:
        """
        Удаление поста
        :param post_id: ID поста
        :return: Ответ от сервера в виде объекта класса Response
        """
        try:
            response = self._request("DELETE", f"/posts/{post_id}")
            return response.status_code
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise PostNotFoundError(f"Пост с ID {post_id} не найден") from e
            raise JSONPlaceholderClientError(f"HTTP Error {e.response.status_code}") from e
