from django.shortcuts import render, redirect, get_object_or_404
from .models import Image, Profile, Follow, Comment
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm, ProfileForm,ProfileUpdateForm, UserUpdateForm, ImageUploadForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from itertools import chain
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        profForm=ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profForm.is_valid():
            username=form.cleaned_data.get('username')
            user=form.save()
            profile=profForm.save(commit=False)
            profile.user=user
            profile.save()

            messages.success(request, f'Successfully created Account!.You can now login as {username}!')
        return redirect('login')
    else:
        form= RegistrationForm()
        profForm=ProfileForm()
    context={
        'form':form,
        'profForm': profForm
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        useForm=UserUpdateForm(request.POST, instance=request.user)
        profForm=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if useForm.is_valid() and profForm.is_valid():
            useForm.save()
            profForm.save()
            messages.success(request, f'Your account has been updated!')
        return redirect('profile')
    
    else:
        useForm=UserUpdateForm(instance=request.user.profile)
        profForm=ProfileUpdateForm(instance=request.user.profile)

    context={
        'useForm':useForm,
        'profForm':profForm
    }

    return render(request, 'users/profile.html', context)

def index(request):
    context={
        'posts':Image.objects.all(),
        'comments': Comment.objects.filter(image_id).all()
    }

    return render(request, 'index.html', context)
class PostListView(ListView):
    model = Image
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']

class UserListView(ListView):
    model=Profile
    template_name='posts/view.html'
    context_object_name='posts'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)
        
class ProfileDetailView(DeleteView):
    model=Profile
    template_name='main/profile.html'
    context_object_name='posts'

    def get_object(self, **kwargs):
        pk=self.kwargs.get('pk')
        avi=Profile.objects.get(pk=pk)
        return avi
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        avi=self.get_object()
        myProf=Profile.objects.get(user=self.request.user)
        if avi.user in myProf.following.all():
            follow=True
        else:
            follow=False
        context["follow"]=follow
        return context

class PostDetailView(DetailView):
    model = Image
    template_name= 'posts/image_detail.html'

    def get_context_data(self, *args, **kwargs):
        context=super(PostDetailView, self).get_context_data(*args, **kwargs)
        stuff=get_object_or_404(Image, id=self.kwargs['pk'])
        total_likes=stuff.total_likes()
        context["total_likes"]=total_likes
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Image
    fields = ['image', 'caption', 'name']
    template_name='posts/postForm.html'
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Image
    fields = ['image', 'caption', 'name']
    template_name='posts/postForm.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    success_url = '/'
    template_name= 'posts/delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False


def about(request):
    return render(request, 'about.html', {'title': 'About'})

@login_required
def comment(request,id):
    comments= Comment.objects.filter(image_id=id).all()
    images=Image.objects.filter(id=id)
    current_user = request.user
    user_profile = Profile.objects.get(user = current_user)
    image = get_object_or_404(Image, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.image_id = image
            comment.user_id = user_profile
            comment.save()
            return redirect('gram-landing')
    else:
        form = CommentForm()
    return render(request,'posts/comment.html',{"form":form, "images":images, "comments":comments})
@login_required
def searchprofile(request): 
    if 'searchUser' in request.GET and request.GET['searchUser']:
        name = request.GET.get("searchUser")
        searchResults = Profile.search_profile(name)
        message = f'name'
        params = {
            'results': searchResults,
            'message': message
        }
        return render(request, 'main/search.html', params)
    else:
        message = "You haven't searched"
    return render(request, 'main/search.html', {'message': message})
@login_required
def follow_unfollow(request, pk):
    if request.method=='POST':
        my_profile=Profile.objects.get(user=request.user)
        pk= request.POST.get('profile_pk')
        obj=Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile-details')


def posts_following(request):
    profile= Profile.objects.get(user=request.user)
    users=[user for user in profile.following.all()]
    posts=[]
    qs=None

    for u in users:
        p=Profile.objects.get(user=u)
        p_posts=p.profiles_posts()
        posts.append(p_posts)
    
    my_posts=profile.profiles_posts()
    posts.append(my_posts)
    if len(posts)>0:
        qs= sorted(chain(*posts), reverse=True, key=lambda obj: obj.pub_date)
    return render(request, 'main/main.html', {"posts":qs, "profile":profile})

def like_image(request, pk):
    post= get_object_or_404(Image, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
