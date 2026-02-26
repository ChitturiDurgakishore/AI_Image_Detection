from django.contrib import admin
from .models import ImageAnalysis


@admin.register(ImageAnalysis)
class ImageAnalysisAdmin(admin.ModelAdmin):
    list_display = ('result', 'created_at')
    readonly_fields = ('image', 'result', 'reason', 'created_at')
