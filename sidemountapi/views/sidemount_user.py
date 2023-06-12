"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sidemountapi.models import SideMountUser


class SideMountUserView(ViewSet):

    def retrieve(self, request, pk):
        user = SideMountUser.objects.get(pk=pk)
        serializer = SideMountSerializer(user)
        return Response(serializer.data)


    def list(self, request):
        users = SideMountUser.objects.all()
        serializer = SideMountSerializer(users, many=True)
        return Response(serializer.data)

class SideMountSerializer(serializers.ModelSerializer):

    class Meta:
        model = SideMountUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'belt')