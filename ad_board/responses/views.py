from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ads.models import Ad, Category
from .models import Response
from django.contrib.auth.models import User
from accounts.models import Author
from django.core.paginator import Paginator
from .forms import ResponseForm
from .filters import ResponseFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect

@login_required
def response_accept(request, *args, **kwargs):
    id = kwargs["pk"]
    response = Response.objects.get(id=id)
    response.status = 'ACP'
    response.save()
    return redirect(f'/responses/{id}/')


class ResponseSearch(PermissionRequiredMixin, ListView):
    """
    Пользователю должна быть доступна приватная страница с откликами на его
    объявлния, внутри которой он может фильтровать отклики по объявлениям, 
    удалять их и принимать
    """
    model = Response
    template_name = 'responses/responses_search.html'
    context_object_name = 'responses_search'
    queryset = Response.objects.all().order_by('-creation_datetime')
    permission_required = ('responses.view_response')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.queryset = Response.objects.filter(ad__author__user=self.request.user).order_by('-creation_datetime')
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ResponseDetail(PermissionRequiredMixin, DetailView):
    model = Response
    template_name = 'responses/response_detail.html'
    context_object_name = 'response_detail'
    queryset = Response.objects.all()
    permission_required = ('responses.view_response')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_ad_author'] = Response.objects.get(id=self.kwargs["pk"]).ad.author.user == \
                               User.objects.get(username=self.request.user)
        return context


class ResponseAdd(PermissionRequiredMixin, CreateView):
    """
    Пользователи могут отправлять отклики на объявления других пользователей, состоящие из простого текста
    """
    template_name = 'responses/response_add.html'
    form_class = ResponseForm
    permission_required = ('responses.add_response')

    def form_valid(self, form):
        self.new_response = form.save(commit=False)
        self.new_response.author = Author.objects.get(user=self.request.user)
        self.new_response.ad = Ad.objects.get(id=self.kwargs["pk"])
        self.new_response.save()
        categories_names = []
        # for category in form.cleaned_data.get('category'):
        #             categories_names += [category.category]
        # news_notify.delay(categories_names, self.new_ad.id)
        return super(ResponseAdd, self).form_valid(form)


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'responses/response_delete.html'
    context_object_name = 'response'
    queryset = Response.objects.all()
    success_url = '/responses/'
    permission_required = ('responses.delete_response')
