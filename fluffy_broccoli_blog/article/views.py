from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from article.models import Article, Comment, Likes
from article.serializers import ArticleSerializer, CommentSerializer, LikeSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import permissions, generics
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User
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
            category = request.GET.get("category", None)
            in_title = request.GET.get("in_title", None)
            in_description = request.GET.get("in_description", None)
            in_text = request.GET.get("in_text", None)

            articles = Article.objects.order_by("created_at" if sort == "asc" else "-created_at")
            if category is not None:
                articles = articles.filter(category=category)
            if author_id != 0:
                articles = articles.filter(author=author_id)

            if in_title is not None:
                articles = articles.filter(title__icontains=in_title)
            elif in_description is not None:
                articles = articles.filter(Q(title__icontains=in_description) |
                                           Q(description__icontains=in_description))
            elif in_text is not None:
                articles = articles.filter(Q(body__icontains=in_text) |
                                           Q(title__icontains=in_text) |
                                           Q(description__icontains=in_text))

            if limit != 0:
                articles = articles[offset:offset+limit]

            if len(articles) == 0:
                return Response(status=204)

            serializer = ArticleSerializer(articles, many=True)
            response_data = serializer.data
            articles_lst = []
            for i in response_data:
                user = User.objects.get(id=i["author_id"])
                comments = Comment.objects.filter(article=i["id"])
                i["author_name"] = user.username
                i["comments_count"] = len(comments)
                articles_lst.append(i)
            return Response({"articles": articles_lst})

        else:
            article = get_object_or_404(Article.objects.all(), pk=pk)
            serializer = ArticleSerializer(article)
            response_data = serializer.data
            comments = Comment.objects.filter(article=response_data["id"])
            user = User.objects.get(id=response_data["author_id"])
            response_data["author_name"] = user.username
            response_data["comments_count"] = len(comments)
            return Response({"articles": response_data})

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
        if request.user.id != saved_article.author_id and not ArticleView.DEBUG:
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
        if request.user.id != article.author_id and not ArticleView.DEBUG:
            return Response({
                "detail": "Нет прав на удаление."
            }, status=403)
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)


class LikesView(generics.ListAPIView):
    DEBUG = False
    permission_classes = [permissions.AllowAny if DEBUG else permissions.IsAuthenticated]

    def put(self, request, article_id):
        """
        Добавляет/убирает лайк.
        :param request:
        :param article_id:
        :return: Response({"likes_count": article.likes_count}, status=200)
        """
        user = request.user.id
        article = get_object_or_404(Article.objects.all(), id=article_id)
        likes = Likes.objects.filter(article=article.id).first()
        if likes is None:
            like_serializer = LikeSerializer(data={
                "article_id": article.id,
                "users_id": f"{user}"
            })
            if like_serializer.is_valid(raise_exception=True):
                like_serializer.save()
        else:
            if str(" " + likes.users_id + " ").find(" " + str(user) + " ") == -1:
                likes.users_id = (likes.users_id + f" {user}").strip()
                likes.save(update_fields=["users_id"])
                like_serializer = LikeSerializer(likes)
            else:
                likes.users_id = str(" " + likes.users_id + " ").replace(" " + str(user) + " ", " ").strip()
                likes.save(update_fields=["users_id"])
                like_serializer = LikeSerializer(likes)

        article.likes_count = len(like_serializer.data['users_id'].split())
        article.save(update_fields=["likes_count"])
        return Response({"likes_count": article.likes_count}, status=200)

    def get(self, request, article_id):
        """
        Проверяет поставил ли текущий пользователь лайк.
        :param request:
        :param article_id:
        :return: Response({"likes_count": article.likes_count}, status=200)
        """
        article = get_object_or_404(Article.objects.all(), id=article_id)
        likes = Likes.objects.filter(article=article.id).first()
        if likes is not None and (" " + likes.users_id + " ").find(" " + str(request.user.id) + " ") !=-1:
            return Response({"is_liked": True}, status=200)
        else:
            return Response({"is_liked": False}, status=200)


class CommentView(generics.ListAPIView):

    DEBUG = False
    permission_classes = [permissions.AllowAny if DEBUG else permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, article_id):
        """
        Возвращает список комментариев к статье.
        :param request:
        :return: Response({"articles": serializer.data})
        """
        comments = Comment.objects.filter(article=article_id).order_by("-created_at")
        if len(comments) == 0:
            return Response({"detail": "Комментариев нет."}, status=204)
        serializer = CommentSerializer(comments, many=True)
        comments_lst = []
        for i in serializer.data:
            user = User.objects.get(id=i["author_id"])
            i["author_name"] = user.username
            comments_lst.append(i)
        return Response({"comments": comments_lst})

    def post(self, request, article_id):
        """
        Создаёт комментарий.
        :param request:
        :param article_id:
        :return: Response({"comment": comment_saved.data})
        """
        comment = request.data.get('comment')
        comment["article_id"] = article_id
        if len(Article.objects.filter(id=comment["article_id"])) == 0:
            return Response({"detail": "Неверные данные."}, status=400)

        serializer = CommentSerializer(data=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"detail": "Неверные данные."})

        user = User.objects.get(id=serializer.data["author_id"])
        response_data = serializer.data
        response_data["author_name"] = user.username
        return Response({"comment": response_data})
