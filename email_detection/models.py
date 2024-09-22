from django.db import models

class EmailClassification(models.Model):
    email_text = models.TextField()
    classification = models.CharField(max_length=20)
    is_correct = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email_text[:50]}... - {self.classification}"
