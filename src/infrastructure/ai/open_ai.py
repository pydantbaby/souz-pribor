from openai import (
    APIConnectionError,
    AsyncOpenAI,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
)
from openai.types.chat import ChatCompletionSystemMessageParam

from src.exceptions import (
    AIAuthenticationError,
    AIBadRequestError,
    AIConnectionError,
    AIInternalServerError,
)


class OpenAIClient:
    """
    Клиент для взаиодействия с ИИ-провайдером при помощи OpenAI API.
    Реализована stateless версия, так как многие провайдеры ещё не перешли на Responses API.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str,
        system_prompt: str,
        timeout: float,
    ) -> None:
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        self.model = model
        self.system_prompt: ChatCompletionSystemMessageParam = {
            "role": "system",
            "content": system_prompt,
        }

    async def request(self, message: str) -> str:
        """Выполнение запроса к ИИ

        Args:
            message (str): Сообщение клиента

        Raises:
            AIConnectionError: Ошибки соединения
            AIBadRequestError: Ошибками в форме запроса
            AIInternalServerError: Ошибки ИИ-провайдера
            AIAuthenticationError: Ошибки аутентификации

        Returns:
            str: Ответное сообщение модели
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[self.system_prompt, {"role": "user", "content": message}],
            )
        except APIConnectionError as e:
            raise AIConnectionError(e.message) from e
        except BadRequestError as e:
            raise AIBadRequestError(body=e.body, response=e.response.text) from e
        except InternalServerError as e:
            raise AIInternalServerError() from e
        except AuthenticationError as e:
            raise AIAuthenticationError() from e

        ai_response = str(response.choices[0].message.content)

        return ai_response
