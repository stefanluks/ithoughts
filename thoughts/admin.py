from django.contrib import admin
from .models import Comentario, Curtir, MicroBlog, Postagem, Usuario


admin.site.register(Comentario)
admin.site.register(Curtir)
admin.site.register(MicroBlog)
admin.site.register(Postagem)
admin.site.register(Usuario)