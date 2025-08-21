from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CareerSerializer,ReisterUserSerializer,ProgamSerializer,InstitutionSerializer,QuestionSerializer,OptionSerializer,QuizSerializer,UserAnswerSerializer
from .models import Institution,Program,Question,Option, Quiz, UserAnswer,Career
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework import generics
from groq import Groq
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.core.cache import cache
from dotenv import load_dotenv
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
load_dotenv()

User = get_user_model


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class RegisterUserView(APIView):
    def post(self,request):
        serializer = ReisterUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username,password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },status=status.HTTP_200_OK)
        return Response({'detail':'invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("Logged out")
            return Response({'detail':'logged out successfully'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail':'invalid token'},status=status.HTTP_400_BAD_REQUEST)


class InstitutionView(APIView):
    def get(self,request):
        data = cache.get("institution")
        if data:
            institution = data
        else:   
            try:
                institution = Institution.objects.all()
            except Exception as e:
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
            serializer = InstitutionSerializer(institution,many=True)
            institution = serializer.data
            cache.set(institution,"institution")
        return Response(data=institution,status=status.HTTP_200_OK)


class ProgramView(APIView):
    def get(self,request):
        data = cache.get("program")
        if data:
            program = data
        else:
            try:
                program = Program.objects.all()
            except Exception as e:
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
            serializer = ProgamSerializer(program,many = True)
            program = serializer.data
            cache.set(program,"program")
        return Response(program,status=status.HTTP_200_OK)

class QuizeDetailView(APIView):
    def get(self,request,pk):
        quiz = Quiz.objects.get(id=pk) 
        serializer = QuizSerializer(quiz)  
        return Response(serializer.data, status=status.HTTP_200_OK)
class GetCourseRecommendation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answers = request.data.get("answers", [])
        if not answers:
            return Response({"error": "No answers provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert submitted answers into text
        answer_texts = []
        for ans in answers:
            try:
                option = Option.objects.get(id=ans["option_id"])
                answer_texts.append(f"{option.question.text} - {option.text}")
            except option.DoesNotExist:
                continue

        answer_text = "\n".join(answer_texts)

        prompt = f"""
        You are an academic advisor. Recommend the most suitable university program 
        ONLY from the following list of available programs. Do not suggest programs outside this list.

        Available Programs:
        - UEW: Basic Education, Early Childhood Education, Special Education, Counselling Psychology, Accounting, Accounting Education, Management Education, Human Resource Management, Religious and Moral Education, Social Studies Education, Biology Education, Chemistry Education, ICT Education
        - AAMUSTED: Accounting, Business Administration, Management, Economics, Human Resource Management, Marketing, Procurement & Supply Chain Management, Banking & Finance, Information Technology Education, Fashion Design & Textiles, Catering and Hospitality, Mechanical Engineering Technology, Automotive Engineering Technology, Electrical & Electronics Engineering Technology, Construction Technology, Wood Technology, Mathematics Education

        Student Answers:
        {answer_text}

        Rules:
        1. Select ONLY from the above programs.
        2. If the student explicitly selects or implies interest in a specific program (e.g., "Banking & Finance"), recommend that program.
        3. Analyze all the answers before recommending.
        4. Be 100% accurate.
        """

        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an academic advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,   # lower temperature for more deterministic output
                max_tokens=500
            )

            recommendation = chat_completion.choices[0].message.content
            return Response({"recommendation": recommendation}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QuizView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data = cache.get("quiz")
        if data:
            quiz = data
        else:
            try:
                quiz = Quiz.objects.all() 
            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            serializer = QuizSerializer(quiz,many=True) 
            quiz = serializer.data
            cache.set(quiz,"quiz") 
        return Response(quiz, status=status.HTTP_200_OK)
    

class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        answers = request.data.get("answers")

        for ans in answers:
            question = Question.objects.get(id= ans["question_id"])
            option = Option.objects.get(id= ans["option_id"])

            UserAnswer.objects.create(user=request.user,question=question,selected_option=option) 

        return Response({"message":"answers submitted successfully"})


class CareerView(APIView):
    def get(self,request):
        data = cache.get("career")
        if data:
            careers = data
        else:
            try:
                careers = Career.objects.all()
            except Exception as e:
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
            serializer = CareerSerializer(careers,many=True)
            career = serializer.data
            cache.set(career,"career")
        return Response(serializer.data,status=status.HTTP_200_OK)


# cache validation

@receiver(post_save, sender=Career)
@receiver(post_delete,sender=Career)
def clear_cache(sender,instance,**kwargs):
    cache.delete('career')

@receiver(post_save, sender=Quiz)
@receiver(post_delete,sender=Quiz)
def clear_cache(sender,instance,**kwargs):
    cache.delete('quiz')

@receiver(post_save, sender=Program)
@receiver(post_delete,sender=Program)
def clear_cache(sender,instance,**kwargs):
    cache.delete('program')

@receiver(post_save, sender=Institution)
@receiver(post_delete,sender=Institution)
def clear_cache(sender,instance,**kwargs):
    cache.delete('institution')
