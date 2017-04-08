# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
from django import forms
from django.dispatch import receiver
from django.http import HttpResponse
from hashlib import sha256
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Страница купить
def buy(request):
	return render(request, 'django-robokassa/sys.html')

# Формирование запроса для оплаты
def popoln(request):
	mrh_login = "Ваш id"
	mrh_pass1 = "Ваш пароль 1"
	inv_id  = "1"
	inv_desc  = "Покупка"
	out_summ  = "50.00"
	#Формирование контрольной суммы
	result_string = "{}:{}:{}:{}".format(mrh_login, out_summ, inv_id, mrh_pass1)
	sign_hash = sha256(result_string.encode())
	crc = sign_hash.hexdigest().upper()
	url = "https://auth.robokassa.ru/Merchant/Index.aspx?MrchLogin={}&OutSum={}&InvId={}&Desc={}&SignatureValue={}"
		.format(mrh_login, out_summ, inv_id, inv_desc, crc)
	if request.method == "POST":
		#К примеру запись в талицу пополнения

		#Переход на страницу оплаты в робокасса
		return redirect(url)
	return render(request, 'django-robokassa/popln.html')

#Проверка плотежа
@csrf_exempt
def res(request):
	if not request.method == 'POST':
		return HttpResponse('error')
	mrh_pass2 = "Ваш пароль 2"
    #Проверка заголовка авторизации
	if request.method == 'POST':
		out_summ = request.POST['OutSum']
		inv_id = request.POST['InvId']
		crc = request.POST['SignatureValue']
		crc = crc.upper()
		crc = str(crc)
		#Формирование своей контрольной суммы
		result_string = "{}:{}:{}".format(out_summ, inv_id, mrh_pass2)
		sign_hash = sha256(result_string.encode())
		my_crc = sign_hash.hexdigest().upper()
		#Проверка сумм
		if my_crc not in crc:
			# Ответ ошибки
			context = "bad sign"
			return HttpResponse(context)
		else:
			#Ответ все верно
			context = "OK{}".format(inv_id)
			return HttpResponse(context)

#Платеж принят
@csrf_exempt
def success(request):
	if not request.method == 'POST':
		return HttpResponse('error')
	mrh_pass1 = "Ваш пароль 1"
    #Проверка заголовка авторизации
	if request.method == 'POST':
		out_summ = request.POST['OutSum']
		inv_id = request.POST['InvId']
		crc = request.POST['SignatureValue']
		crc = crc.upper()
		crc = str(crc)
		#Формирование своей контрольной суммы
		result_string = "{}:{}:{}".format(out_summ, inv_id, mrh_pass1)
		sign_hash = sha256(result_string.encode())
		my_crc = sign_hash.hexdigest().upper()
		#Проверка сумм
		if my_crc not in crc:
			#Ошибка
			context = "bad sign"
			return HttpResponse(context)
		else:
			#Показ страницы успешной оплаты
			return render(request, 'django-robokassa/success.html')

#Платеж не принят
@csrf_exempt
def fail(request):
	if request.method == "POST":
		return render(request, 'django-robokassa/fail.html')
