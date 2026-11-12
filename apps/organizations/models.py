from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Branch(BaseModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Course(BaseModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class ClassGroup(BaseModel):
    name = models.CharField(max_length=150)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="classes")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="class_groups")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} | {self.course.name}"


class StudentProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    registration_number = models.CharField(max_length=50, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="students")

    def __str__(self):
        return f"{self.user.email} ({self.registration_number})"


class TeacherProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="teachers")

    def __str__(self):
        return self.user.email


class ClassEnrollment(BaseModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="class_enrollments")
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="active", choices=(("active", "Active"), ("inactive", "Inactive"), ("completed", "Completed")))

    class Meta:
        unique_together = ("student", "class_group")

    def __str__(self):
        return f"{self.student} -> {self.class_group}"


class TeacherAssignment(BaseModel):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="class_assignments")
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="teacher_assignments")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="teacher_assignments")

    class Meta:
        unique_together = ("teacher", "class_group", "course")

    def __str__(self):
        return f"{self.teacher} -> {self.class_group}"
