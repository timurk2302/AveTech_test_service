from fastapi import HTTPException
import redis.asyncio as redis
import re


class DeletePhoneAddressCommand:
    """Command для удаления связки телефон-адрес"""
    
    @staticmethod
    async def execute(redis_client: redis.Redis, phone: str) -> None:
        """
        Удалить запись по номеру телефона
        
        :param redis_client: redis.Redis
        :param phone: Номер телефона
        :return: None
        :raises HTTPException: 404 если телефон не найден
        """
        # Очищаем номер телефона
        cleaned_phone = re.sub(r'\D', '', phone)
        
        # Проверяем существование
        exists = await redis_client.exists(f"phone:{cleaned_phone}")
        
        if not exists:
            raise HTTPException(
                status_code=404,
                detail=f"Телефон {cleaned_phone} не найден"
            )
        
        # Удаляем запись
        await redis_client.delete(f"phone:{cleaned_phone}")