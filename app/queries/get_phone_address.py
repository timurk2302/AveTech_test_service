from fastapi import HTTPException
from app.models.response_models import PhoneAddressResponse
import json
from datetime import datetime
import re
import redis.asyncio as redis


class GetPhoneAddressQuery:
    """Query для получения адреса по телефону"""
    
    @staticmethod
    async def execute(redis_client: redis.Redis, phone: str) -> PhoneAddressResponse:
        """
        Получить адрес по номеру телефона
        
        :param redis_client: redis.Redis
        :param phone: Номер телефона
        :return: PhoneAddressResponse
        :raises HTTPException: 404 если телефон не найден
        """
        # Очищаем номер телефона от нецифровых символов
        cleaned_phone = re.sub(r'\D', '', phone)
        
        # Получаем данные из Redis
        data = await redis_client.get(f"phone:{cleaned_phone}")
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"Телефон {cleaned_phone} не найден"
            )
        
        # Десериализуем данные
        record = json.loads(data)
        
        # Преобразуем строки времени обратно в datetime
        if 'created_at' in record and record['created_at']:
            record['created_at'] = datetime.fromisoformat(record['created_at'])
        if 'updated_at' in record and record['updated_at']:
            record['updated_at'] = datetime.fromisoformat(record['updated_at'])
        
        return PhoneAddressResponse.model_validate(record)