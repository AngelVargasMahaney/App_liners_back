from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    Entity,
    RegisterHead,
    RegisterFiles,
    RegisterDetail,
    Activity,
    Equipment,
    Ubication,
    Job,
    PistolaTorque
)

from .serializers import (
    EntitySerializer,
    ActivitySerializer,
    EquipmentSerializer,
    RegisterHeadSerializer,
    RegisterFilesSerializer,
    RegisterDetailSerializer,
    UbicationSerializer,
    JobSerializer,
    PistolasSerializer
)

class BaseAPIView(APIView):
    permission_classes = []
    model = None
    serializer_class = None
    soft_delete = False

    def get_queryset(self):
        qs = self.model.objects.all()
        if self.soft_delete:
            qs = qs.filter(deleted=False)
        return qs

    def get(self, request, pk=None):
        if pk:
            obj = get_object_or_404(self.get_queryset(), pk=pk)
            serializer = self.serializer_class(obj)
            return Response({"status": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        objs = self.get_queryset()
        serializer = self.serializer_class(objs, many=True)
        return Response({"status": "Success", "data": serializer.data},  status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "Failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "data": serializer.data})
        return Response({"status": "Failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        if self.soft_delete:
            obj.deleted = True
            obj.deleted_at = timezone.now()
            obj.save()
        else:
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EntityAPIViewCampain(APIView):
    
    permission_classes = []
    def get(self, request, pk=None):
        if pk:
            entity = get_object_or_404(Entity, pk=pk, deleted=False)
            serializer = EntitySerializer(entity)
            return Response({"status": "Success", "data": serializer.data})

        queryset = Entity.objects.filter(deleted=False)

        entity_type = request.query_params.get("type")
        parent = request.query_params.get("parent")

        if entity_type:
            queryset = queryset.filter(type=entity_type)

        if parent:
            queryset = queryset.filter(parent_id=parent)

        serializer = EntitySerializer(queryset, many=True)
        return Response({"status": "Success", "data": serializer.data})

class EntityAPIView(BaseAPIView):
    model = Entity
    serializer_class = EntitySerializer
    soft_delete = True


class ActivityAPIView(BaseAPIView):
    model = Activity
    serializer_class = ActivitySerializer

class RegisterHeadAPIView(BaseAPIView):
    model = RegisterHead
    serializer_class = RegisterHeadSerializer
    soft_delete = True


class UbicationAPIView(BaseAPIView):
    model = Ubication
    serializer_class = UbicationSerializer


class JobAPIView(BaseAPIView):
    model = Job
    serializer_class = JobSerializer


class RegisterFilesAPIView(BaseAPIView):
    model = RegisterFiles
    serializer_class = RegisterFilesSerializer
    soft_delete = True


class RegisterDetailAPIView(BaseAPIView):
    model = RegisterDetail
    serializer_class = RegisterDetailSerializer
    soft_delete = True
    
class EquipmentAPIView(BaseAPIView):
    model = Equipment
    serializer_class = EquipmentSerializer
    soft_delete = True
    
class PistolasTorqueAPIView(BaseAPIView):
    model = PistolaTorque
    serializer_class = PistolasSerializer
    soft_delete = True
    
class ProjectsByEquipoAPIView(APIView):
    permission_classes = []

    def get(self, request):
        equipo = request.query_params.get("equipo")
        campaign_id = request.query_params.get("campaign")

        if not equipo:
            return Response(
                {"error": "equipo es requerido"},
                status=400
            )

        filters = {
            "deleted": False,
            "type": Entity.PROYECTO,
            "registerhead__equipo": equipo,
        }

        if campaign_id:
            filters["parent_id"] = campaign_id

        projects = Entity.objects.filter(**filters).distinct()

        serializer = EntitySerializer(projects, many=True)
        return Response({
            "status": "Success",
            "data": serializer.data
        })

    
class ActivitiesByProjectAPIView(APIView):
    permission_classes = []
    def get(self, request):
        project_id = request.query_params.get("project")
        equipo = request.query_params.get("equipo")

        if not project_id or not equipo:
            return Response(
                {"error": "project y equipo son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1️⃣ Verificar que exista la combinación en RegisterHead
        exists = RegisterHead.objects.filter(
            proyecto_id=project_id,
            equipo=equipo,
            deleted=False
        ).exists()

        if not exists:
            # No está habilitado ese proyecto para ese equipo
            return Response({
                "status": "Success",
                "data": []
            })

        # 2️⃣ Devolver TODAS las actividades del proyecto
        activities = Activity.objects.filter(
            project_id=project_id
        )

        serializer = ActivitySerializer(activities, many=True)

        return Response({
            "status": "Success",
            "data": serializer.data
        })
    
class RegisterHeadByProjectAPIView(APIView):
    permission_classes = []

    def get(self, request):
        project_id = request.query_params.get("project")
        equipment_id = request.query_params.get("equipment")

        filters = {}

        if project_id:
            filters["proyecto_id"] = project_id

        if equipment_id:
            filters["equipo_id"] = equipment_id

        heads = (
            RegisterHead.objects
            .filter(**filters)
            .order_by("-initial_date")
        )

        serializer = RegisterHeadSerializer(heads, many=True)
        return Response({
            "status": "Success",
            "data": serializer.data
        })


class CurrentRegisterDetailAPIView(APIView):
    permission_classes = []
    def get(self, request):
        register_head = request.query_params.get("register_head")
        activity = request.query_params.get("activity")
        ubication = request.query_params.get("ubication")
        job = request.query_params.get("job")

        if not all([register_head, activity, ubication, job]):
            return Response(
                {"error": "Parámetros incompletos"},
                status=400
            )

        detail = RegisterDetail.objects.filter(
            register_head_id=register_head,
            activity_id=activity,
            ubication_id=ubication,
            job_id=job,
        ).first()

        if not detail:
            return Response({"exists": False})

        return Response({
            "exists": True,
            "id": detail.id,
            "shape_information": detail.shape_information
        })
