from http.client import HTTPException

from celery import shared_task
from kavenegar import KavenegarAPI
from rest_framework.exceptions import APIException

from accounts.models import OtpCode
from ippanel import Client


@shared_task
def send_otp_code(phone_number,otp_code):
    """
        get user phone number and send otp code to it
        :param phone_number: user phone number that stored in session
        :param otp_code: a random code
        :return: error or a dictionary
        """
    try:
        api = KavenegarAPI('7935305551545963626D6E3844415A44397755554F49644D6E593148664641622B5257337130482B6565593D')
        params = {
            'receptor': f'{phone_number}',
            'template': 'tv7',
            'token': f'{otp_code}',
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


@shared_task
def remove_otp_code(id):
    """
    get an instance primary key and remove it
    :param id: otpCode instance primary key
    :return: None
    """
    try:
        instance=OtpCode.objects.get(id=id)
        instance.delete()
    except:
        pass