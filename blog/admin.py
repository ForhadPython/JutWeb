from django.contrib import admin
from .models import *


admin.site.register(PostTag)
admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(PostComment)
