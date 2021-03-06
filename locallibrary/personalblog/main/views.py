import random

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.apps import apps
from django.utils import timezone
import datetime

from django.utils.timesince import timesince
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from .forms import EditPostForm, EditWorkForm, CommentForm, CreateLittlePostForm
from .models import Post, Stories, Work, ArticleTypeHeader, ArticlesType, Comment
from django.core.paginator import Paginator
from django.views import generic

from .templatetags.main_tags import time_filter

Profile = apps.get_model('accounts', 'Profile')


class Index(generic.ListView, FormView):
    model = Post
    form_class = CreateLittlePostForm
    paginate_by = 5
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stories_list'] = Stories.objects.all()
        context['form'] = CreateLittlePostForm()

        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.status = 'l'
        post.title = 'None'
        isbn = random.randint(1, 1000000000000)
        post = Post.objects.all()

        post.isbn = isbn
        post.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

    def get_queryset(self):
        return Post.objects.filter(status__in=['a', 'l'])


class PostDisplay(generic.DetailView):
    model = Post
    message = ''
    message_color = ''
    template_name = 'main/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.model.objects.get(id=self.kwargs['pk'])

        context['posts_list'] = Post.objects.filter(articles_type=post.articles_type, status='a')[:5]
        context['comments'] = post.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        context['comment_user'] = User.objects.filter(username=post.comments.name)
        context['message'] = self.message
        context['message_color'] = self.message_color

        return context


class PostComment(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'main/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        all_comments = []
        post = Post.objects.get(id=self.kwargs['pk'])

        for i in post.comments.filter(name=self.request.user.username):
            all_comments.append(i.created_on.strftime("%m/%d/%Y, %H:%M:%S"))

        if not len(all_comments) >= 10:
            comment = form.save(commit=False)
            comment.post = self.object
            comment.name = self.request.user.username
            comment.profile_photo = self.request.user.profile.avatar_photo

            # Save the comment to the database
            comment.save()
        else:
            pass
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post-detail', kwargs={'pk': post.pk})

    def get_queryset(self):
        return Post.objects.filter(status='a')


class PostDetailView(generic.View):

    def get(self, request, *args, **kwargs):
        all_comments = []
        post = Post.objects.get(id=self.kwargs['pk'])

        for i in post.comments.filter(name=request.user.username):
            all_comments.append(i.created_on.strftime("%m/%d/%Y, %H:%M:%S"))
            if self.request.user.is_staff:
                i.read = True
                i.save()

        if len(all_comments) >= 10:
            view = PostDisplay.as_view(message=request.session.get('message'), message_color=request.session.get('message_color'))

        else:
            view = PostDisplay.as_view(message=request.session.get('message', ''), message_color=request.session.get('message_color'))

            request.session['message'] = ''

        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        all_comments = []
        post = Post.objects.get(id=self.kwargs['pk'])

        for i in post.comments.filter(name=request.user.username):
            all_comments.append(i.created_on.strftime("%m/%d/%Y, %H:%M:%S"))
        if len(all_comments) >= 10:
            request.session['message'] = '?????? ?????????? ???? ?????? ??????????????????, ???????????????? ???????????????????? ??????????'
            request.session['message_color'] = 'red'
        else:
            request.session['message'] = '?????? ?????????? ???????????????? ??????????????????'
            request.session['message_color'] = 'yellow'

        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'main/post_update.html'


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'main/post_delete.html'


class AboutMeView(generic.TemplateView):
    template_name = 'main/about_me.html'


class WorkListView(generic.ListView):
    model = Work
    template_name = 'main/works.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WorkListView, self).get_context_data(*args, **kwargs)
        context['tag_list'] = (o.name for o in Work.tags.all())
        return context


class WorkUpdateView(generic.UpdateView):
    model = Work
    template_name = 'main/work_update.html'
    form_class = EditWorkForm

    def get(self, request, *args, **kwargs):
        self.initial = {'tags': u", ".join(tag.name for tag in Work.objects.get(pk=self.get_object().id).tags.all())}
        return super(WorkUpdateView, self).get(request, *args, **kwargs)


class SearchProfileByUsernameDetailView(generic.DetailView):
    template_name = 'accounts/profile_detail.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProfileByUsernameDetailView, self).get_context_data(*args, **kwargs)
        user1 = User.objects.get(username=self.kwargs['username'])
        context['main_user'] = self.request.user
        context['profile_object'] = Profile.objects.all().filter(user=user1)
        return context


class ArticleTypeHeaderListView(generic.ListView):
    model = ArticlesType
    template_name = 'main/articlestype_list.html'

    def get_queryset(self):
        article_type_header = get_object_or_404(ArticleTypeHeader, link=self.kwargs.get('articles_type'))
        return ArticlesType.objects.filter(article_type_header=article_type_header)
