from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sidemountapi.models import Comment, SideMountUser, Event

class CommentView(ViewSet):
    """Comment view"""

    def retrieve(self, request, pk=None):
        """Handle get requests for single comment"""
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET request for all comments"""
        comments = Comment.objects.all()
        user = SideMountUser.objects.get(user=request.auth.user)

        event_id = request.query_params.get('event_id', None)
        if event_id is not None:
            comments = comments.filter(event_id=event_id)

        for comment in comments:
            if comment.author == user:
                comment.can_delete = True
            else:
                comment.can_delete = False

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST request for comment"""

        author = SideMountUser.objects.get(user=request.auth.user)
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT request for update"""
        comment = Comment.objects.get(pk=pk)
        author = SideMountUser.objects.get(user=request.auth.user)
        comment.author = author
        event = Event.objects.get(pk=request.data['event'])
        comment.event = event
        comment.content = request.data['content']
        comment.created_on = request.data['created_on']
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE request"""
        comment=Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'event_id', 'author', 'content','created_on', 'can_edit', 'can_delete')
        depth = 2

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'event', 'content', 'created_on')
