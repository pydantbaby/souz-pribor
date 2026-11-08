import logging

from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

from src.exceptions import (
    AIAuthenticationError,
    AIBadRequestError,
    AIConnectionError,
    AIInternalServerError,
)
from src.presentation.dependencies import AIClientDep
from src.presentation.schemas import Item

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ai"])

log_prefix = "Error while working with AI Provider:"


@router.post("/item/card", status_code=200)
async def generate_item_card(item: Item, client: AIClientDep) -> PlainTextResponse:
    """Обработчик, создающий черновик карточки товара

    Args:
        item (Item): Объект товара, спаршенный из входных данных
        client (ClientDep): ИИ-клиент

    Returns:
        PlainTextResponse: Текст черновика карточки товара
    """

    try:
        response = await client.request(item.model_dump_json())
    except AIConnectionError as e:
        logger.error(f"{log_prefix} {e}")
        return PlainTextResponse(
            content=str(e), status_code=status.HTTP_502_BAD_GATEWAY
        )
    except AIBadRequestError as e:
        logger.error(f"{log_prefix} {e}.\nServer responded with {e.body}\n{e.response}")
        return PlainTextResponse(
            content=str(e), status_code=status.HTTP_400_BAD_REQUEST
        )
    except AIInternalServerError as e:
        logger.error(f"{log_prefix} {e}")
        return PlainTextResponse(
            content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except AIAuthenticationError as e:
        logger.error(f"{log_prefix} {e}")
        return PlainTextResponse(
            content=str(e), status_code=status.HTTP_401_UNAUTHORIZED
        )

    return PlainTextResponse(content=response)
