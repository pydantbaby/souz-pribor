from typing import Any


class AIAuthenticationError(Exception):
    """Ошибка учётных данных"""

    def __init__(self) -> None:
        super().__init__("AI Provider Authentication Error")


class AIBadRequestError(Exception):
    """Ошибка входных данных для API ИИ-провайдера"""

    def __init__(self, body: object | None, response: str) -> None:
        self.response = response
        self.body: dict[str, Any]

        if isinstance(body, dict):
            self.body = body
        else:
            self.body = {"response_body": body} if body else {}

        super().__init__("Bad Request")


class AIInternalServerError(Exception):
    """Внутрення ошибка ИИ-провайдера"""

    def __init__(self) -> None:
        super().__init__("AI Provider's server error")


class AIConnectionError(Exception):
    """Ошибка соединения при взаимодейстии с API ИИ-провайдера"""

    def __init__(self, message: str) -> None:
        super().__init__(message)