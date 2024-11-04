from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Product, ProductVariant, ProductImage, DiscountCode, Review, ProductQuestion, ProductAnswer, ProductAnalytics, Wishlist, CartItem, Order, OrderStatusHistory
from django.urls import reverse
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

# List all categories
class CategoryListView(ListView):
    model = Category
    template_name = 'product/category_list.html'  # Updated with app name
    context_object_name = 'categories'


# Detailed view of a specific category
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'product/category_detail.html'  # Updated with app name
    context_object_name = 'category'


# Create a new category
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'product/category_form.html'  # Updated with app name
    success_url = reverse_lazy('product:category-list')


# Update an existing category
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'product/category_form.html'  # Updated with app name
    success_url = reverse_lazy('product:category-list')


# Delete a category
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'product/category_confirm_delete.html'  # Updated with app name
    success_url = reverse_lazy('product:category-list')


### Product Views ###

# List all products
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'  # Updated with app name
    context_object_name = 'products'

class ProductUpdatedListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_updated_list.html'
    context_object_name = 'updated_products'

    def get_queryset(self):
        # Filter products to include only those updated by the logged-in user
        return super().get_queryset().filter(seller=self.request.user).order_by('-updated_at')

# Detailed view of a product
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'  # Updated with app name
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = self.object.variants.all()
        context['reviews'] = self.object.reviews.all()
        context['analytics'] = getattr(self.object, 'analytics', None)
        return context


# Create a new product
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    login_url = '/login/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Populate the category choices
        form.fields['category'].queryset = Category.objects.all()  # Fetch all categories
        return form

    def form_valid(self, form):
        form.instance.seller = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the product detail page of the created product
        return reverse('product:product-detail', kwargs={'pk': self.object.pk})

# Update a product
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['category', 'name', 'description', 'price', 'discount_percentage', 'stock', 'image']
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product:product-list')


# Delete a product
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('product:product-list')

    def get_queryset(self):
        # Filter by the 'seller' field instead of 'created_by'
        return super().get_queryset().filter(seller=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Check if the user is the seller of the product
        self.object = self.get_object()
        if self.object.seller != request.user:
            raise PermissionDenied("You do not have permission to delete this product.")
        return super().delete(request, *args, **kwargs)


### Review Views ###

# Create a review for a product
class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'product/review_form.html'  # Updated with app name

    def form_valid(self, form):
        form.instance.product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product:product-detail', kwargs={'pk': self.kwargs['product_id']})


### Wishlist Views ###

# Display a user's wishlist
class WishlistView(ListView):
    model = Wishlist
    template_name = 'product/wishlist.html'  # Updated with app name
    context_object_name = 'wishlist'

    def get_queryset(self):
        return Wishlist.objects.get_or_create(user=self.request.user)


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return HttpResponseRedirect(reverse_lazy('product:wishlist'))


### Order Views ###

# List all orders for a user
class OrderListView(ListView):
    model = Order
    template_name = 'product/order_list.html'  # Updated with app name
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)



class OrderDetailView(DetailView):
    model = Order
    template_name = 'product/order_detail.html'  # Updated with app name
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


# Update the status of an order (for admin or staff)
class OrderStatusUpdateView(UpdateView):
    model = Order
    fields = ['status']
    template_name = 'product/order_status_form.html'  # Updated with app name
    success_url = reverse_lazy('product:order-list')
