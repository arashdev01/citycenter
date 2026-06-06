from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'یوزرنیم و پسورد الزامیه'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'این یوزرنیم قبلاً ثبت شده'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'ثبت‌نام موفق'}, status=201)