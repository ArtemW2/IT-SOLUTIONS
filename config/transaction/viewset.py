from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .filters import TransactionFilter
from .models import Category, SubCategory, Status, Type, Transaction
from .serializers import TransactionDetailSerializer, StatusSerializer, TypeSerializer, CategorySerializer, SubCategorySerializer


"""Реализация REST API"""


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class TransactionViewSet(viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    queryset = Transaction.objects.all()
    serializer_class = TransactionDetailSerializer
    
    #Получение списка всех записей
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        filtered_queryset = self.filter_queryset(queryset)
        serializer = TransactionDetailSerializer(filtered_queryset, many = True)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        transaction = Transaction.objects.get(pk = pk)
        serializer = TransactionDetailSerializer(transaction)

        return Response(serializer.data)

    #Создание записи
    def create(self, request):
        serializer = TransactionDetailSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response({'message': "Запись создана"}, status = status.HTTP_201_CREATED)
    
    #Обновление записи
    def update(self, request, pk):
        transaction = Transaction.objects.get(pk = pk)
        serializer = TransactionDetailSerializer(transaction, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response({'message': "Запись обновлена"}, status = status.HTTP_200_OK)

    def partial_update(self, request, pk):
        transaction = Transaction.objects.get(pk = pk)
        serializer = TransactionDetailSerializer(transaction, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response({'message': "Запись частично обновлена"}, status = status.HTTP_200_OK)

    #Удаление записи
    def destroy(self, request, pk):
        transaction = Transaction.objects.get(pk = pk)
        transaction.delete()
        
        return Response({'message': "Запись удалена"}, status = status.HTTP_204_NO_CONTENT)
