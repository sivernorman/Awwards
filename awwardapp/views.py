from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Profile,Projects,Comments,Ratings
from django.contrib.auth.models import User
from .forms import NewProjectForm,CommentForm,EditProfileForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Create your views here.
# @login_required(login_url = '/accounts/login/')
def index(request):

    all_projects = Projects.all_projects()
    return render(request,'awwardapp/index.html',{'all_projects':all_projects})

@login_required(login_url = '/accounts/login/')
def profile(request):

    all_projects = Projects.objects.filter(user = request.user)
    return render(request,'profile.html',{'all_projects':all_projects})


@login_required(login_url = '/accounts/login/')
def new_project(request):
    form = NewProjectForm
    if request.method=='POST':
        form = NewProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            return redirect('home')

    else:
        form = NewProjectForm()
    return render(request,'awwardapp/new_project.html',{'form':form})


@login_required(login_url = '/accounts/login/')
def search_results(request):

    if 'project' in request.GET and request.GET['project']:
        search_term = request.GET.get('project')
        searched_projects = Projects.search_project(search_term)
        message = f'{search_term}'

        return render(request,'search.html',{'message':message,'project':searched_projects})

    else:
        message = 'You have not entered anything to search'
        return render(request,'search.html',{'message':message})


@login_required(login_url = '/accounts/login/')
def comment(request,id):
    id = id
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.user = request.user
            project = Projects.objects.get(id = id)
            comment.project_id = project
            comment.save()
            return redirect('home')

        else:
            project_id = id
            messages.info(request,'MAke sure you fill all the fields')
            return redirect('comment',id = project_id)

    else:
        id = id
        form = CommentForm()
        return render(request,'comment.html',{'form':form,'id':id})


@login_required(login_url = '/accounts/login/')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')

    else:
        form = EditProfileForm(request.POST,request.FILES)
    return render(request,'update_profile.html',{'form':form})


@login_required(login_url = '/accounts/login/')
def single_project(request,id):  

    project = Projects.objects.get(id = id)
    comments = Comments.objects.filter(project_id = id)
    rates = Ratings.objects.filter(project_id = id)
    designrate = []
    usabilityrate = []
    contentrate = []
    if rates:
        for rate in rates:
            designrate.append(rate.design)
            usabilityrate.append(rate.usability)
            contentrate.append(rate.content)

        total = len(designrate)*10
        design = round(sum(designrate)/total*100,1)
        usability = round(sum(usabilityrate)/total*100,1)
        content = round(sum(contentrate)/total*100,1)
        return render(request,'single_project.html',{'project':project,'comments':comments,'design':design,'usability':usability,'content':usability})

    else:
        design = 0
        usability = 0
        content = 0       

        return render(request,'single_project.html',{'project':project,'comments':comments,'design':design,'usability':usability,'content':usability})


@login_required(login_url = '/accounts/login/')
def rate(request,id):
    if request.method =='POST':
        rates = Ratings.objects.filter(id = id)
        for rate in rates:
            if rate.user == request.user:
                messages.info(request,'You cannot rate a project twice')
                return redirect('singleproject',id)
        design = request.POST.get('design')
        usability = request.POST.get('usability')
        content = request.POST.get('content')

        if design and usability and content:
            project = Projects.objects.get(id = id)
            rate = Ratings(design = design,usability = usability,content = content,project_id = project,user = request.user)
            rate.save()
            return redirect('singleproject',id)

        else:
            messages.info(request,'Input all fields')
            return redirect('singleproject',id)


    else:
        messages.info(request,'Input all fields')
        return redirect('singleproject',id)
        
 
@login_required(login_url="/accounts/login/")
def logout_request(request):
  '''
  Function for logging out user
  '''

  logout(request)
  return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = 'awwardapp/register_form.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home ')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(*args, *kwargs)