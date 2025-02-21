import uuid
import time
import datetime

from api.v1.payment.payme.utils.get_params import get_params
from api.v1.payment.payme.models import MerchatTransactionsModel, Order
from api.v1.payment.payme.errors.exceptions import TooManyRequests
from api.v1.payment.payme.serializers import MerchatTransactionsModelSerializer


class CreateTransaction:
    def __call__(self, params: dict) -> dict:
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get("order_id")

        try:
            transaction = MerchatTransactionsModel.objects.filter(
                order_id=order_id
            ).last()

            if transaction is not None:
                if transaction._id != serializer.validated_data.get("_id"):
                    raise TooManyRequests()

        except TooManyRequests:
            raise TooManyRequests()

        if transaction is None:
            transaction, _ = \
                MerchatTransactionsModel.objects.get_or_create(
                    _id=serializer.validated_data.get('_id'),
                    order_id=serializer.validated_data.get('order_id'),
                    transaction_id=uuid.uuid4(),
                    amount=serializer.validated_data.get('amount'),
                    created_at_ms=int(time.time() * 1000),
                )

        if transaction:
            order = Order.objects.select_related('bron').filter(id=serializer.validated_data.get('order_id')).first()
            order.status = 1,
            order.save()

            response: dict = {
                "result": {
                    "create_time": int(transaction.created_at_ms),
                    "transaction": transaction.transaction_id,
                    "state": int(transaction.state),
                }
            }

        return response

    @staticmethod
    def _convert_ms_to_datetime(time_ms: str) -> int:
        """Use this format to convert from time ms to datetime format.
        """
        readable_datetime = datetime.datetime.fromtimestamp(time_ms / 1000)

        return readable_datetime
