from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quotes
from django.contrib import messages
import datetime
import bcrypt
now = datetime.datetime.now()

def index(request):
    return render(request, 'black_app/index.html')

def home(request):
    if request.session['uname']:
        userr = User.objects.filter(first_name=request.session["uname"]).last()
        context = {
            'favs': userr.quotes_set.all(),
            'others': Quotes.QuoteManager.exclude(owned_by=userr)
        }
        return render(request, 'black_app/home.html', context)
    else:

        context = {
            'items': Quotes.QuoteManager.all()
        }
        return render(request, 'black_app/home.html', context)

def register(request):
    fname = str(request.POST['first_name'])
    lname = str(request.POST['last_name'])
    email = str(request.POST['email'])
    pwd = request.POST['password'].encode()
    conpwd = request.POST['confirm_password'].encode()
    context = {
    "fname" : fname,
    "lname" : lname,
    "email" : email,
    "pwd" : pwd,
    "conpwd" : conpwd
    }
    if  User.objects.all().filter(email = email):
        messages.add_message(request, messages.INFO, "Email already exists! Please login")
        return redirect('/')
    error = User.objects.validate(context)
    if error:
        for ele in error:
            messages.add_message(request, messages.ERROR, ele)
        return redirect('/')
    else:
        hashedpwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
        user = User.objects.create(first_name = fname, last_name = lname, email = email, password = hashedpwd)
        request.session['uid'] = user.id
        request.session['uname'] = user.first_name
    return render(request, "black_app/home.html")

def login(request):
    email = str(request.POST['email'])
    pwd = request.POST['password'].encode()
    user = User.objects.all().filter(email = email)
    if  not user:
        messages.add_message(request, messages.INFO, "Email doesn't exist! Please register")
        return redirect('/')
    else:
        if user[0].password != bcrypt.hashpw(pwd, (user[0].password).encode()):
            messages.add_message(request, messages.INFO, "Invalid password")
            return redirect('/')
        else:
            request.session['uid'] = user[0].id
            request.session['uname'] = user[0].first_name
    return render(request, "black_app/home.html")

def addQuote(request):
    if request.session["uname"]:
        user = User.objects.filter(first_name=request.session["uname"]).last()
        quoted_by = request.POST.get("quoted_by")
        newMsg = request.POST.get("message_in")
        info = Quotes.QuoteManager.addQuote(quoted_by, newMsg, user)
        if info[0] is True:
            return redirect('/home')
        else:
            if Quotes.QuoteManager.validquoted_by(quoted_by):
                messages.error(request, 'At least 3 characters', extra_tags='quoted_by')

            if Quotes.QuoteManager.validmessage(newMsg):
                messages.error(request, 'Message is not long enough. At least 10 characters', extra_tags='message')
            return redirect('/home')

def Quote(request, created_by):
    allquotes = Quotes.QuoteManager.filter(created_by=created_by)
    context = {
        'author': created_by,
        'quotes': allquotes,
        'count': len(allquotes)
    }
    return render(request, 'black_app/quotes.html', context)


def addremove(request):
    if request.session["uname"]:
        user = User.objects.filter(first_name=request.session["uname"]).last()
        if request.POST and request.POST.get("addMe"):
            quoteId = request.POST.get("addMe")
            newFav = Quotes.QuoteManager.get(id=quoteId)
            newFav.owned_by.add(user)
        elif request.POST and request.POST.get("deleteMe"):
            print "Aysun"
            quoteId = request.POST.get("deleteMe")
            newFav = Quotes.QuoteManager.get(id=quoteId)
            newFav.owned_by.remove(user)
        return redirect('/home')


def logout(request):
    request.session.clear()
    return redirect('/')
