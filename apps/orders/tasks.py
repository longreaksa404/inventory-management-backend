from celery import shared_task
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=10,
    retry_kwargs={'max_retries': 3},
    retry_jitter=True,
)
def process_sales_order_shipping(self, order_id, user_id):
    from apps.orders.models import SaleOrder, OrderStatusHistory
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        with transaction.atomic():
            order = (
                SaleOrder.objects
                .select_for_update()
                .select_related("warehouse", "customer")
                .get(id=order_id)
            )

            if order.status != "confirmed":
                print(f"⚠️ Order {order.id} already processed or invalid state: {order.status}")
                return "already_processed"

            old_status = order.status

            order.ship()

            OrderStatusHistory.objects.create(
                order_type="sale",
                order_id=order.id,
                old_status=old_status,
                new_status=order.status,
                changed_by_id=user_id,
                changed_at=timezone.now(),
            )

            print(f"✅ Sales order {order.id} shipped successfully")

            return "shipped"

    except SaleOrder.DoesNotExist:
        print(f"❌ Order {order_id} does not exist")
        return "not_found"

    except ValidationError as e:
        print(f"❌ Shipping failed for order {order_id}: {e}")

        with transaction.atomic():
            try:
                order = SaleOrder.objects.select_for_update().get(id=order_id)
                order.status = "cancelled"
                order.save(update_fields=["status"])
            except Exception:
                pass

        raise

    except Exception as e:
        print(f"⚠️ Temporary error shipping order {order_id}, retrying: {e}")
        raise


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def process_purchase_order_receiving(self, order_id, user_id):
    from apps.orders.models import PurchaseOrder, OrderStatusHistory
    from apps.inventory.models import Product
    from apps.accounts.models import CustomUser

    with transaction.atomic():
        order = (
            PurchaseOrder.objects
            .select_for_update()
            .select_related("supplier", "warehouse")
            .get(id=order_id)
        )

        if order.status != "confirmed":
            return

        user = CustomUser.objects.get(id=user_id)

        for item in order.items.select_related("product"):
            product = Product.objects.select_for_update().get(id=item.product_id)
            product.quantity += item.quantity
            product.save(update_fields=["quantity"])

            item.line_status = "received"
            item.save(update_fields=["line_status"])

        old_status = order.status
        order.status = "received"
        order.save(update_fields=["status"])

        OrderStatusHistory.objects.create(
            order_type="purchase",
            order_id=order.id,
            old_status=old_status,
            new_status="received",
            changed_by=user,
        )
