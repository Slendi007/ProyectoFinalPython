from typing import Annotated

from fastapi import APIRouter, Depends, status

from proyecto_final.api.dependencies import (
    get_current_user,
    get_uow,
)
from proyecto_final.api.schemas import (
    MessageResponse,
    OrderCreate,
    OrderResponse,
)
from proyecto_final.application.dtos import (
    CreateOrderCommand,
    CreateOrderItemData,
)
from proyecto_final.application.use_cases import (
    CreateOrder,
    DeleteOrder,
    GetOrder,
    ListOrders,
)
from proyecto_final.infrastructure.notifications.memory import (
    MemoryNotificationAdapter,
)
from proyecto_final.infrastructure.unit_of_work import (
    SQLAlchemyUnitOfWork,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


UoWDependency = Annotated[
    SQLAlchemyUnitOfWork,
    Depends(get_uow),
]


CurrentUser = Annotated[
    str,
    Depends(get_current_user),
]


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderCreate,
    uow: UoWDependency,
    _current_user: CurrentUser,
) -> OrderResponse:
    notification = MemoryNotificationAdapter()

    use_case = CreateOrder(
        uow=uow,
        notification=notification,
    )

    command = CreateOrderCommand(
        order_id=data.id,
        customer=data.customer,
        items=[
            CreateOrderItemData(
                product=item.product,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in data.items
        ],
    )

    order = use_case.execute(command)

    return OrderResponse.model_validate(order)


@router.get(
    "",
    response_model=list[OrderResponse],
)
def list_orders(
    uow: UoWDependency,
    _current_user: CurrentUser,
) -> list[OrderResponse]:
    use_case = ListOrders(
        repository=uow.orders,
    )

    orders = use_case.execute()

    return [OrderResponse.model_validate(order) for order in orders]


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    uow: UoWDependency,
    _current_user: CurrentUser,
) -> OrderResponse:
    use_case = GetOrder(
        repository=uow.orders,
    )

    order = use_case.execute(order_id)

    return OrderResponse.model_validate(order)


@router.delete(
    "/{order_id}",
    response_model=MessageResponse,
)
def delete_order(
    order_id: int,
    uow: UoWDependency,
    _current_user: CurrentUser,
) -> MessageResponse:
    use_case = DeleteOrder(uow)

    use_case.execute(order_id)

    return MessageResponse(
        message=f"Orden {order_id} eliminada",
    )
