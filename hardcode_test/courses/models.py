from datetime import timezone

from django.db import models
from django.db.models import Count

from django.contrib.auth.models import User

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accesses')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accesses')
    access_granted = models.BooleanField(default=False)

    def __str__(self):
        return (f"Доступ {self.user.username} к {self.product.name}: "
                f"{'Разрешен' if self.access_granted else 'Запрещен'}")
class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=255)
    video_url = models.URLField()

    def __str__(self):
        return self.name

class Group(models.Model):
    students = models.ManyToManyField(User, related_name='group_memberships')
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')
    min_students = models.IntegerField(default=1)
    max_students = models.IntegerField()

    def __str__(self):
        return self.name

def get_student_access(student,product):
    groups=Group.objects.filter(product=product).annotate(student_count=Count('students')).group_by('student_count')
    if product.start_datetime>timezone.now():
        student_group=None
        for group in groups:
            if group.min_students<=group.student_count<group.max_students:
                student_group=group
        if student_group:
            student_group.students.add(student)
    else:
        groups[0].students.add(student)



