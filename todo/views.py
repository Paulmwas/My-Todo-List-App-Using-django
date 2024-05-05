from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import Task
from django.urls import reverse_lazy

# Create your views here.
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='tasks'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input= self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['search_input']= search_input
        return context    
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model= Task
class TaskCreate(LoginRequiredMixin,CreateView):
    model =Task
    fields= ['title', 'description','complete']
    success_url= reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    # TaskCreate, self
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model= Task
    fields=['title', 'description','complete']
    success_url=reverse_lazy('task')
class TaskDelete(LoginRequiredMixin,DeleteView):
    model= Task
    fields=['title', 'description','complete']
    success_url=reverse_lazy('task')
class customLoginveiw(LoginView):
    template_name= 'todo/login.html'
    field= '__all__'
    redirect_authenticated_user =False
    def get_success_url(self):
        return reverse_lazy('task')
    
class RegisterPage(FormView):
    template_name= 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user= False
    success_url= reverse_lazy('task')

    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, **kwargs)