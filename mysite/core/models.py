from django.db import models


class Connection(models.Model): 
    ip = models.GenericIPAddressField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username

class About(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=100)
    image = models.FilePathField(path="/media")    

