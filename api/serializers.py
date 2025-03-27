from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']

    def validate_status(self, value):
        if value not in ['Pending', 'Completed']:
            raise serializers.ValidationError("Invalid status. Choose 'Pending' or 'Completed'.")
        return value