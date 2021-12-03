from django.shortcuts import redirect
from config import redirect_auth_url

def redirect_activation(request):
    uid = str(request.GET.get("uid", ""))
    token = str(request.GET.get("token", ""))
    return redirect(redirect_auth_url.format(uid=uid, token=token))