import datetime
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema

from items.serializers import ItemAddSerializer, ItemFixSerializer
from items.models import Item, Product
from users.permissions import IsOwnerOrAdmin, IsNotAuthenticated


logger = logging.getLogger('my_log')


class ItemView(generics.CreateAPIView):
    serializer_class = ItemAddSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Item.objects.select_related('product').all()

    @swagger_auto_schema(operation_summary='회원별 아이템 조회',
                         operation_description='회원별 아이템 리스트를 조회합니다', )
    def get(self, request, *args, **kwargs):
        logger.info('get item 진입')
        user = request.user
        qs = self.queryset.filter(user=user).values('id', 'product_id', 'product__name', 'amount', 'unit',
                                                    'created_at', 'expired_at')
        data = [{'id': q['id'],
                 'product_id': q['product_id'],
                 'item_name': q['product__name'],
                 'amount_with_unit': f'{q["amount"]}({q["unit"]})',
                 'created_at': q['created_at'],
                 'expired_at': q['expired_at']} for q in qs]
        return Response(data)

    @swagger_auto_schema(operation_summary='회원별 아이템 등',
                         operation_description='회원별 록신규 아이템을 등록합니다', )
    def post(self, request, *args, **kwargs):
        logger.info('post item 진입')
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        product = get_object_or_404(Product, id=data['product_id'])
        expired_at = data.get('expired_at')

        detail = data.get('detail', '')

        if expired_at is None:
            today = timezone.localdate()
            expire_within = product.expire_within
            expired_at = today + datetime.timedelta(days=expire_within)

        item = Item.objects.create(
            user=user,
            product=product,
            expired_at=expired_at,
            amount=data['amount'],
            unit=data['unit'],
            detail=detail
        )

        return Response({
            'id': item.id,
            'product_id': product.id,
            'item_name': item.product.name,
            'amount_with_unit': f'{item.amount}({item.unit})',
            'expired_at': item.expired_at,
            'detail': detail
        })


class ItemFixView(generics.CreateAPIView):
    serializer_class = ItemFixSerializer
    permission_classes = (IsOwnerOrAdmin,)
    queryset = Item.objects.select_related('product').all()

    @swagger_auto_schema(operation_summary='아이템 수정',
                         operation_description='선택된 아이템을 수정합니다', )
    def patch(self, request, *args, **kwargs):
        logger.info('patch item 진입')

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        expired_at = data.get('expired_at')
        detail = data.get('detail')

        item = Item.objects.get(id=data['id'])
        product = Product.objects.get(id=data['product_id'])
        item.product = product
        item.amount = data['amount']
        item.unit = data['unit']
        if expired_at is not None:
            item.expired_at = expired_at
        if detail is not None:
            item.detail = detail
        item.save()

        return Response({
            'id': item.id,
            'product_id': product.id,
            'item_name': item.product.name,
            'amount_with_unit': f'{item.amount}({item.unit})',
            'expired_at': item.expired_at,
            'detail': detail
        })


class ItemEachView(generics.CreateAPIView):
    serializer_class = ItemFixSerializer
    permission_classes = (IsOwnerOrAdmin,)
    queryset = Item.objects.select_related('product').all()

    @swagger_auto_schema(operation_summary='아이템 삭제',
                         operation_description='선택된 아이템을 삭제합니다', )
    def get(self, request, *args, **kwargs):
        logger.info('get each item 진입')
        user = request.user
        id = kwargs.get('id')
        item = get_object_or_404(Item, id=id)
        if item.user != user:
            return Response({'message': '회원 정보 불일치'})

        return Response({
            'id': item.id,
            'product_id': item.product.id,
            'item_name': item.product.name,
            'amount_with_unit': f'{item.amount}({item.unit})',
            'expired_at': item.expired_at,
            'detail': item.detail
        })

    @swagger_auto_schema(operation_summary='아이템 삭제',
                         operation_description='선택된 아이템을 삭제합니다', )
    def delete(self, request, *args, **kwargs):
        logger.info('delete each item 진입')
        id = kwargs.get('id')
        user = request.user
        item = get_object_or_404(Item, id=id)

        if item.user != user:
            return Response({'message': '회원 정보 불일치'})

        item.delete()
        return Response({'message': '삭제 완료'})
