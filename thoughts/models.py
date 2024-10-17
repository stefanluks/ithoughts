from django.db import models
from django.contrib.auth.models import User

class  Usuario(models.Model):
    nome = models.CharField("nome do usuario", max_length=50)
    bio = models.TextField("Descrição do úsuario", max_length=250, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def json(self):
        obj = {
            "nome":self.nome,
            "bio":self.bio,
            "user":{
                "username":self.user.username,
                "pk":self.user.id,
            }
        }
        return obj  

    def __str__(self):
        return self.nome
    

class MicroBlog(models.Model):
    class Meta:
        verbose_name = "Micro blog"
        verbose_name_plural = "Micro blog's"

    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField("Texto do blog", max_length=500)

    def __str__(self):
        return f"blog: ID[{self.pk}] de {self.autor.nome}"


class Comentario(models.Model):
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField("Texto do comentário", max_length=500)

    def json(self):
        obj = {
            "texto":self.texto,
            "autor":self.autor.json()
        }
        return obj

    def __str__(self):
        return f"comentario: ID[{self.pk}] de {self.autor.nome}"
    

class Postagem(models.Model):
    class Meta:
        verbose_name = "Postagem"
        verbose_name_plural = "Postagens"

    blog = models.ForeignKey(MicroBlog, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentarios = models.ManyToManyField(Comentario, blank=True)

    def QtdComentarios(self):
        return len(list(self.comentarios.all()))
    
    def QtdDeCurtidas(self):
        return len(list(Curtir.objects.filter(post__id=self.pk)))

    def __str__(self):
        return f"postagem: blog - ID[{self.blog.pk}] de {self.autor.nome}"


class Curtir(models.Model):
    
    post = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.autor.nome} curtiu post [ID: {self.post.pk}] de {self.post.autor.nome}"
    