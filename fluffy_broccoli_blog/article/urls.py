from django.urls import path
from article.views import ArticleView
from django.conf.urls import url
app_name = "articles"


urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>', ArticleView.as_view()),
]
