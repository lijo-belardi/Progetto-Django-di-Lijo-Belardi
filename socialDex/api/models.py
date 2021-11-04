from django.db import models
from django.contrib.auth.models import User
from .utils import sendTransaction
import hashlib
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default=None, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    hash = models.CharField(max_length=32, default=None, blank=True, null=True)
    txId = models.CharField(max_length=66, default=None, blank=True, null=True)

    def writeOnChain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()

    def get_absolute_url(self):
        #return full url as a string
        #redirect in new detail view
        return reverse('api:post-detail', kwargs={'pk': self.pk})