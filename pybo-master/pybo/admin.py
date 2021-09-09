from django.contrib import admin
from .models import User
from .models import UploadFileModel
from .models import Keyword


class UserAdmin(admin.ModelAdmin):
    search_fields = ['subject']
class UploadFileModelAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(User, UserAdmin)
admin.site.register(UploadFileModel, UploadFileModelAdmin)
admin.site.register(Keyword)
