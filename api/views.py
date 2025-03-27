from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import *
from api.authentication import CustomJWTAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import get_object_or_404
import jwt, datetime
from api.permissions import *
from rest_framework import status
from rest_framework.permissions import *
from .permissions import *
from .serializers import *
from .utils import *
from google.oauth2 import id_token



@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")
    role = request.data.get("role")

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(password)
    user = User.objects.create(email=email, password=hashed_password, role=role)

    return Response({"message": "User registered successfully", "id" : user.id}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    token = generate_jwt_token(user)
    return Response({"token": token, "user": {"id": user.id, "role": user.role}}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def google_auth(request):
    token = request.data.get("id_token")
    if not token:
        return Response({"error": "ID Token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        email = id_info["email"]
        google_id = id_info["sub"]

        user, created = User.objects.get_or_create(email=email, defaults={"google_id": google_id})

        jwt_token = generate_jwt_token(user)

        return Response({"token": jwt_token, "new_user": created}, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def post(self, request):
        if request.user.role != "admin":
            return Response({"error": "Permission denied"}, status=403)

        task = Task.objects.create(
            title=request.data.get("title"),
            description=request.data.get("description"),
            status="Pending",
            assigned_to_id=request.data.get("assigned_to"),
        )
        return Response({"message": "Task created", "task_id": task.id}, status=201)

    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        task.status = request.data.get("status", task.status)
        task.save()
        return Response({"message": "Task status updated"}, status=200)

    def get(self, request):
        if request.user.role == "admin":
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to=request.user)
            print(f"{tasks=}")
        serializer = TaskSerializer(tasks, many=True)
        
        return Response(serializer.data)

    def delete(self, request, task_id):
        if request.user.role != "admin":
            return Response({"error": "Permission denied"}, status=403)

        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return Response({"message": "Task deleted"}, status=204)

