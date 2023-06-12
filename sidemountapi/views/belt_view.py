"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sidemountapi.models import Belt


class BeltView(ViewSet):

    def retrieve(self, request, pk):
        belt = Belt.objects.get(pk=pk)
        serializer = BeltSerializer(belt)
        return Response(serializer.data)


    def list(self, request):
        belts = Belt.objects.all()
        serializer = BeltSerializer(belts, many=True)
        return Response(serializer.data)

class BeltSerializer(serializers.ModelSerializer):

    class Meta:
        model = Belt
        fields = ('id', 'label')