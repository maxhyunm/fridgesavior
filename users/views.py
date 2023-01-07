from json.decoder import JSONDecodeError
import requests
import logging

from django.conf import settings
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


logger = logging.getLogger('my_log')

state = getattr(settings, 'STATE')
BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'users/google/callback/'
KAKAO_CALLBACK_URI = BASE_URL + 'users/kakao/callback/'


# def google_login(request):
#     scope = "https://www.googleapis.com/auth/userinfo.email"
#     client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
#     return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?"
#                     f"client_id={client_id}&response_type=code&"
#                     f"redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")
#
#
# def google_callback(request):
#     client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
#     client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
#     code = request.GET.get('code')
#
#     token_req = requests.post(
#         f"https://oauth2.googleapis.com/token?client_id={client_id}&"
#         f"client_secret={client_secret}&code={code}&grant_type=authorization_code&"
#         f"redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     access_token = token_req_json.get('access_token')
#
#     email_req = requests.get(
#         f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
#     email_req_status = email_req.status_code
#     if email_req_status != 200:
#         return JsonResponse({'message': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
#     email_req_json = email_req.json()
#     email = email_req_json.get('email')
#
#     try:
#         user = User.objects.get(email=email)
#
#         social_user = SocialAccount.objects.get(user=user)
#         if social_user is None:
#             return JsonResponse({'message': 'not a social user'}, status=status.HTTP_400_BAD_REQUEST)
#         if social_user.provider != 'google':
#             return JsonResponse({'message': 'social type error'}, status=status.HTTP_400_BAD_REQUEST)
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}users/google/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'message': 'failed to signin'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
#     except User.DoesNotExist:
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}users/google/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'message': 'failed to signup'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)


def kakao_login(request):
    # code 요청
    logger.info('kakao login 진입')
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&'
        f'redirect_uri={KAKAO_CALLBACK_URI}&response_type=code'
    )


def kakao_callback(request):
    # 액세스 토큰 요청 -> 로그인 정보 요청
    logger.info('kakao login - callback 진입')
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    code = request.GET.get('code')
    redirect_uri = KAKAO_CALLBACK_URI

    token_res = requests.get(
        f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&'
        f'client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}')
    token_res_json = token_res.json()

    error = token_res_json.get('error')
    if error is not None:
        logger.info('kakao login - token request error')
        raise JSONDecodeError(error)

    access_token = token_res_json.get('access_token')

    profile_res = requests.get(
        'https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {access_token}'})
    profile_res_json = profile_res.json()

    social_id = profile_res_json.get('id')
    kakao_account = profile_res_json.get('kakao_account')
    email = kakao_account.get('email')

    user = User.objects.filter(email=email)
    if not user.exists():
        try:
            username = kakao_account.get('profile').get('nickname')
        except:
            logger.info('kakao login - no username error')
            return JsonResponse({'message': 'need a username'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            email=email,
            username=username,
            social_provider='KAKAO',
            social_id=social_id,
            social_detail=profile_res_json
        )
    else:
        user = user.get()
    social_provider = user.social_provider
    if social_provider is None:
        logger.info('kakao login - not a social user error')
        return JsonResponse({'message': 'not a social user'}, status=status.HTTP_400_BAD_REQUEST)
    elif social_provider != 'KAKAO':
        logger.info('kakao login - not a kakao user error')
        return JsonResponse({'message': 'social type error'}, status=status.HTTP_400_BAD_REQUEST)

    token = TokenObtainPairSerializer.get_token(user)
    access = str(token.access_token)
    refresh = str(token)

    return JsonResponse({'message': 'Logged In',
                         'access_token': access,
                         'refresh_token': refresh})

