from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
# from PIL import Image
from django.urls import reverse 

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    bio= models.CharField(max_length=100)
    prof_pic= CloudinaryField('image')
    following= models.ManyToManyField(User, related_name='follower', blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

    def save_profile(self):
        self.save()
    
    def delete_profile(self):
        self.delete()

    def profiles_posts(self):
        return self.image_set.all()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

    class Meta:
        ordering=('-created',)
       
class Image(models.Model):
    image= CloudinaryField('image')
    author= models.ForeignKey(Profile, on_delete=models.CASCADE)
    name= models.CharField(max_length=30)
    caption= models.TextField()
    comments = models.CharField(max_length=30,blank=True)
    likes=models.ManyToManyField(User, related_name='blog_posts')
    pub_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()
    
    def save_image(self):
        self.save()
    
    def delete_image(self):
        self.delete()
    
    def update_image(self):
        self._do_update()
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

class Comment(models.Model):
    user_id= models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    image_id=models.ForeignKey(Image,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} :{self.comment}'



class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'    
