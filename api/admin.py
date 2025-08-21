from django.contrib import admin
from .models import Career,CustomUser,Institution,Program,Question,Option,Quiz,UserAnswer


admin.site.register(CustomUser)
admin.site.register(Program)
admin.site.register(Institution)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Quiz)
admin.site.register(UserAnswer)
admin.site.register(Career)

