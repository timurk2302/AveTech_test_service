from fastapi import HTTPException
from app.models.request_models import PhoneAddressCreateRequest
from app.models.response_models import CreateResponse
import json
from datetime import datetime
from app.config import settings
import redis.asyncio as redis


class CreatePhoneAddressCommand:
    """Command для создания новой связки телефон-адрес"""
    
    @staticmethod
    async def execute(redis_client: redis.Redis, request: PhoneAddressCreateRequest, overwrite: bool = False) -> CreateResponse:
        """
        Создать новую связку телефон-адрес
        
        :param redis_client: redis.Redis
        :param request: PhoneAddressCreateRequest
        :param overwrite: bool
        :return: CreateResponse
        :raises HTTPException: 409 если телефон уже существует и overwrite=False
        """
        # Проверяем существование записи
        existing_data = await redis_client.get(f"phone:{request.phone}")
        
        if existing_data and not overwrite:
            raise HTTPException(
                status_code=409,
                detail=f"Телефон {request.phone} уже существует"
            )
        
        # Подготавливаем данные для сохранения
        now = datetime.now() # опять таки, при работе с базой лучше вызывать внутреннюю функцию для получения времени базы данных
        record = {
            'phone': request.phone,
            'address': request.address,
            'created_at': now.isoformat() if not existing_data else json.loads(existing_data)['created_at'],
            'updated_at': now.isoformat()
        }
        
        # Сохраняем в Redis с TTL
        await redis_client.setex(
            f"phone:{request.phone}",
            settings.redis_ttl,
            json.dumps(record)
        )
        
        return CreateResponse(
            message="Запись успешно создана" if not existing_data else "Запись успешно обновлена",
            phone=request.phone
        )