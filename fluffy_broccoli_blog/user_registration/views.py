from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse

# Create your views here.
def api_registration(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)