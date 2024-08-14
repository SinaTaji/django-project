from Lib.django.http.response import JsonResponse
from django.db.models import Prefetch
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from site_setting.models import SiteBanner
from .forms import CommentForm
from .models import Article, ArticleCategory, ArticleComment


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 20
    context_object_name = 'article_list'

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        query = query.order_by('-create_date')
        category_name = self.kwargs.get('category')
        if category_name:
            query = query.filter(selected_category__url_title__iexact=category_name)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.Position.articles)
        return context


def article_category_component(request):
    MainCategory = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,
                                                                                          category_id=None)
    context = {'main_category': MainCategory}
    return render(request, 'article_component/article_category_component.html', context)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article-detail/article_detail.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None,
                                                            is_active=True).prefetch_related(
            Prefetch('articlecomment_set', queryset=ArticleComment.objects.filter(is_active=True)))
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id,is_active=True).count()
        return context


@csrf_exempt
def add_article_comment(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            response = {
                'status': 'success',
                'message': 'نظر شما با موفقیت ثبت شد و پس از بازبینی منتشر خواهد شد'
            }
        else:
            response = {
                'status': 'error',
                'message': 'فرم معتبر نیست',
                'errors': form.errors.as_json()
            }
        return JsonResponse(response)
    else:
        return JsonResponse({'status': 'error', 'message': 'روش ارسال پشتیبانی نمی‌شود یا کاربر احراز هویت نشده است'})
