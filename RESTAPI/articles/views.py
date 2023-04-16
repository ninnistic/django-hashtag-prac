from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
# Json response
from django.http.response import JsonResponse, HttpResponse
from django.core import serializers
from .models import Article
# serializers import
from .serializers import ArticleSerializer


# Create your views here.
def article_html(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/article.html', context)

# Json Response로 돌려주기


def article_json_1(request):
    articles = Article.objects.all()
    articles_json = []
    for article in articles:
        articles_json.append(
            {
                'id': article.pk,
                'title': article.title,
                'content': article.content
            }
        )
    return JsonResponse(articles_json, safe=False)

# django.core import serializers


def article_json_2(request):
    articles = Article.objects.all()
    data = serializers.serialize('json', articles)
    return HttpResponse(data, content_type='application/json')

# DRF는 decorator 붙여줘야 한다. 요청 방식도 명시
# .serializers 에서 ArticleSerializer import 해온다.


@api_view(['GET'])
def article_json_3(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

# single-model 활용하기


@api_view(['GET'])
def article_list(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
