from django.urls import path,include
from .views import (RegisterUserView,
                    LoginView,LogoutView,
                    ProgramView,InstitutionView,
                    QuizeDetailView,
                    GetCourseRecommendation,
                    QuizView,
                    SubmitAnswerView,CareerView
                    )

urlpatterns = [
    
    # Authentication
    path('register/',RegisterUserView.as_view(),name='reister'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    
    # programs in an institution
    path('programs/',ProgramView.as_view(),name="program"),
    # institutions
    path("institutions/",InstitutionView.as_view(),name="institution"),
    
    # detail quiz
    path("quizes/<int:pk>/", QuizeDetailView.as_view(), name="quiz-detail"),
    
    # all quizes
    path("quizes/",QuizView.as_view(), name="Quizes"),

    # AI recommendation
    path("ai-recommend/", GetCourseRecommendation.as_view(), name="ai-recommendation"),
    
    # answer submition
    path("submit-answer/",SubmitAnswerView.as_view(), name="submit-answer"),

    #Career views
    path("careers/",CareerView.as_view(),name="careers"),

]
