from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

import datetime

class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Статус')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Тип')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Category(models.Model):
    name = models.CharField(max_length = 100, verbose_name = 'Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    

class SubCategory(models.Model):
    name = models.CharField(max_length = 100, verbose_name = 'Подкатегория')
    category = models.ForeignKey(Category, on_delete = models.CASCADE,verbose_name = 'Категория', related_name = 'subcategories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Transaction(models.Model):
    date = models.DateField(default = datetime.date.today, verbose_name = 'Дата записи')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name = 'Статус')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name = 'Тип')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = 'Категория')
    subcategory = models.ForeignKey(SubCategory, on_delete = models.CASCADE, verbose_name = 'Подкатегория')
    amount = models.DecimalField(blank = False, max_digits = 7, decimal_places = 2, default = 0.00, validators = [MinValueValidator(1)], verbose_name = 'Сумма')
    text = models.TextField(blank = True, verbose_name = 'Текст комментария')

    def __str__(self):
        return f"Запись №{self.id} от {self.date.strftime('%d.%m.%Y')}"
    
    def clean(self):
        category = self.category
        subcategory = self.subcategory

        if category and subcategory and subcategory.category != category:
            raise ValidationError("Подкатегория не соответствует выбранной категории")
        
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
