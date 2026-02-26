from django.db import models


class ImageAnalysis(models.Model):
    """Simple model to store image analysis results (optional)."""
    image = models.ImageField(upload_to='analyses/')
    result = models.CharField(max_length=10, choices=[('AI', 'AI-Generated'), ('Real', 'Real')])
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.result} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
