"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Count
from django.db.models import Q
from sidemountapi.models import Event, SideMountUser, Gi, Attendee
from django.contrib.auth.models import User


class EventView(ViewSet):

    def retrieve(self, request, pk):
        event = Event.objects.get(pk=pk)
        user = SideMountUser.objects.get(user=request.auth.user)
        event.joined = user in event.attendees.all()
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        user = SideMountUser.objects.get(user=request.auth.user)
        events = Event.objects.all()
        events = Event.objects.annotate(attendee_count=Count('attendee'),
            joined=Count(
                'attendees',
                filter=Q(attendees=user)))
        
        for event in events:
            if event.organizer == user:
                event.can_delete = True
            if event.organizer == user:
                event.can_edit = True
        
        if user:
            search = request.query_params.get('search', None)
            if search is not None:
                events = events.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search)
                )

        serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        user = SideMountUser.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):

        event=Event.objects.get(pk=pk)
        event.description=request.data["description"]
        event.title=request.data["title"]
        event.date=request.data["date"]
        event.time=request.data["time"]
        event.location=request.data["location"]
        event.requirements=request.data["requirements"]
        event.image_url=request.data["image_url"]

        gi = Gi.objects.get(pk=request.data["gi"])
        event.gi=gi

        organizer=SideMountUser.objects.get(user=request.auth.user)
        event.organizer=organizer

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event=Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    
    @ action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        organizer=SideMountUser.objects.get(user=request.auth.user)
        event=Event.objects.get(pk=pk)
        event.attendees.add(organizer)
        return Response({'message': 'User added'}, status=status.HTTP_201_CREATED)

    @ action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""

        organizer=SideMountUser.objects.get(user=request.auth.user)
        event=Event.objects.get(pk=pk)
        event.attendees.remove(organizer)
        return Response({'message': 'User removed'}, status=status.HTTP_204_NO_CONTENT)
    
    @ action(methods=["get"], detail=False)
    def myevents(self, request):
        """Get method for my posts"""
        user = SideMountUser.objects.get(user=request.auth.user)
        events = Event.objects.filter(organizer=user).annotate(attendee_count=Count('attendee'),
            joined=Count(
                'attendees',
                filter=Q(attendees=user)))

        try:
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({"message": "This event isn't yours, authenticated user."}, status=404)
        
    @ action(methods=["get"], detail=False)
    def attendingevents(self, request):
        """Get method for my posts"""
        user = SideMountUser.objects.get(user=request.auth.user)
        events = Event.objects.all()
        # attendees = Attendee.objects.all()
        events = Event.objects.annotate(
        attendees_count=Count('attendees'),
        joined=Count(
            'attendees',
            filter=Q(attendees__user=user)
    )
)

        try:
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({"message": "This event isn't yours, authenticated user."}, status=404)

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'organizer', 'description', 'title', 'date', 'time', 'location', 'attendees', 'joined', 'image_url', 'requirements', 'gi', 'can_edit', 'can_delete')
        depth = 2

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'description', 'title', 'date', 'time', 'location', 'image_url', 'requirements', 'gi']