from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def setup_exception_handlers(app: FastAPI) -> None:
    """Оборачивает ошибки в кастомную обработку"""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        missing_fields = []

        # ищем названия непереданных обязательных полей
        for err in exc.errors():
            if err.get("type") == "missing":
                field_name = err.get("loc")[-1]
                missing_fields.append(field_name)

        if missing_fields:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "error",
                    "message": "Не указаны обязательные поля в теле запроса",
                    "missed_fields": missing_fields,
                },
            )

        # для остальных ошибок - стандартный ответ
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exc.errors()},
        )
