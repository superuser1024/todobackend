from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.reverse import reverse
from rest_framework.response import Response

from todo.serializers import TodoItemSerializer
from todo.models import TodoItem

# Create your views here.
class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    # override
    def perform_create(self, serializer):
        # save instance to get primary key then update URL
        instance = serializer.save()
        # create a url to the item based on its PK
        instance.url = reverse('todoitem-detail', args=[instance.pk], request=self.request)
        instance.save()
    
    def delete(self, request):
        TodoItem.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    