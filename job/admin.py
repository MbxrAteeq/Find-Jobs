from django.contrib import admin

from .models import Job, UserApplication


class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ("title", "job_type", "location", "occupied", "user")
    list_filter = ("occupied", "job_type", )
    search_fields = ("title", "job_type", "location", "occupied", "user")
    ordering = ("created_at",)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class UserApplicationAdmin(admin.ModelAdmin):
    model = UserApplication
    list_display = ("user", "job", "resume")
    list_filter = ("user", "job")
    search_fields = ("user", "job")
    ordering = ("created_at",)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
admin.site.register(UserApplication, UserApplicationAdmin)
