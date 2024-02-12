from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from .models import Items
from .serializers import ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page



# Create your views here.
def home(request):
    return render(request, "kaizntree/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        return redirect('signin')

    return render(request, "kaizntree/signup.html")



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            item_list = Items.objects.all()
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('item_dashboard')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')

    return render(request, "kaizntree/index.html")


class item_dashboard(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        queryset = Items.objects.all()
        stock_status = request.query_params.get('stock_status')
        sku = request.query_params.get('sku')
        name = request.query_params.get('name')
        category = request.query_params.get('category')
        available_stock = request.query_params.get('available_stock')
        if stock_status:
            queryset = queryset.filter(stock_status=stock_status)
        if sku:
            queryset = queryset.filter(sku=sku)
        if name:
            queryset = queryset.filter(name=name)
        if category:
            queryset = queryset.filter(category=category)
        if available_stock:
            queryset = queryset.filter(available_stock=available_stock)
        serializer = ItemSerializer(queryset, many=True)
        context = {'items': serializer.data}  # Pass serialized data to the context
        return render(request, 'kaizntree/dashboard.html', context, status=status.HTTP_200_OK)