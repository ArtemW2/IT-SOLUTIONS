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

    #Проверяем, существуют ли соответствующие экземпляры модели
    def get_model_instance(self, name, model):
        try:
            return model.objects.get(name = name)
        except model.DoesNotExist:
            raise serializers.ValidationError({name: f'{model} "{name}" не существует'})

    #Устанавливаем связь между категорией и подкатегорией
    def get_subcategory_instance(self, subcategory, category):
        try:
            return SubCategory.objects.get(name = subcategory, category = category)
        except:
            raise serializers.ValidationError({'subcategory': f'Подкатегория "{subcategory}" не существует для категории "{category.name}"'})

    #Забираем из словарей только название без ключа
    def parse_data(self, validated_data):
        status_name = validated_data.get('status')
        type_name = validated_data.get('type')
        category_name = validated_data.get('category')
        subcategory_name= validated_data.get('subcategory')

        status_name = status_name.get('name', status_name) if isinstance(status_name, dict) else status_name
        type_name = type_name.get('name', type_name) if isinstance(type_name, dict) else type_name
        category_name = category_name.get('name', category_name) if isinstance(category_name, dict) else category_name
        subcategory_name = subcategory_name.get('name', subcategory_name) if isinstance(subcategory_name, dict) else subcategory_name

        return status_name, type_name, category_name, subcategory_name

    #Получаем значения для полей, являющимися внешними ключами
    def get_instances(self, status_name, type_name, category_name, subcategory_name):
        status = self.get_model_instance(status_name, Status)
        type = self.get_model_instance(type_name, Type)
        category = self.get_model_instance(category_name, Category)
        subcategory = self.get_subcategory_instance(subcategory_name, category)

        return status, type, category, subcategory

    def create(self, validated_data):
        if 'date' not in validated_data:
            validated_data['date'] = timezone.now().date()

        date = validated_data.get('date')
        amount = validated_data.get('amount')
        text = validated_data.get('text')

        status_name, type_name, category_name, subcategory_name = self.parse_data(validated_data)
        status, type, category, subcategory = self.get_instances(status_name, type_name, category_name, subcategory_name)

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
        
        amount = validated_data.get('amount', instance.amount)
        text = validated_data.get('text', instance.text)

        status_name, type_name, category_name, subcategory_name = self.parse_data(validated_data)
        status, type, category, subcategory = self.get_instances(status_name, type_name, category_name, subcategory_name)

        instance.date = date
        instance.status = status
        instance.type = type
        instance.category = category
        instance.subcategory = subcategory
        instance.amount = amount
        instance.text = text
        instance.save()

        return instance
    