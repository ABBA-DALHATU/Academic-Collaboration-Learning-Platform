from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q #this import is a method that allows us to add and/ or into our search filter
from django.contrib.auth.decorators import login_required #this import is used to restrict page unless you login
from .models import Room, Topic, Message, Resource, Res, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Gamers talk'},
# ]

def loginPage(request): #do not call this function 'login' cuz there is a builtin function called login
    page = 'login' # this is just so that we can render the correct form from the 'login_register.html


    if request.user.is_authenticated: # this is for when a logged in user tries to go the the login page again using the url searcher
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error('lol go and register lil bro')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password is incorrect")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)# i have to look at how the logout function actually works
    return redirect('home')


def registerPage(request):
    # page = 'register' #since its an if else statement in the login_register.html we can comment out this

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        print(form)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registeration')


    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    # rooms = Room.objects.all()

    # q = request. GET.get('q') if request.GET.get('q') != None else ''# not mine, mine is below

    q = request.GET.get('q')

    if q != None:
        q = request.GET.get('q')
    else:
        q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
        )# the __ represents . and also the i the icontains just means its case insensitive
    

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(room__topic__name__icontains=q)

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages[0:5]}
    return render(request, 'base/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    # room_messages = room.message_set.all().order_by('-created') # so this queries from bottom up for example this iis like saying 'message.room' but instead it get all the messages related to a specific room
    room_messages = room.message_set.all() #i comment that last room_message because i can actually make the ordering general from our model
    participants = room.participants.all()

    if request.method == 'POST':
        # if not request.POST.get('body'):
        #     context = {'room': room, 'room_messages': room_messages, 'participants': participants}
        #     return render(request, 'base/room.html', context) 
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if the user is not authenticated
        
        message = Message.objects.create(
            user = request.user, 
            room = room,
            body = request.POST.get('body'),
            document=request.FILES.get('document', None),
            video=request.FILES.get('video', None)
        )
        room.participants.add(request.user)#this is for adding any user that messages in a room as a participant in that room
        return redirect('room', pk)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def resource(request, pk):
    resource = Resource.objects.get(id=pk)
    # room_messages = room.message_set.all().order_by('-created') # so this queries from bottom up for example this iis like saying 'message.room' but instead it get all the messages related to a specific room
    resource_res = resource.res_set.all() #i comment that last room_message because i can actually make the ordering general from our model

    if request.method == 'POST':
        res = Res.objects.create(
            user = request.user,
            resource = resource,
            document=request.FILES.get('document', None),
            video=request.FILES.get('video', None)
        )
        return redirect('resource', pk)

    context = {'resource': resource, 'resource_res': resource_res}
    return render(request, 'base/resource.html', context)

@login_required(login_url='login')
def deleteResource(request, pk):

    room = Resource.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        room.delete()    
        return redirect('user-profile', request.user.id)

    context = {'obj': room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')#if the a user isnt logged in and he/she tries to create a room he gets redirected to the login page
def createResource(request):
    user_id = request.user.id
    form = RoomForm

    if request.method == 'POST':
        form = RoomForm(request.POST)

        Resource.objects.create(
            host=request.user,
            name= request.POST.get('name'),
            description= request.POST.get('description'),
        )
        return redirect('user-profile', user_id)

        
    context = {'form': form}
    return render(request, 'base/resource_form.html', context)

@login_required(login_url='login')
def updateResource(request, pk):

    resource = Resource.objects.get(id=pk)
    form = RoomForm(instance=resource)

    if request.user != resource.host: #this is so that a user can delete another users room from the url search directly. like 'localhost/room/edit/3'
        return HttpResponse('you are not allowed here')


    if request.method == 'POST':

        resource.name = request.POST.get('name')
        resource.description = request.POST.get('description')
        resource.save()
        return redirect('resource', resource.id)
    context = {'form': form, 'resource': resource}
    return render(request, 'base/resource_form.html', context)


@login_required(login_url='login')
def deleteRes(request, pk):
    roomMessage = Res.objects.get(id=pk)

    obj = roomMessage.video

    if request.method == 'POST':
        roomMessage.delete()
        return redirect('resource', roomMessage.resource.id)
    
    context = {'roomMessage': roomMessage, 'obj': obj}
    return render(request, 'base/delete.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    resources = user.resource_set.all()
    
    rooms = user.room_set.all()


    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'resources': resources}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')#if the a user isnt logged in and he/she tries to create a room he gets redirected to the login page
def createRoom(request):
    # form = RoomForm
    # # Room.host = request.user # lol im not meant to handle the auto assigne

    # topics = Topic.objects.all()

    # if request.method == 'POST':
    #     form = RoomForm(request.POST)
    #     if form.is_valid():
    #         room = form.save(commit=False)
    #         room.host = request.user
    #         room.save()
    #         return redirect('home')

        
    # context = {'form': form, 'topics': topics}
    # return render(request, 'base/room_form.html', context)

    form = RoomForm
    # Room.host = request.user # lol im not meant to handle the auto assigne

    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name= request.POST.get('name'),
            description= request.POST.get('description'),
        )
        return redirect('home')

        
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):

    # room = Room.objects.get(id=pk)
    # form = RoomForm(instance=room)

    # topics = Topic.objects.all()

    # if request.user != room.host: #this is so that a user can delete another users room from the url search directly. like 'localhost/room/edit/3'
    #     return HttpResponse('you are not allowed here')


    # if request.method == 'POST':
    #     form = RoomForm(request.POST, instance=room)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    # context = {'form': form, 'topics': topics}
    # return render(request, 'base/room_form.html', context)

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host: #this is so that a user can delete another users room from the url search directly. like 'localhost/room/edit/3'
        return HttpResponse('you are not allowed here')


    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        room.delete()    
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    roomMessage = Message.objects.get(id=pk)
    room_id = roomMessage.room.id  # Get the ID of the room associated with the message

    obj = roomMessage.body

    if request.method == 'POST':
        roomMessage.delete()
        return redirect('room', pk=room_id)  # Redirect back to the room page using the room ID

    
    context = {'roomMessage': roomMessage, 'obj': obj}
    return render(request, 'base/delete.html', context)




@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)


    return render(request, 'base/update-user.html', {'form': form})

    
def topicPage(request):
    q = request.GET.get('q')

    if q != None:
        q = request.GET.get('q')
    else:
        q = ''
    
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})