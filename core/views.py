from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
import random

@login_required(login_url='signin')
def index(request):
    user_object =  User.objects.get(username=request.user.username)
    profile_object = Profile.objects.get(user=user_object)
    
    # Generating the feed - start
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(following_user=request.user.username)

    for users in user_following:
        user_following_list.append(users.followed_user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))

    # user suggestion - start
    all_users = []
    all_following = []

    for user in list(User.objects.all()):
        if user.username == 'admin':
            continue
        all_users.append(Profile.objects.get(user=user))

    for user in list(user_following):  # user_following used above
        all_following.append(Profile.objects.get(user=User.objects.get(username=user.followed_user)))  # append the profile of the users in the user_following list
    
    new_suggestion_list = [x for x in all_users if x not in all_following and x != profile_object]
    random.shuffle(new_suggestion_list)

    return render(request, 'index.html', {'profile_object': profile_object, 'posts': feed_list, 'new_suggestion_list': new_suggestion_list[:4]})

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') is None:
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        elif request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
    
        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profile})

# Upload Posts
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
       user = request.user.username
       image = request.FILES.get('image_upload')
       caption = request.POST['caption']

       new_post = Post.objects.create(user=user, image=image, caption=caption)
       new_post.save()

    return redirect('/')

@login_required(login_url='signin')
def follow(request, profile_user):
    follower = request.user.username
    followed = profile_user

    followed_count = FollowersCount.objects.filter(following_user=follower, followed_user=followed).first()

    if followed_count is None:
        new_follower = FollowersCount.objects.create(following_user=follower, followed_user=followed)
        new_follower.save()
        
    else:
        followed_count.delete()

    return redirect('/profile/' + followed)  # profile/username url will take the username and display the corresponding profile page

@login_required(login_url='signin')
def search(request):
    # To display current user information
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # Returning searched users
    if request.method == 'POST':
        username = request.POST['username']
        username_objects = User.objects.filter(username__icontains=username)

        username_profile_list = []

        for user in username_objects:
            username_profile_list.append(Profile.objects.filter(id_user=user.id))

        username_profile_list = list(chain(*username_profile_list))        

    return render(request, 'search.html', {'user_profile': user_profile, 'username': username, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    # Check if following
    follower = request.user.username
    followed = pk

    if FollowersCount.objects.filter(following_user=follower, followed_user=followed).first() is None:
        button_text = 'Follow'
    else:
        button_text = 'Unfollow'

    # Followers and Following
    user_following = len(FollowersCount.objects.filter(following_user=pk))
    user_followers = len(FollowersCount.objects.filter(followed_user=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_following': user_following,
        'user_followers': user_followers,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 and password != '':

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        elif password == '' or password2 == '':
            messages.info(request, 'Cannot have empty password')
            return redirect('signup')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')