from django.utils import timezone
from rest_framework import serializers
from .models import Category, SubCategory, Status, Type, Transaction


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class SubCategorySerializer(serializers.ModelSerializer):

    category = serializers.CharField(source='category.name')

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']

    def create(self, validated_data):
        name = validated_data.get('name')
        category = validated_data.get('category')

        try:
            category = Category.objects.get(name=category['name'])
        except Category.DoesNotExist:
            raise serializers.ValidationError({
                'category': f'Категория "{category["name"]}" не существует'
            })

        subcategory = SubCategory.objects.create(
            name=name,
            category=category
        )

        return subcategory


class TransactionDetailSerializer(serializers.ModelSerializer):

    status = serializers.CharField(source='status.name')
    type = serializers.CharField(source='type.name')
    category = serializers.CharField(source='category.name')
    subcategory = serializers.CharField(source='subcategory.name')

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'status', 'type', 'category', 'subcategory', 'amount', 'text']
        read_only_fields = ('id', )

    def create(self, validated_data):
        if 'date' not in validated_data:
            validated_data['date'] = timezone.now().date()
        date = validated_data.get('date')
        status_data = validated_data.get('status')
        type_data = validated_data.get('type')
        category_data = validated_data.get('category')
        subcategory_data = validated_data.get('subcategory')
        amount = validated_data.get('amount')
        text = validated_data.get('text')

        status_name = status_data.get('name', status_data) if isinstance(status_data, dict) else status_data
        type_name = type_data.get('name', type_data) if isinstance(type_data, dict) else type_data
        category_name = category_data.get('name', category_data) if isinstance(category_data, dict) else category_data
        subcategory_name = subcategory_data.get('name', subcategory_data) if isinstance(subcategory_data, dict) else subcategory_data

        try:
            status = Status.objects.get(name=status_name)
            type = Type.objects.get(name=type_name)
            category = Category.objects.get(name=category_name)
        except Status.DoesNotExist:
            raise serializers.ValidationError({
                'status': f'Статус "{status_name}" не существует'
            })
        except Type.DoesNotExist:
            raise serializers.ValidationError({
                'type': f'Тип "{type_name}" не существует'
            })
        except Category.DoesNotExist:
            raise serializers.ValidationError({
                'category': f'Категория "{category_name}" не существует'
            })

        try:
            subcategory = SubCategory.objects.get(name=subcategory_name, category=category)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({
                'subcategory': f'Подкатегория "{subcategory_name}" не существует для категории "{category_name}"'
            })

        transaction = Transaction.objects.create(
            date=date,
            status=status,
            type=type,
            category=category,
            subcategory=subcategory,
            amount=amount,
            text=text
        )

        return transaction
    
    def update(self, instance, validated_data):
        date = validated_data.get('date', instance.date)
        status_data = validated_data.get('status', instance.status)
        type_data = validated_data.get('type', instance.type)
        category_data = validated_data.get('category', instance.category)
        subcategory_data = validated_data.get('subcategory', instance.subcategory)
        amount = validated_data.get('amount', instance.amount)
        text = validated_data.get('text', instance.text)

        status_name = status_data.get('name', status_data) if isinstance(status_data, dict) else status_data
        type_name = type_data.get('name', type_data) if isinstance(type_data, dict) else type_data
        category_name = category_data.get('name', category_data) if isinstance(category_data, dict) else category_data
        subcategory_name = subcategory_data.get('name', subcategory_data) if isinstance(subcategory_data, dict) else subcategory_data

        try:
            status = Status.objects.get(name=status_name)
            type = Type.objects.get(name=type_name)
            category = Category.objects.get(name=category_name)
        except Status.DoesNotExist:
            raise serializers.ValidationError({
                'status': f'Статус "{status_name}" не существует'
            })
        except Type.DoesNotExist:
            raise serializers.ValidationError({
                'type': f'Тип "{type_name}" не существует'
            })
        except Category.DoesNotExist:
            raise serializers.ValidationError({
                'category': f'Категория "{category_name}" не существует'
            })

        try:
            subcategory = SubCategory.objects.get(name=subcategory_name, category=category)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({
                'subcategory': f'Подкатегория "{subcategory_name}" не существует для категории "{category_name}"'
            })

        instance.date = date
        instance.status = status
        instance.type = type
        instance.category = category
        instance.subcategory = subcategory
        instance.amount = amount
        instance.text = text
        instance.save()

        return instance
    