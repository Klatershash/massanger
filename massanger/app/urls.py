from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('ajaxReg', ajaxReg),
    path('ajaxAuth', ajaxAuth),
    path('logout', logout),
    path('profile', profile),
    path('update_password', update_password),
    path('update_avatar',update_avatar),
    path('create_chat', create_chat),
    path('chat/<int:id_chat>', chat_id_chta),
    path('ajaxAddMessage', ajaxAddMessage),
    path('ajaxAddAudio', ajaxAddAudio)
]

