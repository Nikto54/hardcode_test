from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccess, Lesson
from .serializers import LessonSerializer
from django.contrib.auth.decorators import login_required


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lesson, UserAccess
from .serializers import LessonSerializer

class LessonsByProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        user = request.user
        if not UserAccess.objects.filter(user=user, product_id=product_id, access_granted=True).exists():
            return Response({"error": "У пользователя нет доступа к этому продукту."}, status=403)
        lessons = Lesson.objects.filter(product_id=product_id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
