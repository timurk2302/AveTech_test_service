from fastapi import HTTPException
from app.models.request_models import PhoneAddressUpdateRequest
from app.models.response_models import PhoneAddressResponse
import json
from datetime import datetime
import redis.asyncio as redis
import re
from app.config import settings


class UpdatePhoneAddressCommand:
    """Command для обновления адреса по телефону"""
    
    @staticmethod
    async def execute(redis_client: redis.Redis, phone: str, request: PhoneAddressUpdateRequest) -> PhoneAddressResponse:
        """
        Обновить адрес для указанного телефона
        
        :param redis_client: redis.Redis
        :param phone: Номер телефона
        :param request: PhoneAddressUpdateRequest
        :return: PhoneAddressResponse
        :raises HTTPException: 404 если телефон не найден
        """
        # Очищаем номер телефона
        cleaned_phone = re.sub(r'\D', '', phone)
        
        # Получаем существующие данные
        data = await redis_client.get(f"phone:{cleaned_phone}")
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"Телефон {cleaned_phone} не найден"
            )
        
        # Обновляем данные
        record = json.loads(data)
        record['address'] = request.address
        record['updated_at'] = datetime.now().isoformat()
        
        # Сохраняем обратно
        await redis_client.setex(
            f"phone:{cleaned_phone}",
            settings.redis_ttl,
            json.dumps(record)
        )
        
        # Преобразуем строки времени обратно в datetime
        if 'created_at' in record and record['created_at']:
            record['created_at'] = datetime.fromisoformat(record['created_at'])
        if 'updated_at' in record and record['updated_at']:
            record['updated_at'] = datetime.fromisoformat(record['updated_at'])
        
        return PhoneAddressResponse.model_validate(record)