from rest_framework import serializers, exceptions
from django.shortcuts import get_object_or_404
from items.models import Item, Product


class ItemAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    expired_at = serializers.DateField(required=False)
    detail = serializers.CharField(required=False)
    amount = serializers.IntegerField()
    unit = serializers.CharField()


class ItemFixSerializer(ItemAddSerializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        user = self.context['request'].user

        product = get_object_or_404(Product, id=attrs.get('product_id'))
        item = get_object_or_404(Item, id=attrs.get('id'))
        if item.user != user:
            raise serializers.ValidationError(
                {'id': '해당 아이템을 찾을 수 없습니다'}
            )

        if attrs.get('amount') < 0:
            raise serializers.ValidationError(
                {'amount': '0보다 작게 변경할 수 없습니다'}
            )
        return attrs

    def create(self, validated_data):
        raise NotImplementedError
