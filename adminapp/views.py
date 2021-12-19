from django.shortcuts import render, get_object_or_404
from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from adminapp.forms import AdminProductCategoryUpdateForm, AdminProductUpdateForm, AdminShopUserCreateForm, AdminShopUserUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from mainapp.models import ProductCategory, Product
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


class ShopUserList(SuperUserOnlyMixin, ListView):
    model = ShopUser


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserCreateForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserCreateForm()

    context = {
        'title': 'пользователи/создание',
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'title': 'пользователи/редактирование',
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': user,
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    categories = ProductCategory.objects.all()
    context = {
        'object_list': categories,
        'title': 'админка/категории',
    }
    return render(request, 'adminapp/categories_list.html', context)


class ProductCategoryCreateView(SuperUserOnlyMixin, CreateView, PageTitleMixin):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории продуктов/создание'


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     obj = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductCategoryUpdateForm(request.POST, request.FILES, instance=obj)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         form = AdminProductCategoryUpdateForm(instance=obj)

#     context = {
#         'title': 'категории продуктов/редактирование',
#         'form': form
#     }
#     return render(request, 'adminapp/category_update.html', context)


class ProductCategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории продуктов/редактирование'


class ProductCategoryDelete(SuperUserOnlyMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def category_products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = category.product_set.all()
    context = {
        'title': f'категория {category.name}/продукты',
        'category': category,
        'object_list': object_list
    }
    return render(request, 'adminapp/category_products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products',
                kwargs={'pk': category.pk}
            ))
    else:
        form = AdminProductUpdateForm(
            initial={
                'category': category,
                # 'quantity': 10,
                # 'price': 157.9,
            }
        )

    context = {
        'title': 'продукты/создание',
        'form': form,
        'category': category,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products',
                kwargs={'pk': product.category.pk}
            ))
    else:
        form = AdminProductUpdateForm(instance=product)

    context = {
        'title': 'продукты/редактирование',
        'form': form,
        'category': product.category,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(reverse('my_admin:categories'))

    context = {
        'title': 'продукты/удаление',
        'object': obj,
    }
    return render(request, 'adminapp/product_delete.html', context)


class ProductDetail(DetailView):
    model = Product
    pk_url_kwarg = 'product_pk'
