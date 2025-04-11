from django.shortcuts import render
from .models import Post, Photo, Comment
from django.http import JsonResponse, HttpResponse
from .forms import PostForm, CommentForm
from profiles.models import Profile
from .utils import action_permission
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.

@login_required
def post_list_and_create(request):
    form = PostForm(request.POST or None)
    # qs = Post.objects.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if form.is_valid():
            author = Profile.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            return JsonResponse({
                'title': instance.title,
                'body': instance.body,
                'author': instance.author.user.username,
                'id': instance.id,
            })

    context = {
        'form': form,
    }

    return render(request, 'posts/main.html', context)

@login_required
def post_detail(request, pk):
    obj = Post.objects.get(pk=pk)
    form = PostForm()
    comment_form = CommentForm()
    comments = obj.comments.all()

    context = {
        'obj': obj,
        'form': form,
        'comment_form': comment_form,
        'comments': comments,
    }

    return render(request, 'posts/detail.html', context)

@login_required
def load_post_data_view(request, num_posts):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        visible = 3
        upper = num_posts
        lower = upper - visible
        size = Post.objects.all().count()

        qs = Post.objects.all()
        data = []
        for obj in qs:
            item = {
                'id': obj.id,
                'title': obj.title,
                'body': obj.body,
                'liked': True if request.user in obj.liked.all() else False,
                'count': obj.like_count,
                'author': obj.author.user.username
            }
            data.append(item)
        return JsonResponse({'data':data[lower:upper], 'size': size})
    return redirect('posts:main-board')

@login_required
def post_detail_data_view(request, pk):
    obj = Post.objects.get(pk=pk)
    data = {
        'id': obj.id,
        'title': obj.title,
        'body': obj.body,
        'author': obj.author.user.username,
        'avatar': obj.author.avatar.url,
        'logged_in': request.user.username,
    }
    return JsonResponse({'data': data})

@login_required
def like_unlike_post(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        pk = request.POST.get('pk')
        obj = Post.objects.get(pk=pk)
        if request.user in obj.liked.all():
            liked = False
            obj.liked.remove(request.user)
        else:
            liked = True
            obj.liked.add(request.user)
        return JsonResponse({'liked': liked, 'count': obj.like_count})
    return redirect('posts:main-board')

@login_required
@action_permission
def update_post(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_title = request.POST.get('title')
        new_body = request.POST.get('body')
        obj.title = new_title
        obj.body = new_body
        obj.save()
        return JsonResponse({
            'title': new_title,
            'body': new_body,
    })
    return redirect('posts:main-board')

@login_required
@action_permission
def delete_post(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        obj.delete()
        return JsonResponse({'msg': 'access denied - AJAX only'})
    return redirect('posts:main-board')

@login_required
def image_upload_view(request):
    # print(request.FILES)
    if request.method == 'POST':
        img = request.FILES.get('file')
        new_post_id = request.POST.get('new_post_id')
        post = Post.objects.get(id=new_post_id)
        Photo.objects.create(image=img, post=post)
    return HttpResponse()

@login_required
def create_comment(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        post = Post.objects.get(pk=pk)
        body = request.POST.get('body')
        new_comment = Comment.objects.create(
            post=post,
            user=request.user,
            body=body
        )
        return JsonResponse({
            'body': new_comment.body,
            'created': new_comment.created.strftime('%B %d, %Y'),
            'username': new_comment.user.username,
            'profile_pic': new_comment.user.profile.avatar.url,
        })
    return redirect('posts:post-detail', pk=pk)