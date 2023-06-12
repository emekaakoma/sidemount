"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sidemountapi.models import Comment


class CommentView(ViewSet):

    def retrieve(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'event', 'author', 'content', 'created_on')