from django.shortcuts import render
from .mdoels import Article


def search(request, query):
    if request.method == "GET":
        query = request.GET.get('query', None)
        if query:
            results = Article.objects.filter(title__icontains=query | content__icontains=query)
            context = {'results':results}
            return render(request, 'article-search.html', context)