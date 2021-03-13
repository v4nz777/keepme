from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import date,datetime
from .models import (
    User,
    Thing,
    TransactionLend,
    AgreeOrRejectTransaction,
    TransactionReturn,
    AgreeOrRejectReturn,
    Outcome
)

from .forms import (
    ThingForm,
    UpdateAvatarForm,
    TransactionLendForm,
    TransactionBorrowForm
)

####################################################################################################
#####################################       MAIN           #########################################
####################################################################################################
#### Global Variables



#### views...
def index(request):

    if request.user.is_authenticated:
        
        return render(request, 'index.html', {
            'current_user': request.user,
            'thing_form': ThingForm(),
            'update_avatar_form': UpdateAvatarForm(),
            'lend_form': TransactionLendForm(),
            'borrow_form': TransactionBorrowForm(),
            'objects': [obj for obj in Thing.objects.all()]
        })
    else:
        return HttpResponseRedirect(reverse('login'))


#### Sign In View..
def login_view(request):
    if request.method == "POST":
        # Attempt to Login
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Verify User
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            context={'login_notif': 'Invalid Username or Password!'}
            return render(request, 'login.html', context)
    
    # Get request of Login 
    return render(request, 'login.html')


#### Sign Out View...
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))




#### Sign Up View...
def register(request):
    if request.method == 'POST':
        # Getting the Details of the New User
        username = request.POST["username"]
        email = request.POST["email"]

        # Check if Password Matched
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            context = {"registration_notif": "The password you entered wont match each other..."}
            return render(request, "register.html", context)


        # Save the Details to the Database
        try:
            # & making sure the USERNAME and EMAIL are in lowerCase
            registration = User.objects.create_user(username.lower(), email.lower(), password)
            registration.save()
            
            return HttpResponseRedirect(reverse('login'))
            
        except IntegrityError:
            context = {"registration_notif": "Username already taken."}
            return render(request, "register.html", context)

    
    return render(request, "register.html")



#### ADD NEW ITEM
def add_new_item(request):
    if request.method == 'POST':

        thing_form = ThingForm(request.POST, request.FILES)
        
        if thing_form.is_valid():
            thing_form.instance.owner = request.user
            thing_form.save()
            return HttpResponseRedirect(reverse('index'))      
        else:
            return HttpResponseRedirect(reverse('index'), args={'error_alert': 'Enter Valid Credentials!'})
        
        return HttpResponseRedirect(reverse('index'))



#### OTHER PROFILES PAGE
def profile(request, user):
    profiles = []

    for profile in User.objects.filter(username=user).all():
        profiles.append(profile.username)

    if user in profiles:
        return render(request,'index.html', {
            'current_user':user,
            'thing_form': ThingForm(),
            'update_avatar_form': UpdateAvatarForm(),
            'borrow_form': TransactionBorrowForm(),
            'objects': [obj for obj in Thing.objects.all()]
        })
    else:
        return HttpResponse('404 NOT FOUND')

            

#### SEARCH OTHER USERS
def search(request):
    if request.method == "POST":
        query = request.POST["query"]
        context = {
            'results': [result for result in User.objects.filter(username__contains=query).all().order_by('username')],
            'query': 'All' if query == '' else query,
            'num_results': User.objects.filter(username__contains=query).count()
        }
        

        return render(request, 'search.html', context)

    return HttpResponseRedirect(reverse('index'))

#### CHANGE AVATAR
def change_avatar(request):
    if request.method == 'POST':
        update_avatar = UpdateAvatarForm(request.POST, request.FILES, instance=request.user)
        print(update_avatar)
        if update_avatar.is_valid():
            update_avatar.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('index'))


#### TRANSACT
def lend(request):
    if request.method == "POST":
        makelend = TransactionLendForm(request.POST)
        this_thing = Thing.objects.get(thing_name=request.POST['thing'])
        try:
            borrower = User.objects.get(username=request.POST['borrower'])
            print(makelend.instance.promised_return)
           # makelend.instance.promised_return = ('%Y-%m-%d %H:%M:%S')
            if makelend.is_valid(): 
                makelend.instance.thing = this_thing
                makelend.instance.borrower = borrower
                makelend.instance.lender = request.user
                makelend.save()
                print('succeed')
      
        except ObjectDoesNotExist:
            return HttpResponse('USER BORROWER NOT FOUND')
        print(makelend)
        return HttpResponseRedirect(reverse('index'))


def borrow(request):
    if request.method == "POST":
        # var for the form to submit
        req_borrow = TransactionBorrowForm(request.POST)
        try:
            this_thing = Thing.objects.get(thing_name=request.POST['req_thing'])
            owner = User.objects.get(username=request.POST['owner'])

            if req_borrow.is_valid():
                req_borrow.instance.thing = this_thing
                req_borrow.instance.borrower = request.user
                req_borrow.instance.owner = owner
                req_borrow.save()
                print('succeed')

        except ObjectDoesNotExist:
            return HttpResponse('USER BORROWER NOT FOUND')
        print(req_borrow)
        return HttpResponseRedirect(reverse('index'))

#AGREE OR REJECT THE OTHER USER'S REQUEST TO BORROW
@csrf_exempt
def agree_or_reject_trans(request, id):
    aort = AgreeOrRejectTransaction.objects.filter(owner=request.user, action="").count()
    aorr = AgreeOrRejectReturn.objects.filter(owner=request.user, action="").count()
    data = json.loads(request.body)
    action = data.get("action", "")
    print(action)
    for transaction in AgreeOrRejectTransaction.objects.filter(t_id=id):
        if request.method == "POST":  
            try:
                transaction.action = action
                transaction.save()
                print(id, f'SUCCEEDED TO {action}')
                print(action)
                print(AgreeOrRejectTransaction.objects.filter(owner=request.user, action="").count())
                return JsonResponse({
                    'id': id,
                    'success': True,
                    'message': action,
                    'lastnotif_count': aort + aorr
                    }, status=201)
            except:
                print(id, f'FAILED TO {action}')
                return JsonResponse({
                    'success': False,
                    'message': action}, status=201)

#AGREE OR REJECT THE OTHER USER'S REQUEST TO RETURN
@csrf_exempt
def agree_or_reject_ret(request, id):
    aort = AgreeOrRejectTransaction.objects.filter(owner=request.user, action="").count()
    aorr = AgreeOrRejectReturn.objects.filter(owner=request.user, action="").count()
    data = json.loads(request.body)
    action = data.get("action", "")
   # print(action)
    if request.method == "POST":  
        
        for transaction in AgreeOrRejectReturn.objects.filter(t_id=id):
            transaction.action = action
            transaction.save()
            #print(id, f'SUCCEEDED TO {action}')
           # print('HOOOYYYYYYYYYYYYYY', action)
            #print(AgreeOrRejectReturn.objects.filter(owner=request.user, action="").count())
            
        return JsonResponse({
            'id': id,
            'success': True,
            'message': 'action',
            'lastnotif_count': aorr + aort
            }, status=201)
      
                
            

@csrf_exempt
def return_borrowed(request, id):
    borrower = request.user
    thing = ''
        
    for i in Thing.objects.filter(pk=id):
        thing = i

    if request.method == "POST":
        data = json.loads(request.body)   
        TransactionReturn.objects.create(thing=thing, borrower=borrower)
        print('RETUUUUUUURN', data)

        for tr in TransactionReturn.objects.filter(thing=thing, borrower=borrower):
            context = {
                'thing': str(tr.thing),
                'thing_id': tr.thing.pk,
                'borrower': str(tr.borrower),
                'accepted': tr.accepted,
                'success': True,
                'from': 'POST'
            }
        return JsonResponse(context, status=201)

    elif request.method == "GET":   

        thing = ''
        for i in Thing.objects.filter(pk=id):
            thing = i
        for tr in TransactionReturn.objects.filter(thing=thing, borrower=borrower):
            context = {
                'thing': str(tr.thing),
                'thing_id': tr.thing.pk,
                'borrower': str(tr.borrower),
                'accepted': tr.accepted,
                'success': True,
                'from': 'GET'
            }
        return JsonResponse(context, status=201)

    




####################################################################################################
#####################################   VIEWS OF ALL    ############################################
#####################################   API RESPONSES   ############################################
####################################################################################################

#### Profile Overview Objects
def api_profile(request, user):
    
    # Making main context variable
    aort = AgreeOrRejectTransaction.objects.filter(owner=request.user, action="").count()
    aorr = AgreeOrRejectReturn.objects.filter(owner=request.user, action="").count()
    context = {
        "username": user,
        "status": "null",
        "reputation": "null",
        "notif_counts" : aort + aorr

    }

    #   GETTING OTHER VALUES AND ADDING TO CONTEXT
    user_id = ''
    for profile in User.objects.filter(username=user).all():
        context["username"] = profile.username
        context["email"] = profile.email
        context["address"] = profile.address
        context["reputation"] = profile.reputation

        user_id = profile.pk
        context["user_id"] = user_id

        # generate avatar pic | USE DEFAULT IF NO IMAGE WAS PROVIDED
        if profile.avatar == '':
            avatar = '/media/avatar.png'
        else:
            avatar = profile.avatar.url

        context["avatar"] = avatar

    # Query All things owned by user >> then add to the list(stash_objects_)
    qs_by_owner = Thing.objects.filter(owner=int(user_id)).order_by('-date_added')
    qs_by_borrower = Thing.objects.filter(current_borrower=int(user_id)).order_by('-date_added')
    
    # OBJECT AVAILABLE FOR THIS PROFILE
    context["stash_objects"] = [stash_objects.pk for stash_objects in qs_by_owner | qs_by_borrower]

    return JsonResponse(context, status=201, safe=False)


# FOR NOTIFICATIONS
def api_borrow_requests(request):
    borrow_request = AgreeOrRejectTransaction.objects.filter(owner=request.user).order_by('-action_made')
    contents = []
    for each in borrow_request:
        context = {}
        context["owner"] = str(each.owner)
        context["id"] = each.pk

        if each.action == "agree":
            context["agreed"] = True
        elif each.action == "reject":
            context["agreed"] = False
        
        if each.action == "":
            context["done"] = False
        else:
            context["done"] = True

        context["context_thing_id"] = each.t_id
        context["context_thing"] = str(each.t_borrow.thing)
        context["context_borrower"] = str(each.t_borrow.borrower)
        context["context_return"] = str(each.t_borrow.promised_return)
        contents.append(context)

    return JsonResponse(contents, status=201, safe=False)


def api_return_requests(request):
    return_request = AgreeOrRejectReturn.objects.filter(owner=request.user).order_by('-action_made')
    contents = []
    for each in return_request:
        context = {}
        context["owner"] = str(each.owner)
        context["id"] = each.pk

        if each.action == "agree":
            context["agreed"] = True
        elif each.action == "reject":
            context["agreed"] = False
        
        if each.action == "":
            context["done"] = False
        else:
            context["done"] = True

        context["context_thing_id"] = each.t_id
        context["context_thing"] = str(each.based_on_lend.thing)
        context["context_borrower"] = str(each.borrower)
        contents.append(context)

    return JsonResponse(contents, status=201, safe=False)



#INDIVIDUAL OBJECTS
def api_for_each_object(request, id):
    find = Thing.objects.filter(pk=id)
    for found in find:

        # generate age
        date_added_string = found.date_added.strftime('%Y-%m-%d %H:%M:%S.%f') #get the datetime from models and stringify
        date_added = datetime.strptime(date_added_string, '%Y-%m-%d %H:%M:%S.%f') #convert to datetime object
        date_today = datetime.now() #current datetime
        age = date_today - date_added #finally the result.... note: its autoconverted to timedelta object
    
        if age.days > 1:
            added = '{} day{} ago'.format(int(age.days), 's' if age.days > 1 else '')
        elif age.days == 1:
            added = 'Yesterday'
        elif age.seconds/3600 >= 1:
            added = '{} hr{} ago'.format(int(age.seconds/3600), 's' if age.seconds >= 7200 else '')
        elif age.seconds/3600 < 1:
            added = '{} min{} ago'.format(int(age.seconds/60), 's' if age.seconds >= 120  else '')
        
        # generate thing_thumbnail
        if found.image == '':
            thing_thumbnail = '/media/photo-placeholder.svg'
        else:
            thing_thumbnail = found.image.url

        #generate current_borrower
        if found.current_borrower is None:
            current_borrower = 'NOT BORROWED'
            promised_return = 'NOT SET'
        else:
            current_borrower = str(found.current_borrower)
            promised_return = found.promised_return_by_borrower

        
        context = {
            'pk': found.pk,
            'thing_name': found.thing_name,
            'owner': str(found.owner),
            'thing_sn': found.serial_no,
            'date_added': added,
            'thing_status': found.status,
            'thing_condition': found.condition,
            'thing_thumbnail': thing_thumbnail,
            'borrowed': found.borrowed,
            'current_borrower': current_borrower,
            'promised_return': promised_return,
            'attempt_return': found.attempt_return
        }

        return JsonResponse(context, status=201)

 
    