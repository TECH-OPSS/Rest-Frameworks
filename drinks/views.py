from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Drink
from .serializers import DrinkSerializer

@api_view(['GET', 'POST'])
def drink_list(request):
    if request.method == 'GET':
        # Get all drinks
        drinks = Drink.objects.all()
        # Serialize them
        serializer = DrinkSerializer(drinks, many=True)
        # Return JSON response
        return Response({'drinks': serializer.data})

    elif request.method == 'POST':
        # Deserialize the incoming data
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response({'error': 'Drink not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response({'message': 'Drink deleted'}, status=status.HTTP_204_NO_CONTENT)
