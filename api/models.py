from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=True)
    password2 = models.CharField(max_length=20)
    
    def __str__(self):
        return self.username


class Institution(models.Model):
    institution_name = models.CharField(max_length=60)
    institution_description = models.TextField(null=True,blank=True)
    institution_body = models.TextField(null=True,blank=True)
    location = models.TextField(null=True,blank=True)
    institution_logo = models.ImageField(upload_to="logos",null=True,blank=True)
    institution_website = models.URLField(null=True,blank=True)
    

    def __str__(self):
        return self.institution_name

class Program(models.Model):
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name="programs",null=True)
    course_title = models.CharField(max_length=100)
    course_description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.course_title


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"

    def __str__(self):
        return f'{self.title}'

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions")
    text = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.text}'

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="options")
    text = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.text} '


class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option,on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username}'


class Career(models.Model):
    career = models.CharField(max_length=60,unique=True)

    def __str__(self):
        return f'{self.career}'