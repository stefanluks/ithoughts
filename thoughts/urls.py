
from django.contrib import admin
from django.urls import path
from .views import Home, Comentar, Perfil, Cadastrar, CurtirPost, PostagemView

urlpatterns = [
    path('', Home, name="Home"),
    path('Perfil/<str:username>/', Perfil, name="Perfil"),
    path('PostagemView/', PostagemView, name="PostagemView"),
    path('Cadastrar/', Cadastrar, name="Cadastrar"),
    path('Comentar/<int:post_id>/', Comentar, name="Comentar"),
    path('CurtirPost/<int:post_id>/<int:user_id>/', CurtirPost, name="CurtirPost"),
]
