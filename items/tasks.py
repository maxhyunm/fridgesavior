import logging
import datetime
from django.utils import timezone
from celery import shared_task
from fridgeback.celery import app
from items.models import Item
from users.models import User

logger = logging.getLogger('my_log')


@app.task()
def check_expire_dates(target_day=None):
    logger.info('check expire dates 진입')
    if target_day is None:
        today = timezone.localdate()
        target_day = today + datetime.timedelta(days=1)
    expire_items = Item.objects.select_related('user', 'product').\
        filter(expired_at=target_day).values('id', 'user_id', 'product_id', 'product__name',
                                             'amount', 'unit')
    expire_per_user = {}

    for ei in expire_items:
        if ei['user_id'] not in expire_per_user:
            expire_per_user[ei['user_id']] = []
        each = f'{ei["product__name"]} {ei["amount"]}({ei["unit"]})'
        expire_per_user[ei['user_id']].append(each)

    # TODO : 메시지 보낼 거 아니면 알림 생성(앱) -> 메시지 발송할 거면 핸드폰번호 받아야 함


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def printing():
    print("just printing")
