from rest_framework import viewsets,filters,permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Specialization, CustomUser
from .serializers import SpecializationListSerializer, SpecializationDetailSerializer, DoctorSerializer
from .filters import SpecializationFilter, DoctorFilter
from django_filters.rest_framework import DjangoFilterBackend
from .Pagination import DoctorPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialization.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SpecializationFilter
    search_fields = ['name']

    def get_serializer_class(self):
        """استخدام `SpecializationListSerializer` للقائمة و `SpecializationDetailSerializer` عند تحديد تخصص"""
        if self.action == 'list':
            return SpecializationListSerializer
        return SpecializationDetailSerializer

    @action(detail=True, methods=['get'])
    def doctors(self, request, pk=None):
        """إرجاع جميع الأطباء المرتبطين بتخصص معين"""
        specialization = self.get_object()
        doctors = CustomUser.objects.filter(specialization=specialization, role='doctor', is_approved=True)

        filtered_doctors = DoctorFilter(request.GET, queryset=doctors).qs  # تطبيق الفلاتر هنا

        if not filtered_doctors.exists():
            return Response({"message": "No approved doctors found for this specialization."}, status=200)

        serializer = DoctorSerializer(filtered_doctors, many=True)  # استخدام الأطباء بعد الفلترة
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='doctors/(?P<doctor_id>[^/.]+)')
    def doctor_detail(self, request, pk=None, doctor_id=None):
        """إرجاع بيانات طبيب معين داخل تخصص معين"""
        specialization = self.get_object()
        doctor = get_object_or_404(CustomUser, id=doctor_id, specialization=specialization, role='doctor', is_approved=True)

        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)



class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(role='doctor', is_approved=True)
    serializer_class = DoctorSerializer
    pagination_class = DoctorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DoctorFilter
    search_fields = ['username', 'location', 'specialization__name']

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)




