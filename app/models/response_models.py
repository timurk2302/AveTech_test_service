from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class PhoneAddressResponse(BaseModel):
    """Модель ответа с данными о связке телефон-адрес"""
    phone: str = Field(..., description="Номер телефона")
    address: str = Field(..., description="Адрес")
    created_at: Optional[datetime] = Field(None, description="Время создания")
    updated_at: Optional[datetime] = Field(None, description="Время обновления")
    # Обычно для временных меток хранящихся в базе,
    # я для created_at задаю server_default=func.now() в моделях SQLAlchemy,
    # а для updated_at зашиваю вызов func.now() в базовом классе методов для работы с таблицами,
    # но т.к. пример на редисе, придетется управлять временем вручную
    
    model_config = ConfigDict(from_attributes=True) # для использования model_validate 


class CreateResponse(BaseModel):
    """Модель ответа при создании записи"""
    message: str = Field(..., description="Сообщение об успешном создании")
    phone: str = Field(..., description="Номер телефона")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Запись успешно создана",
                "phone": "79123456789"
            }
        }


class ErrorResponse(BaseModel):
    """Модель ответа с ошибкой"""
    detail: str = Field(..., description="Описание ошибки")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Телефон не найден"
            }
        }