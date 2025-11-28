from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import CustomUser
from .serializers import(
    UserLoginSerializer,
    UserRegistrationSerializer
)




class RegisterView(APIView):
    def post(self,request):
        ser = UserRegistrationSerializer(data=request.data)
        if ser.is_valid:
            ser.save()
            return Response({'message':'Usr Register'},status=201)
        return Response(ser.errors,status=400)
    




class LoginView(APIView):
    def post(self,request):
        ser = UserLoginSerializer(data=request.data,context={"reques":request})
        if ser.is_valid():
            ser.save()
            return Response({'message':'User is authenicate.'},status=201)
        return Response(ser.errors,status=400)
    