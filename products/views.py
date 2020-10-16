from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect

from emails.forms import InventoryWaitlistForm

from .forms import ProductModelForm
from .models import Product

def featured_product_view(request, *args, **kwargs):
    qs = Product.objects.filter(featured=True)
    product = None
    form = None
    can_order = False
    if qs.exists():
        product = qs.first()
    if product != None:
        can_order = product.can_order
        if can_order: # ()
            product_id = product.id
            request.session['product_id'] = product_id
        form = InventoryWaitlistForm(request.POST or None, product=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product
            if request.user.is_authenticated: # ()
                obj.user = request.user
            obj.save()
            return redirect("/waitlist-success")
    context = {
        "object": product,
        "can_order": can_order,
        "form": form,
    }
    return render(request, "products/detail.html", context)


# def bad_view(request, *args, **kwargs):
#     # print(dict(request.GET))
#     my_request_data = dict(request.GET)
#     new_product = my_request_data.get("new_product")
#     print(my_request_data, new_product)
#     if new_product[0].lower() == "true":
#         print("new product")
#         Product.objects.create(title=my_request_data.get('title')[0], content=my_request_data.get('content')[0])
#     return HttpResponse("Dont do this")


# Create your views here.
def search_view(request, *args, **kwargs): # /search/
    # print(args, kwargs)
    # return HttpResponse("<h1>Hello world</h1>")
    query = request.GET.get('q') # q
    qs = Product.objects.filter(title__icontains=query[0])
    print(query, qs)
    context = {"name": "abc", "query": query}
    return render(request, "home.html", context)

# def product_create_view(request, *args, **kwargs):
#     # print(request.POST)
#     # print(request.GET)
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = ProductForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title"))
#                 title_from_input = my_form.cleaned_data.get("title")
#                 Product.objects.create(title=title_from_input)
#                 # print("post_data", post_data)
#     return render(request, "forms.html", {})

@staff_member_required
def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # instance = form.save(commit=True)
        obj = form.save(commit=False)
        image = request.FILES.get('image')
        media = request.FILES.get('media')
        # do some stuff
        if image:
            obj.image = image
        if media:
            obj.media = media
        obj.user = request.user
        obj.save()
        # print(request.POST)
        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Product.objects.create(**data)
        # Product(**data)
        form = ProductModelForm()
        # return HttpResponseRedirect("/success")
        # return redirect("/success")
    return render(request, "forms.html", {"form": form}) # 200




def product_detail_view(request, pk):
    # obj = Product.objects.get(id=id)
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404 # render html page, with HTTP status code of 404
    # try:
    #     obj = Product.objects.get(id=id)
    # except:
    #     raise Http404
    # return HttpResponse(f"Product id {obj.id}")
    # return render(request, "products/product_detail.html", {"object": obj})
    return render(request, "products/detail.html", {"object": obj})


def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all() # [obj1, obj2, obj3,]
    context = {"object_list": qs}
    return render(request, "products/list.html", context)


def product_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Not found"}) # return JSON with HTTP status code of 404
    return JsonResponse({"id": obj.id})
    

# class HomeView():
#     pass