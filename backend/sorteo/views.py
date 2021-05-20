import random

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, renderers
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.sorteo.models import User, Lottery
from backend.sorteo.serializers import UserSerializer, LotterySerializer, VerifyUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects

    @action(methods=['POST'], detail=True)
    def verify(self, request, pk):
        """
            Funcion para colocar la contraseña y verificar el usuario
        """
        serializer = VerifyUserSerializer(
            self.get_object(),
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LotteryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LotterySerializer
    queryset = Lottery.objects

    @action(methods=['POST'], detail=False)
    def win(self, request):
        """
            Peticion para obtener el ganador
        """

        count_user = User.objects.vefiry().count()
        if count_user < 1:
            return Response(status=status.HTTP_404_NOT_FOUND)

        index_user = random.randrange(0, count_user)
        winner = User.objects.vefiry()[index_user]
        lottery = Lottery.objects.create(user=winner)
        serializer = LotterySerializer(lottery)
        return Response(serializer.data, status=status.HTTP_200_OK)
