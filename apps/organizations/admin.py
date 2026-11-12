from django.contrib import admin

from .models import Branch, ClassEnrollment, ClassGroup, Course, StudentProfile, TeacherAssignment, TeacherProfile


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "branch", "course", "is_active")
    list_filter = ("branch", "course", "is_active")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "registration_number", "branch")
    search_fields = ("registration_number", "user__email")


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "branch")
    search_fields = ("user__email",)


@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "class_group", "status")
    list_filter = ("status", "class_group")


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ("teacher", "class_group", "course")
    list_filter = ("class_group", "course")
