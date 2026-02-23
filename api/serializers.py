from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import *
import os

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"

    def validate(self, data):
        instance = Entity(**data)
        try:
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError({"detail": e.messages})
        return data


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

class RegisterHeadSerializer(serializers.ModelSerializer):
    proyecto = serializers.PrimaryKeyRelatedField(
        queryset=Entity.objects.filter(deleted=False)
    )

    class Meta:
        model = RegisterHead
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['proyecto'] = EntitySerializer(instance.proyecto).data
        return data



class UbicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubication
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class RegisterFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterFiles
        fields = "__all__"


class RegisterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterDetail
        fields = "__all__"
        
class EquipmentFilesSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = EquipmentFiles
        fields = "__all__"

    def get_file(self, obj):
        # Construimos la URL absoluta manualmente
        if obj.file:
          return f"{os.getenv('BASE_URL')}/media/{obj.file}"
        return None


class EquipmentSerializer(serializers.ModelSerializer):
    images = EquipmentFilesSerializer(many=True, read_only=True)  # <--- aquí

    class Meta:
        model = Equipment
        fields = "__all__"
        
class PistolasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PistolaTorque
        fields = "__all__"