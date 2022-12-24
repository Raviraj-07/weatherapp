from datetime import date, datetime, timedelta
from django.shortcuts import render
from .models import Account, VerificationEmail
import random
import string
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    username = request.data.get("email")
    password = request.data.get("password")
    email = request.data.get("email")
    first_name = request.data.get("first_name")

    if username is None or password is None or\
            email is None or first_name is None:
        return Response(
            {'error': 'Please provide username, password, email, first_name'},
            status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'User with same email already exists'},
                        status=HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=email,
        email=email,
        first_name=first_name,
        password=password
    )

    account = Account.objects.create(
        user=user
    )

    SendVerifcation(user)

    return Response({'status': 'A verification email is sent'},
                    status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def emailverification(request):
    data = request.GET
    token = data.get('token', None)
    uuid = data.get('uniqid', None)

    if not token or not uuid:
        pass

    account = Account.objects.get(uuid=uuid)
    now = datetime.now()
    verifications = VerificationEmail.objects.filter(
        account=account,
        token=token,
        expires_at__gte=now,
        is_verified=False
        )

    if verifications.exists():
        verifications.update(is_verified=True)
        account.is_verified = True
        account.verified_at = datetime.now()
        account.save()

        return render(request, 'verified.html')
    else:
        return render(request, 'verification_issue.html')


def SendVerifcation(user):
    user = user
    email = user.email
    uuid = user.account.uuid
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    expire_time = datetime.now() + timedelta(minutes=settings.LINK_EXPIRE_TIME)

    VerificationEmail.objects.create(
        account=user.account,
        token=token,
        expires_at=expire_time
    )

    host = settings.CURRENT_HOST
    link = '{}/verify?token={}&uniqid={}'.format(host, token, uuid)

    msg_html = render_to_string(
        'emailverification.html',
        {'name': user.first_name, 'href': link}
    )

    send_mail(
        message=msg_html,
        subject='Email verification',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=msg_html,
    )

    return True
