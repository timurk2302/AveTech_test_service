from pydantic import BaseModel, Field, field_validator
import re


class PhoneAddressCreateRequest(BaseModel):
    """Модель запроса для создания связки телефон-адрес"""
    phone: str = Field(..., min_length=10, max_length=15, description="Номер телефона")
    address: str = Field(..., min_length=1, max_length=500, description="Адрес")
    
    @field_validator('phone')
    def validate_phone(cls, v: str) -> str:
        """Валидация номера телефона"""
        # Удаляем все нецифровые символы
        digits = re.sub(r'\D', '', v)
        
        if len(digits) < 10:
            raise ValueError("Номер телефона должен содержать минимум 10 цифр")
        
        # Возвращаем очищенный номер
        return digits
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+79123456789",
                "address": "г. Москва, ул. Тверская, д. 1, кв. 10"
            }
        }


class PhoneAddressUpdateRequest(BaseModel):
    """Модель запроса для обновления адреса"""
    address: str = Field(..., min_length=1, max_length=500, description="Новый адрес")
    
    class Config:
        json_schema_extra = {
            "example": {
                "address": "г. Санкт-Петербург, Невский пр., д. 100, кв. 5"
            }
        }