from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ad, Category
from django.contrib.auth.models import User
from accounts.models import Author
from django.core.paginator import Paginator
from .forms import AdForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class AdsList(ListView):
    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'
    queryset = Ad.objects.order_by('-creation_datetime')
    paginate_by = 10


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad_detail'
    queryset = Ad.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_anonymous:
            context['is_author'] = False
        else:
            context['is_author'] = Ad.objects.get(id=self.kwargs["pk"]).author.user == \
                                   User.objects.get(username=user)
        return context


class AdAdd(PermissionRequiredMixin, CreateView):
    """
    После регистрации пользователям становится доступно создание и редактирование объявлений
    """
    template_name = 'ad_add.html'
    form_class = AdForm
    permission_required = ('ads.add_ad')

    def form_valid(self, form):
        self.new_ad = form.save(commit=False)
        self.new_ad.author = Author.objects.get(user=self.request.user)
        self.new_ad.save()
        categories_names = []
        # for category in form.cleaned_data.get('category'):
        #             categories_names += [category.category]
        # news_notify.delay(categories_names, self.new_ad.id)
        return super(AdAdd, self).form_valid(form)


class AdUpdate(PermissionRequiredMixin, UpdateView):
    """
    После регистрации пользователям становится доступно создание и редактирование объявлений
    """
    template_name = 'ad_add.html'
    form_class = AdForm
    permission_required = ('ads.change_ad')

    def get_object(self, **kwargs):
        # метод get_object мы используем вместо queryset, чтобы получить 
        # информацию об объекте который мы собираемся редактировать
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)


class AdDelete(PermissionRequiredMixin, DeleteView):
    """
    После регистрации пользователям становится доступно создание и редактирование объявлений
    """
    template_name = 'ad_delete.html'
    context_object_name = 'ad'
    queryset = Ad.objects.all()
    success_url = '/ads/'
    permission_required = ('ads.delete_ad')
