from datetime import tzinfo

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseGone
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.text import slugify
from django.views.generic import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
                                    HTTP_204_NO_CONTENT

from .models import Articles

# Put all functions view right here
from .serializers import ArticleSerializer


def delete_article(request, *args, **kwargs):
    id_ = kwargs.get('id')
    article = Articles.objects.get(pk=id_)
    if article is not None:
        article.delete()
    return redirect(to=reverse(viewname='blog:dashboard:list-articles'))


def edit_article(request, *args, **kwargs):
    template_name = 'blog/add-article.html'
    # particular article base on its slugify title
    slug_title = kwargs.get('title')
    article = Articles.objects.get(slug=slug_title)
    if article.owner == request.user:
        context = {'editing_article': article}
        return render(request=request, template_name=template_name, context=context)
    return redirect(to='blog:dashboard:view-article', title=slug_title)


def view_article(request, **kwargs):
    template_name = 'blog/readonly-article.html'
    # particular article base on its slugify title
    slug_title = kwargs.get('title')
    article = Articles.objects.get(slug=slug_title)
    context = {
        'title': article.title,
        'html': article.html.replace('<html>', '')
            .replace('<head>', '')
            .replace('</html>', '')
            .replace('</head>', '')
            .replace('<body>', '')
            .replace('</body>', '')
            .replace('contenteditable="true"', 'contenteditable="false"')
    }
    return render(request=request, template_name=template_name, context=context)


def tweak_sharing_article(request):
    uuid = request.GET['uuid']
    share = request.GET['share']
    Articles.objects.filter(uuid__exact=uuid).update(is_shareable=True if share == 'true' else False)
    return HttpResponseGone()


# Put all class-based view right below
class ListArticles(View):
    template_name = 'blog/list-articles.html'

    def get(self, request, *args, **kwargs):
        articles = Articles.objects.filter(owner__username=request.user).values(
            'uuid', 'title', 'publish_date', 'slug', 'is_shareable', 'owner__username'
        ).order_by('publish_date')
        return render(request=request, template_name=self.template_name, context={
            'articles': articles
        })


class CreateArticle(PermissionRequiredMixin, View):
    permission_required = ('blog.add_articles', 'blog.change_articles')
    permission_denied_message = 'Bạn không có quyền làm hành động này'

    template_name = 'blog/add-article.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        html = request.POST.get('html')
        add_new = request.POST.get('add-new')
        uuid = request.POST.get('uuid')
        if uuid != "":
            try:
                article = Articles.objects.get(pk=uuid)
                setattr(article, 'title', title)
                setattr(article, 'content', content)
                setattr(article, 'html', html)
                setattr(article, 'slug', slugify(title))
                article.save()
            except Exception as e:
                pass
        else:
            if title and content is not None:
                Articles.objects.create(
                    title=title,
                    content=content,
                    html=html,
                    owner=request.user,
                )
        if add_new:
            return redirect(to=reverse(viewname='blog:dashboard:add-article'))
        return redirect(to=reverse(viewname='blog:dashboard:edit-article', kwargs={'title': slugify(value=title)}))


@api_view(['GET'])
def search_post(request, format=None):
    try:
        text_search = request.GET['text_search']
    except MultiValueDictKeyError:
        return HttpResponse(content='<b>Không có ?text_search=</b>', status=400)
    results = Articles.objects.filter(
        Q(title__icontains=text_search) & (Q(owner__username=request.user) | Q(is_shareable=True)))
    for result in results:
        result.publish_date = result.publish_date.astimezone().strftime('%d/%m/%Y, %H:%M:%S %P %A')
    json_results = ArticleSerializer(instance=results, many=True)
    return Response(data=json_results.data)


@api_view(['GET'])
def get_content_quick_view(request, *args, **kwargs):
    try:
        uuid = request.GET['uuid']
        article = Articles.objects.values('title', 'html', 'slug').get(uuid__exact=uuid)
        return Response(data=article)
    except ObjectDoesNotExist:
        return Response(data=None, status=HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return HttpResponse(content='<b>Không có ?uuid=</b>', status=400)


@api_view(['GET'])
def list_all_articles(request, format=None):
    all_articles = Articles.objects.all().order_by('-publish_date')
    limit = request.query_params.get('limit')
    serializers = None
    if limit is not None:
        serializers = ArticleSerializer(all_articles[:int(limit)], many=True)
    else:
        serializers = ArticleSerializer(all_articles, many=True)
    return Response(data={'articles': serializers.data}, status=HTTP_200_OK)


@api_view(['GET'])
def get_an_article(request, uuid=None):
    an_article = Articles.objects.get(pk=uuid)
    serializer = ArticleSerializer(an_article)
    return Response(data={'article': serializer.data}, status=HTTP_200_OK)


@api_view(['POST'])
def update_or_create_an_article(request):

    def has_one_is_none(*args):
        for arg in args:
            if arg is None:
                return True
        return False

    try:
        uuid = request.POST.get('uuid')
        title = request.POST.get('title')
        content = request.POST.get('content')
        html = request.POST.get('html')
        owner = request.POST.get('owner')
        if has_one_is_none(title, content, html, owner):
            return Response(data={'success': False}, status=HTTP_400_BAD_REQUEST)

        _, created = Articles.objects.update_or_create(
            defaults={
                'title': title,
                'content': content,
                'html': html,
                'owner': User.objects.get(id=owner)
            }, uuid=uuid
        )
        if created:
            return Response(data={'success': True, 'created': True}, status=HTTP_201_CREATED)
        else:
            return Response(data={'success': True, 'update': True}, status=HTTP_200_OK)
    except Exception as e:
        return Response(data={'success': False, 'extra': 'Không thể tạo hoặc chỉnh sửa'}, status=HTTP_400_BAD_REQUEST)


@api_view(['delete', 'put', 'get'])
def delete_the_article(request, uuid=None):
    an_article = Articles.objects.get(pk=uuid)
    an_article.delete()
    return Response(data={'deleted': True}, status=HTTP_204_NO_CONTENT)
