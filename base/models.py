from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length = 200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    
    avatar = models.ImageField(null=True, default='avatar.svg')
    
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
    
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #null is for the database and blank is for the form; when we run the save method
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) #this takes a snapshot of anytime this model or its instance is updated. so anytime we run the save method to update the model/table its gonna take a time and date stamp 
    created = models.DateTimeField(auto_now_add=True) #auto_now_add only takes a timestamp when we first save or create this instance.

    class Meta:
        ordering = ['-updated', '-created'] #this is too order the room in a certain order.in this case, it is to order by updated and created in ascending or decending order depending on "-"

    def __str__(self):
        return self.name
    
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #CASCADE means that when a room is deleted, the message also gets deleted from the db.SET_NULL means that when the room gets deleted the message still stays in the db.
    body = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='room/image/', null=True, blank=True)  # Field for image
    document = models.FileField(upload_to='room/documents/', null=True, blank=True)  # Field for documents
    video = models.FileField(upload_to='room/videos/', null=True, blank=True)  # Field for videos
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] #this is too order the room in a certain order.in this case, it is to order by updated and created in ascending or decending order depending on "-"

    # def __str__(self):
    #     return self.body[0:50]

    def __str__(self):
        if self.document:
            return self.document.name
        elif self.video:
            return self.video.name
        else:
            return self.body[:50] if self.body else "Message with no content"
        
        
        
class Resource(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #null is for the database and blank is for the form; when we run the save method
    updated = models.DateTimeField(auto_now=True) #this takes a snapshot of anytime this model or its instance is updated. so anytime we run the save method to update the model/table its gonna take a time and date stamp 
    created = models.DateTimeField(auto_now_add=True) #auto_now_add only takes a timestamp when we first save or create this instance.

    class Meta:
        ordering = ['-updated', '-created'] #this is too order the room in a certain order.in this case, it is to order by updated and created in ascending or decending order depending on "-"

    def __str__(self):
        return self.name
    
    
    
    
class Res(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE) #CASCADE means that when a room is deleted, the message also gets deleted from the db.SET_NULL means that when the room gets deleted the message still stays in the db.
    image = models.FileField(upload_to='res/image/', null=True, blank=True)  # Field for image
    document = models.FileField(upload_to='res/documents/', null=True, blank=True)  # Field for documents
    video = models.FileField(upload_to='res/videos/%y', null=True, blank=True)  # Field for videos
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created'] #this is too order the room in a certain order.in this case, it is to order by updated and created in ascending or decending order depending on "-"

    # def __str__(self):
    #     return self.body[0:50]

    def __str__(self):
        if self.document:
            return self.document.name
        elif self.video:
            return self.video.name
        else:
            return "Resource with no content"