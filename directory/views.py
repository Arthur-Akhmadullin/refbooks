import datetime

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Refbook, Version, Element
from .serializers import RefbookSerializer, ElementSerializer
from .swg_parametres import refbook_list_api_param, elemet_list_api_param, valid_element_api_param


class RefbookListAPIView(ListAPIView):
    @swagger_auto_schema(**refbook_list_api_param)
    def get(self, request, *args, **kwargs):
        queryset = Refbook.objects.all()

        date = self.request.query_params.get('date', None)
        if date:
            queryset = Refbook.objects.filter(versions__date__lte=date).distinct()

        serializer = RefbookSerializer(queryset, many=True)
        return Response({'refbooks': serializer.data})


class ElementListAPIView(ListAPIView):
    @swagger_auto_schema(**elemet_list_api_param)
    def get(self, request, *args, **kwargs):
        id_param = self.kwargs.get('id')

        version_param = self.request.query_params.get('version', None)
        if version_param:
            version = Version.objects.get(refbook_id=id_param, version=version_param)
        else:
            date_today = datetime.datetime.now()
            version = Version.objects.filter(refbook_id=id_param,
                                             date__lte=date_today).order_by('date').last()

        queryset = Element.objects.filter(version_id=version.id)
        serializer = ElementSerializer(queryset, many=True)
        return Response({'elements': serializer.data})


class ValidElementsAPIView(ListAPIView):
    @swagger_auto_schema(**valid_element_api_param)
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')

        code_param = self.request.query_params.get('code', None)
        value_param = self.request.query_params.get('value', None)
        version_param = self.request.query_params.get('version', None)

        if not code_param or not value_param:
            raise AssertionError("Проверьте наличие параметров <code> и <value> в вашем запросе")

        if version_param:
            version = Version.objects.get(refbook_id=id, version=version_param)
        else:
            now = datetime.datetime.now()
            version = Version.objects.filter(refbook_id=id,
                                             date__lte=now).order_by('date').last()

        queryset = Element.objects.filter(code=code_param,
                                          value=value_param,
                                          version_id=version.id)

        if queryset.exists():
            serializer = ElementSerializer(queryset, many=True)
            return Response({'element': serializer.data})
        else:
            return Response({'element': None})
