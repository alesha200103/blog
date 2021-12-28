from django.urls import path
from article.views import ArticleView, CommentView, LikesView
from django.conf.urls import url
app_name = "articles"


urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>', ArticleView.as_view()),
    path('comments/<int:article_id>', CommentView.as_view()),
    path('like/<int:article_id>', LikesView.as_view()),
]
