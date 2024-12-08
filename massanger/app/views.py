from django.contrib.auth.hashers import make_password, check_password
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import base64
from django.views.decorators.csrf import csrf_exempt
def index(request):
    return render(request, 'index.html')
def ajaxReg(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        if len(login) <= 5:
            return HttpResponse('1')
        if len(password) <= 5:
            return HttpResponse('2')
        if User.objects.filter(login = login).exists():
            return HttpResponse('3')
        user = User()
        user.login = login
        user.password = make_password(password)
        user.save()
        return HttpResponse('4')
def ajaxAuth(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        if User.objects.filter(login = login).exists():
            user = User.objects.filter(login = login).first()
            if check_password(password, user.password):
                request.session['user'] = login
                return HttpResponse('1')
            else:
                return HttpResponse('2')
        else:
            return HttpResponse('3')

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('/')

def profile(request):
    if not 'user' in request.session:
        return redirect('/')
    error = ''
    if 'error' in request.session:
        error =  request.session['error']
        del  request.session['error']

    user = User.objects.filter(login=request.session['user']).first()
    chats = Chat.objects.filter(admin=user)
    return render(request, 'lk/settings.html', {'error': error, 'user': user, 'chats': chats})

def update_password(request):
    if not 'user' in request.session:
        return redirect('/')
    if request.method == 'POST':
        old_password = request.POST['password_old']
        new_password = request.POST['password_new']
        user = User.objects.filter(login=request.session['user']).first()
        if check_password(old_password, user.password):
            user.password = make_password(new_password)
            user.save()
        else:
            request.session['error'] = 'Password error!'
    return redirect('/profile')
def update_avatar(request):
    if not 'user' in request.session:
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.filter(login=request.session['user']).first()
        path = ''
        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            fs.save('users_avatar/'+file.name, file)
            path = 'users_avatar/' + file.name
        if path != '':
            user.avatar = path
            user.save()
    return redirect('/profile')

def create_chat(request):
    if not 'user' in request.session:
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.filter(login=request.session['user']).first()
        chat = Chat()

        title = request.POST['title']
        description = request.POST['description']
        path = ''
        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            fs.save('chats_avatar/' + file.name, file)
            path = 'chats_avatar/' + file.name
        if path != '':
            chat.avatar = path

        chat.name = title
        chat.description = description
        chat.admin = user
        chat.save()
    return redirect('/profile')

def chat_id_chta(request, id_chat):
    user = User.objects.filter(login=request.session['user']).first()
    chats = Chat.objects.filter(admin=user)
    chat = Chat.objects.filter(id=id_chat).first()
    messages = Message.objects.filter(chat=chat)
    return render(request, 'lk/chat.html', {'user': user, 'chats': chats, 'chat': chat,'messages': messages})


def ajaxAddMessage(request):
    if request.method == 'POST':

        print(request.FILES)

        text = request.POST['message'];
        chat = Chat.objects.filter(id=request.POST['chat']).first();
        user = User.objects.filter(login=request.session['user']).first()

        message = Message()
        message.text = text
        message.user = user
        message.chat = chat
        message.save()
        return HttpResponse('Ok')
    return HttpResponse('Error method')


@csrf_exempt
def ajaxAddAudio(request):
    if request.method == 'POST':
        text = request.POST['message'];
        chat = Chat.objects.filter(id=request.POST['chat']).first();
        user = User.objects.filter(login=request.session['user']).first()
        file = request.POST['file']
        file_data = file.split(';base64,')[1]
        file_content = base64.b64decode(file_data)

        m = Message()
        m.text = text
        m.user = user
        m.chat = chat
        m.file.save(request.POST['filename'], ContentFile(file_content))
        m.save()
        res = '''<div class="message" style="text-align: right">
                        <span class="user">'''+m.user.login+'''</span>
                         <br> 
                        <span class="text">
                            
                               <audio id="audioPlayback" src="/media/'''+ str(m.file)+'''"  controls></audio>
                            <br>
                            

                        </span>
                        <span class="datetime">'''+str(m.create_at)+'''</span>
                    </div>'''

        return HttpResponse(res)


