from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from article.models import Article
from article.serializers import ArticleSerializer
from rest_framework.generics import get_object_or_404


class ArticleView(APIView):

    def get(self, request, pk=None):
        """
        Возвращает статью или список статей.
        :param request:
        :param pk:
        :return: Response({"articles": serializer.data})
        """
        if pk is None:
            articles = Article.objects.all()
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
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)
