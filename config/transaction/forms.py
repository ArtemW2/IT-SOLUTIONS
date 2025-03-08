from django import forms

from .models import Category, SubCategory, Status, Type, Transaction


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = '__all__'


