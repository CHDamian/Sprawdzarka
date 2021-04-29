from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from .models import Uzytkownicy, Zadania, Wysylki
import hashlib
import os
import binascii
import json


'''
Funkcje pomocnicze
'''

# Funkcja hashująca #

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


# Funkcja porównująca #

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


'''
Funkcje główne
'''

# Strona z logowaniem #

def index(request):
    return render(request, 'Tester/index.html')


# Do tworzenia użytkownika #

def new_account(request):
    return render(request, 'Tester/new_account.html')


# Do strony głównej zalogowanego #

def my_page(request):
    if 'logged_user' not in request.session:
        return redirect('index')
    return render(request, 'Tester/my_page.html', {'user_id': request.session['logged_user']})


# Do strony z linkami do zadań #

def tasks(request):
    if 'logged_user' not in request.session:
        return redirect('index')

    # Tabela do zadań
    data = []
    try:
        zadanka = Zadania.objects.all().order_by('trudnosc')
        for e in zadanka:
            # Dla każdego wyciągamy dane, pakujemy je w słownik i do data
            task_url = 'Tester/tasks/' + e.identyfikator + '/text.pdf'
            data.append({'id': task_url,
                         'name': e.nazwa,
                         'diff': e.trudnosc})
        context = {'data': data}
        return render(request, 'Tester/tasks.html', context)
    except:
        return redirect('index')


# Do strony, gdzie można wysłać rozwiązanie #

def send(request):
    if 'logged_user' not in request.session:
        return redirect('index')

    # Tabela do zadań
    data = []
    try:
        # Dla każdego wyciągamy dane, pakujemy je w słownik i do data
        for e in Zadania.objects.all():
            data.append({'id': e.identyfikator,
                         'name': e.nazwa})
        context = {'data': data}
        return render(request, 'Tester/send.html', context)
    except:
        return redirect('index')


# Tworzenie raportu nowego rozwiązania (tylko po make_tests) #

def make_raport(request, context, task):
    # Przygotowanie danych
    data = timezone.now()
    raport = json.dumps(context)
    try:
        Wysylki.objects.create(zadanie=Zadania.objects.get(identyfikator=task),
                               uzytkownik=Uzytkownicy.objects.get(identyfikator=request.session['logged_user']),
                               data=data,
                               raport=raport)
        return render(request, 'Tester/raport.html', context)
    except:
        return redirect('my_page')


# Odczytanie raportu z bazy #

def read_raport(request, id):
    if 'logged_user' not in request.session:
        return redirect('index')
    try:
        # Wyciągamy i patrzymy, czy rozwiązanie należy do użytkownika
        sol=Wysylki.objects.get(pk=id)
        if not sol.uzytkownik.identyfikator == request.session['logged_user']:
            return redirect('my_page')

        # Odkodowanie
        context = json.loads(sol.raport)
        return render(request, 'Tester/raport.html', context)
    except:
        return redirect('my_page')


# Tworzenie listy wysyłek użytkownika #

def solutions(request):
    if 'logged_user' not in request.session:
        return redirect('index')
    try:
        user = Uzytkownicy.objects.get(identyfikator=request.session['logged_user'])
        sol = Wysylki.objects.filter(uzytkownik=user)
        context = {'user_sol': []}
        for e in sol:
            # Każdą wysyłke opakowujemy
            context['user_sol'].append({'id': e.pk,
                                        'task': e.zadanie.nazwa,
                                        'data': e.data})
        return render(request, 'Tester/solutions.html', context)
    except:
        return redirect('my_page')


'''
Funkcje Przygotowujące (każda redirectuje bądź odpala pod koniec nową)
'''


# Wylogowanie #

def logout(request):
    try:
        del request.session['logged_user']
    finally:
        return redirect('index')


# Logowanie #

def login(request):
    if request.POST and request.POST['login'] and request.POST['password']:
        log = request.POST['login']
        passw = request.POST['password']
        if len(log) < 1 or len(log) > 16 or len(passw) < 6 or len(passw) > 16:
            return redirect('index')
        try:
            result = Uzytkownicy.objects.get(identyfikator=log)
            if not result:
                return redirect('index')
            if verify_password(result.haslo, passw):
                request.session['logged_user'] = log
                return redirect('my_page')
            else:
                return redirect('index')
        except Uzytkownicy.DoesNotExist:
            return redirect('index')
    else:
        return redirect('index')


# Dodawanie nowego użytkownika #

def add_account(request):
    if request.POST and request.POST['login'] and request.POST['password']:
        log = request.POST['login']
        passw = request.POST['password']
        if len(log) < 1 or len(log) > 16 or len(passw) < 6 or len(passw) > 16:
            return redirect('new_account')
        try:
            try:
                catcher = Uzytkownicy.objects.get(identyfikator=log)
                return redirect('new_account')
            except Uzytkownicy.DoesNotExist:
                Uzytkownicy.objects.create(identyfikator=log, haslo=hash_password(passw))
                return redirect('index')
        except:
            return redirect('new_account')

    else:
        return redirect('new_account')


# Testowanie #

def make_tests(request):
    if 'logged_user' not in request.session:
        return redirect('index')
    try:
        if request.method == 'POST' and request.FILES['fileToUpload'] and request.POST['taskID']:

            # Przygotuj plik
            uploaded = request.FILES['fileToUpload']
            fs = FileSystemStorage()
            if fs.exists('plik.cpp'):
                fs.delete('plik.cpp')
            fs.save('plik.cpp', uploaded)
            context = {'compile': 0,
                       'raport':[]}

            # Kompilacja
            exit_code = os.system('g++ -o media/program.exe media/plik.cpp > media/program.err')
            if exit_code:
                context['compile'] = exit_code

            else:
                # Adresy pomocnicze
                test_url = 'Tester\\static\\Tester\\tasks\\' + request.POST['taskID'] + '\\tests\\'
                out_url = 'media\\testOut.out'

                # Testowanie
                for i in range(1, 6):
                    to_raport = 'Test ' + str(i) + ': '
                    tin_url = test_url + str(i) + '.in'
                    tout_url = test_url + str(i) + '.out'

                    exit_code = os.system('media\\program.exe < ' + tin_url + ' > ' + out_url)
                    if exit_code:
                        err = to_raport + 'ERROR ' + str(exit_code)
                        context['raport'].append(err)

                    else:
                        # Porównanie
                        exit_code = os.system('FC /w ' + out_url + ' ' + tout_url + ' >program.err')
                        if not exit_code:
                            to_raport = to_raport + 'PASSED'
                        else:
                            to_raport = to_raport + 'FAILED'
                        context['raport'].append(to_raport)

            return make_raport(request, context, request.POST['taskID'])

    except:
        return redirect('my_page')

