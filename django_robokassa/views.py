# -*- coding: utf-8 -*-
from hashlib import sha256
from typing import Union

from django.http import (HttpResponse, HttpResponsePermanentRedirect)
from django.shortcuts import (render, redirect)
from django.views.decorators.csrf import csrf_exempt


def buy(request) -> HttpResponse:
    """Страница купить"""
    return render(request, 'django-robokassa/sys.html')


def popoln(request) -> Union[HttpResponsePermanentRedirect, HttpResponse]:
    """Формирование запроса для оплаты"""
    mrh_login = "Ваш id"
    mrh_pass1 = "Ваш пароль 1"
    inv_id = "1"
    inv_desc = "Покупка"
    out_amount = "50.00"
    # Формирование контрольной суммы
    result_string = f'{mrh_login}:{out_amount}:{inv_id}:{mrh_pass1}'
    sign_hash = sha256(result_string.encode())
    crc = sign_hash.hexdigest().upper()
    url: str = (
        f"https://auth.robokassa.ru/Merchant/Index.aspx"
        f"?MrchLogin={mrh_login}&OutSum={out_amount}&InvId={inv_id}&Desc={inv_desc}&SignatureValue={crc}"
    )
    if request.method == "POST":
        # К примеру запись в талицу пополнения
        # Переход на страницу оплаты в робокасса
        return redirect(to=url)
    return render(request, 'django-robokassa/popln.html')


# Проверка плотежа
@csrf_exempt
def res(request) -> HttpResponse:
    if not request.method == 'POST':
        return HttpResponse('error')
    mrh_pass2 = "Ваш пароль 2"
    # Проверка заголовка авторизации
    out_amount = request.POST['OutSum']
    inv_id = request.POST['InvId']
    crc = request.POST['SignatureValue']
    crc = crc.upper()
    crc = str(crc)
    # Формирование своей контрольной суммы
    result_string = f'{out_amount}:{inv_id}:{mrh_pass2}'
    sign_hash = sha256(result_string.encode())
    my_crc = sign_hash.hexdigest().upper()
    # Проверка сумм
    if my_crc not in crc:
        # Ответ ошибки
        context: str = "bad sign"
    else:
        # Ответ все верно
        context: str = f"OK{inv_id}"
    return HttpResponse(context)


@csrf_exempt
def success(request) -> HttpResponse:
    """Платеж принят"""
    if not request.method == 'POST':
        return HttpResponse('error')
    mrh_pass1 = "Ваш пароль 1"
    # Проверка заголовка авторизации
    out_amount = request.POST['OutSum']
    inv_id = request.POST['InvId']
    crc = request.POST['SignatureValue']
    crc = crc.upper()
    crc = str(crc)
    # Формирование своей контрольной суммы
    result_string = f'{out_amount}:{inv_id}:{mrh_pass1}'
    sign_hash = sha256(result_string.encode())
    my_crc = sign_hash.hexdigest().upper()
    # Проверка сумм
    if my_crc not in crc:
        # Ошибка
        context: str = "bad sign"
        return HttpResponse(context)
    else:
        # Показ страницы успешной оплаты
        return render(request, 'django-robokassa/success.html')


@csrf_exempt
def fail(request) -> HttpResponse:
    """Платеж не принят"""
    if request.method == "POST":
        return render(request, 'django-robokassa/fail.html')


__all__ = (
    'buy',
    'popoln',
    'res',
    'success',
    'fail',
)
