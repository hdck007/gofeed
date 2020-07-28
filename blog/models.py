from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Post(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField(default='write your description here',max_length=255)
  content = RichTextField(blank=True, null=True)
  # content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.title
    
  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})
    