from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Career,Program,Institution,Question,Option,UserAnswer,Quiz

User = get_user_model()

class ReisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)
    
    class Meta:
        model=User
        fields =['username','email','is_student','password','password2']
    
    def validate(self, data):
        if data['password2'] != data['password']:
            raise ValidationError('Both passwords must match')
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProgamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields ="__all__"

class InstitutionSerializer(serializers.ModelSerializer):
    programs = ProgamSerializer(many=True,read_only=True)
    institution_logo = serializers.ImageField(use_url=True)
    class Meta:
        model = Institution
        fields = "__all__"

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id','text']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True,read_only=True)

    class Meta:
        model = Question
        fields = ["id","text","options"]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,read_only=True)
    class Meta:
        model = Quiz
        fields = ["id","title","questions"]


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ["question","selected_option"]


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = "__all__"