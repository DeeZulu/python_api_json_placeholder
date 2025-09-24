import requests
from requests import Response
from typing import Optional


class ApiClient:
    """Базовый API клиент. Поддерживает все запросы для CRUD операций"""

    def __init__(self, base_url):
        """
        :param base_url: Базовый URL API
        """
        self.base_url = base_url

    def get(self, path: str, params: Optional[dict] = None) -> Response:
        """
        GET запрос
        :param params:
        :param path: путь после / в URL
        """
        response = requests.get(self.base_url + path.lstrip("/"), params)
        response.raise_for_status()
        return response

    def post(self, path: str, json: Optional[dict] = None, data: Optional[dict] = None) -> Response:
        """
        POST запрос
        :param path: путь после / в URL
        :param data: :param data: Данные формы (form-data).
        :param json: Данные в формате JSON.
        """
        response = requests.post(self.base_url + path.lstrip("/"), data, json)
        response.raise_for_status()
        return response

    def patch(self, path: str, data: Optional[dict] = None) -> Response:
        """
        PATCH запрос
        :param path: путь после / в URL
        :param data: :param data: Данные формы (form-data).
        """
        response = requests.patch(self.base_url + path.lstrip("/"), data)
        response.raise_for_status()
        return response

    def put(self, path: str, data: Optional[dict] = None) -> Response:
        """
        PUT запрос
        :param path: путь после / в URL
        :param data: :param data: Данные формы (form-data).
        """
        response = requests.put(self.base_url + path.lstrip("/"), data)
        response.raise_for_status()
        return response

    def delete(self, path: str):
        """
        DELETE запрос
        :param path: путь после / в URL
        """
        response = requests.delete(self.base_url + path.lstrip("/"))
        response.raise_for_status()
