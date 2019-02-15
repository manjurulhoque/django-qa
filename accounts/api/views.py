from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def register(request):
    # Get form values
    errors = {}
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password1')
    password2 = request.POST.get('password2')
    print(request.POST.get('username'))

    # Check if passwords match
    if password == password2:
        # Check username
        if User.objects.filter(username=username).exists():
            errors['error'] = 'That username is already taken'
            return Response(errors, status.HTTP_409_CONFLICT)
        else:
            if User.objects.filter(email=email).exists():
                errors['error'] = 'That email is being used'
                return Response(errors, status.HTTP_409_CONFLICT)
            else:
                # Looks good
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                errors['success'] = 'You are now registered and can log in'
                return Response(errors, status.HTTP_200_OK)
    else:
        errors['error'] = 'Passwords do not match'
        return Response(errors)
