"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sidemountapi.models import Gi


class GiView(ViewSet):

    def retrieve(self, request, pk):
        gi = Gi.objects.get(pk=pk)
        serializer = GiSerializer(gi)
        return Response(serializer.data)


    def list(self, request):
        gis = Gi.objects.all()
        serializer = GiSerializer(gis, many=True)
        return Response(serializer.data)

class GiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gi
        fields = ('id', 'label')