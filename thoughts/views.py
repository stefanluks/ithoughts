from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Postagem, MicroBlog, Comentario, Curtir, Usuario

def Home(request):
    postagens = Postagem.objects.all().reverse()
    logado = None
    if request.user.is_authenticated:
        logado = Usuario.objects.get(user=request.user)
    return render(request, 'home.html', {
        "usuario": request.user,
        "logado":logado,
        "postagens":postagens,
    })


def Comentar(request, post_id):
    comentario = Comentario()
    comentario.texto = request.GET["texto"]
    comentario.autor = Usuario.objects.get(user__id = request.user.pk)
    comentario.save()
    postagem = Postagem.objects.get(pk=post_id)
    postagem.comentarios.add(comentario)
    erro = False
    return JsonResponse(data = {"error":erro, "comentario": comentario.json()}, safe=False)


def Perfil(request, username):
    if Usuario.objects.filter(user__username=username):
        perfil = Usuario.objects.get(user__username=username)
        postagens = Postagem.objects.filter(autor=perfil)
        logado = None
        if request.user.is_authenticated:
            logado = Usuario.objects.get(user=request.user)
        return render(request, "perfil.html", {
            "usuario": request.user,
            "logado": logado,
            "postagens":postagens,
            "perfil":perfil,
        })
    return render(request, "erro.html", {
        "msg":"Úsuario não encontrado!"
    })


def Cadastrar(request):
    if request.method == "GET":
        return render(request, "cadastrar.html")
    elif request.method == "POST":
        post = request.POST
        
        user = User()
        user.username = post["username"]
        user.password = make_password(post["password"])
        user.save()
        
        novo = Usuario()
        novo.nome = post["nome"]
        novo.bio = post["bio"]
        novo.user = user
        novo.save()

        return redirect("Home")
    

def PostagemView(request):
    if request.method == "POST":
        texto = request.POST["texto"]

        if request.user.is_authenticated:
            if Usuario.objects.filter(user = request.user):
                user = Usuario.objects.get(user=request.user)

                blog = MicroBlog()
                blog.texto = texto
                blog.autor = user
                blog.save()

                postagem = Postagem()
                postagem.blog = blog
                postagem.autor = user
                postagem.save()

            return redirect("Home")
        else:
            return render(request, "erro.html", {"msg": "Ralize login para publicar!"}) 
    return render(request, "erro.html", {"msg": "Ralize login para publicar!"}) 



def CurtirPost(request, post_id, user_id):
    if Postagem.objects.filter(pk=post_id):
        postagem = Postagem.objects.get(pk=post_id)
        if Usuario.objects.get(pk=user_id):
            usuario = Usuario.objects.get(pk=user_id)
            if Curtir.objects.filter(post=postagem, autor=usuario):
                curtida = Curtir.objects.get(post=postagem, autor=usuario)
                curtida.delete()
            else:
                like = Curtir()
                like.post = postagem
                like.autor = usuario
                like.save()

            return JsonResponse(data={
                "erro": False,
                "msg":"operação realizada com sucesso!"
            },
            safe=False)
        else:
            return JsonResponse(data={
                "erro": True,
                "msg":"Houve um erro!"
            },
            safe=False)
    return JsonResponse(data={
        "erro": True,
        "msg":"Houve um erro!"
    },
    safe=False)
            