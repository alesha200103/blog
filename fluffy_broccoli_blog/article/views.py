from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from article.models import Article, Comment
from article.serializers import ArticleSerializer, CommentSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import permissions, generics
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Q
from rest_framework.authtoken.models import Token



class ArticleView(generics.ListAPIView):
    DEBUG = False
    permission_classes = [permissions.AllowAny if DEBUG else permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        """
        Возвращает статью или список статей.
        :param request:
        :param pk:
        :return: Response({"articles": serializer.data})
        """
        if pk is None:
            limit = int(request.GET.get("limit", 0))
            offset = int(request.GET.get("offset", 0))
            sort = request.GET.get("sort", "asc")
            author_id = int(request.GET.get("author_id", 0))
            in_title = request.GET.get("in_title", None)
            in_description = request.GET.get("in_description", None)
            in_text = request.GET.get("in_text", None)

            articles = Article.objects.order_by("created_at" if sort == "asc" else "-created_at")
            if author_id != 0:
                articles = articles.filter(author=author_id)
            if limit != 0:
                articles = articles[offset:offset+limit]

            if in_title is not None:
                articles = articles.filter(title__icontains=in_title)
            elif in_description is not None:
                articles = articles.filter(Q(title__icontains=in_description) |
                                           Q(description__icontains=in_description))
            elif in_text is not None:
                articles = articles.filter(Q(body__icontains=in_text) |
                                           Q(title__icontains=in_text) |
                                           Q(description__icontains=in_text))

            if len(articles) == 0:
                return Response({"detail": "Страница не найдена."}, status=404)

            serializer = ArticleSerializer(articles, many=True)
            return Response({"articles": serializer.data})

        else:
            article = get_object_or_404(Article.objects.all(), pk=pk)
            serializer = ArticleSerializer(article)
            return Response({"articles": serializer.data})

    def post(self, request):
        """
        Создаёт статью и возвращает, сообщение успешно ли она была создана.
        :param request:
        :return: Response({"success": "Article '{}' created successfully".format(article_saved.title)})
        """
        article = request.data.get('article')
        serializer = ArticleSerializer(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(article_saved.title)})

    def put(self, request, pk):
        """
        Редактирует статью и возвращает, сообщение успешно ли она была отредактирована.
        :param request:
        :param pk:
        :return: Response({
            "success": "Article '{}' updated successfully".format(article_saved.title)
        })
        """
        saved_article = get_object_or_404(Article.objects.all(), pk=pk)
        data = request.data.get('article')
        if request.user.id != data["author_id"]:
            return Response({
                "detail": "Нет прав на редактирование."
            }, status=403)
        serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({
            "success": "Article '{}' updated successfully".format(article_saved.title)
        })

    def delete(self, request, pk):
        """
        Удаляет статью и возвращает сообщения, была ли статья успешно удалена.
        :param request:
        :param pk:
        :return: Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)
        """
        article = get_object_or_404(Article.objects.all(), pk=pk)
        if request.user.id != article.author_id:
            return Response({
                "detail": "Нет прав на удаление."
            }, status=403)
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)


class CommentView(generics.ListAPIView):

    DEBUG = True
    permission_classes = [permissions.AllowAny if DEBUG else permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, article_id):
        """
        Возвращает список комментариев к статье.
        :param request:
        :return: Response({"articles": serializer.data})
        """
        comments = Comment.objects.filter(article=article_id).order_by("-created_at")
        if len(comments) == 0:
            return Response({"detail": "Комментариев нет."}, status=404)
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    def post(self, request, article_id):
        """
        Создаёт комментарий.
        :param request:
        :return: Response({"success": "Comment for article {} created successfully".format(comment_saved.article_id)})
        """
        comment = request.data.get('comment')
        comment["article_id"] = article_id
        if len(Article.objects.filter(id=comment["article_id"])) == 0:
            return Response({"detail": "Неверные данные."}, status=400)

        serializer = CommentSerializer(data=comment)
        if serializer.is_valid(raise_exception=True):
            comment_saved = serializer.save()
        else:
            return Response({"detail": "Неверные данные."})
        return Response({"success": "Comment for article {} created successfully".format(comment_saved.article_id)})
