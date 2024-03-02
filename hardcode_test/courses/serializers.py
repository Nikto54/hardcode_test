from rest_framework import serializers
from .models import Product, UserAccess, Lesson


class ProductSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    filled_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'creator', 'name', 'start_datetime', 'price', 'lessons', 'students', 'filled_percentage']

    def get_students(self, obj):
        return UserAccess.objects.filter(product=obj, access_granted=True).count()

    def get_lessons(self, obj):
        return Lesson.objects.filter(product=obj).count()

    def get_filled_percentage(self, obj):
        groups = obj.groups.all()
        filled_percentage_sum = 0

        if not groups.exists():
            return 0

        for group in groups:
            current_students = group.students.count()
            max_students = group.max_students
            if max_students > 0:
                filled_percentage_sum += (current_students / max_students) * 100


        filled_percentage = filled_percentage_sum / groups.count()
        return round(filled_percentage, 2)



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_url']


