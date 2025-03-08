from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import render

from .forms import CategoryForm, SubCategoryForm, StatusForm, TypeForm, TransactionForm
from .models import Category, SubCategory, Status, Type, Transaction
from .filters import TransactionFilter


"""Реализация с использованием базовых представлений"""
class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/create_status.html'
    success_url = reverse_lazy('transaction:reference')


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/update_status.html'
    success_url = reverse_lazy('transaction:reference')


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'status/delete_status.html'
    success_url = reverse_lazy('transaction:reference')


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm
    template_name = 'type/create_type.html'
    success_url = reverse_lazy('transaction:reference')

class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm
    template_name = 'type/update_type.html'
    success_url = reverse_lazy('transaction:reference')


class TypeDeleteView(DeleteView):
    model = Type
    template_name = 'type/delete_type.html'
    success_url = reverse_lazy('transaction:reference')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create_category.html'
    success_url = reverse_lazy('transaction:reference')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/update_category.html'
    success_url = reverse_lazy('transaction:reference')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete_category.html'
    success_url = reverse_lazy('transaction:reference')


class SubCategoryCreateView(CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'subcategory/create_subcategory.html'
    success_url = reverse_lazy('transaction:reference')


class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'subcategory/update_subcategory.html'
    success_url = reverse_lazy('transaction:reference')


class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = 'subcategory/delete_subcategory.html'
    success_url = reverse_lazy('transaction:reference')


class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'transaction/transaction_list.html'
    ordering = ['date', 'amount']

    def get_queryset(self):
        queryset = super().get_queryset().order_by(self.ordering[0])
        self.filterset = TransactionFilter(self.request.GET, queryset = queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/create_transaction.html'
    success_url = reverse_lazy('transaction:transaction_list')


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/update_transaction.html'
    success_url = reverse_lazy('transaction:transaction_list')


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction/delete_transaction.html'
    success_url = reverse_lazy('transaction:transaction_list')


#Подзапрос, чтобы динамически отображать только те подкатегории, что относятся к выбранной пользователем категории во время настройки фильтрации
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

#Отображение всех имеющихся статусов, типов, категорий и подкатегорий для возможности их редактирования, удаления или создания
def reference(request):
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    context = {
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'reference.html', context)






# """Прямая реализация всех операций для управления данными"""
# # class StatusView:

#     # def create_status(request):
#     #     if request.method == 'POST':
#     #         form = StatusForm(request.POST)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = StatusForm()
#     #     return render(request, '', {'form': form})

#     # def update_status(request, pk):

#     #     status_instance = get_object_or_404(Status, pk = pk)

#     #     if request.method == 'POST':
#     #         form = StatusForm(request.POST, instance = status_instance)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = StatusForm(instance = status_instance)
#     #     return render(request, '', {'form': form})

#     # def delete_status(request, pk):
#     #     status_instance = get_object_or_404(Status, pk = pk)
#     #     status_instance.delete()

#     #     return render(request, '')

# # class TypeView:

#     # def create_type(request):
#     #     if request.method == 'POST':
#     #         form = TypeForm(request.POST)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = TypeForm()
#     #     return render(request, '', {'form': form})

#     # def update_type(request, pk):

#     #     type_instance = get_object_or_404(Type, pk = pk)

#     #     if request.method == 'POST':
#     #         form = TypeForm(request.POST, instance = type_instance)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = TypeForm(instance = type_instance)
#     #     return render(request, '', {'form': form})

#     # def delete_type(request, pk):
#     #     type_instance = get_object_or_404(Type, pk = pk)
#     #     type_instance.delete()

#     #     return render(request, '')

# # class CategoryView:

#     # def create_category(request):
#     #     if request.method == 'POST':
#     #         form = CategoryForm(request.POST)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = CategoryForm()
#     #     return render(request, '', {'form': form})

#     # def update_category(request, pk):

#     #     category_instance = get_object_or_404(Category, pk = pk)

#     #     if request.method == 'POST':
#     #         form = CategoryForm(request.POST, instance = category_instance)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = CategoryForm(instance = category_instance)
#     #     return render(request, '', {'form': form})

#     # def delete_category(request, pk):
#     #     category_instance = get_object_or_404(Category, pk = pk)
#     #     category_instance.delete()

#     #     return render(request, '')

# # class SubCategoryView:

#     # def create_subcategory(request):
#     #     if request.method == 'POST':
#     #         form = SubCategoryForm(request.POST)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = SubCategoryForm()
#     #     return render(request, '', {'form': form})

#     # def update_subcategory(request, pk):

#     #     subcategory_instance = get_object_or_404(SubCategory, pk = pk)

#     #     if request.method == 'POST':
#     #         form = StatusForm(request.POST, instance = subcategory_instance)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('')
#     #     else:
#     #         form = StatusForm(instance = subcategory_instance)
#     #     return render(request, '', {'form': form})

#     # def delete_subcategory(request, pk):
#     #     subcategory_instance = get_object_or_404(SubCategory, pk = pk)
#     #     subcategory_instance.delete()

#     #     return render(request, '')


# # class TransactionView:

# #     def get_transactions_list(request):
# #         queryset = Transaction.objects.all()
# #         transaction_filter = TransactionFilter(request.GET, queryset = queryset)

# #         return render(request, '', {'filter': transaction_filter})

# #     def create_transaction(request):
# #         if request.method == 'POST':
# #             form = TransactionForm(request.POST)
# #             if form.is_valid():
# #                 form.save()
# #                 return redirect('')
# #         else:
# #             form = TransactionForm()
# #         return render(request, '', {'form': form})

# #     def update_transaction(request, pk):

# #         transaction_instance = get_object_or_404(SubCategory, pk = pk)

# #         if request.method == 'POST':
# #             form = TransactionForm(request.POST, instance = transaction_instance)
# #             if form.is_valid():
# #                 form.save()
# #                 return redirect('')
# #         else:
# #             form = TransactionForm(instance = transaction_instance)
# #         return render(request, '', {'form': form})

# #     def delete_transaction(request, pk):
# #         transaction_instance = get_object_or_404(Transaction, pk = pk)
# #         transaction_instance.delete()

# #         return render(request, '')
        
