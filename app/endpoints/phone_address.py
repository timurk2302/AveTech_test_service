from fastapi import APIRouter, status, Query
from typing import Optional
from app.dependecies import RedisDependency
from app.models.request_models import PhoneAddressCreateRequest, PhoneAddressUpdateRequest
from app.models.response_models import PhoneAddressResponse, CreateResponse, ErrorResponse
from app.queries.get_phone_address import GetPhoneAddressQuery
from app.commands.create_phone_address import CreatePhoneAddressCommand
from app.commands.update_phone_address import UpdatePhoneAddressCommand
from app.commands.delete_phone_address import DeletePhoneAddressCommand

router = APIRouter(
    responses={
        404: {"model": ErrorResponse, "description": "Запись не найдена"},
        409: {"model": ErrorResponse, "description": "Конфликт данных"}
    }
)


@router.get(
    path="/{phone}",
    response_model=PhoneAddressResponse,
    summary="Получить адрес по телефону",
    description="Получает сохранённый адрес по номеру телефона из Redis.",
    response_description="Адрес, связанный с указанным номером телефона",
)
async def get_address_by_phone(
    phone: str,
    redis: RedisDependency
)-> PhoneAddressResponse:
    """
    Получить адрес по номеру телефона.
    """
    return await GetPhoneAddressQuery.execute(redis_client=redis, phone=phone)


@router.post(
    path="/",
    response_model=CreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую связку телефон-адрес",
    description="Создаёт новую связку телефон-адрес в Redis.",
    responses={
        201: {"description": "Запись успешно создана"},
        409: {"description": "Телефон уже существует"}
    }
)
async def create_phone_address(
    request: PhoneAddressCreateRequest,
    redis: RedisDependency,
    overwrite: Optional[bool] = Query(
        False,
        description="Перезаписать существующую запись"
    )
)-> CreateResponse:
    """
    Создать новую связку телефон-адрес.
    """
    return await CreatePhoneAddressCommand.execute(redis_client=redis, request=request, overwrite=overwrite)


@router.put(
    path="/{phone}",
    response_model=PhoneAddressResponse,
    summary="Обновить адрес по телефону",
    description="Обновляет адрес для существующего номера телефона.",
    response_description="Обновленные данные"
)
async def update_address(
    phone: str,
    request: PhoneAddressUpdateRequest,
    redis: RedisDependency
)-> PhoneAddressResponse:
    """
    Обновить адрес для указанного телефона.
    """
    return await UpdatePhoneAddressCommand.execute(redis_client=redis, phone=phone, request=request)


@router.delete(
    path="/{phone}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить запись",
    description="Удаляет связку телефон-адрес из Redis.",
    responses={
        204: {"description": "Запись успешно удалена"},
        404: {"description": "Запись не найдена"}
    }
)
async def delete_phone_address(
    phone: str,
    redis: RedisDependency
)-> None:
    """
    Удалить запись по номеру телефона.
    """
    await DeletePhoneAddressCommand.execute(redis_client=redis, phone=phone)