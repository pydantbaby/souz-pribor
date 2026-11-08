from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(examples=["Манометр показывающий DM 02"])
    manufacturer: str = Field(examples=["Сургутский Дом Бракосочетаний"])
    specs: dict[str, str] = Field(
        examples=[
            {
                "диапазон измерений": "0–1,6 МПа",
                "класс точности": "1,5",
                "присоединение": "G1/2",
                "диаметр корпуса": "100 мм",
            }
        ]
    )
    description: str = Field(
        examples=["Прибор предназначен для измерения избыточного давления..."]
    )
