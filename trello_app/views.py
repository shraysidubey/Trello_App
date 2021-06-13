from trello_app.models import UserProfile, User, Bank, Board, List, Card
import requests, json
from django.http import JsonResponse
from django.db import IntegrityError
import traceback
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


'''
status_codes:
    error from database: 1
    object not found: 0

    
'''

def is_blank(S):
    if len(S.strip(" ")) != 0:
        return False
    return True


def user(request):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            #print json_data
            # {u'username': u'dhsharma_', u'is_superuser': True, u'password': u'1234', u'email': u'dhsharma27@gmail.com'}
            if is_blank(json_data.get("username")) or is_blank(json_data.get("password")) or is_blank(json_data.get("email")) or is_blank(json_data.get("firstname")) or is_blank(json_data.get("lastname")) or is_blank(json_data.get("is_superuser")):
                return JsonResponse({'status': 500, 'status_code': -1, 'message': 'expected keys are: [username, email, password,first_name, last_name, is_superuser]', })

            user = User()
            user.username = json_data.get("username")
            user.set_password(json_data.get("password"))
            user.email = json_data.get("email")
            user.first_name = json_data.get("firstname")
            user.last_name = json_data.get("lastname")
            #print "qbienijenone", json_data.get("is_superuser")
            #print str(json_data.get("is_superuser") == "True")
            if json_data.get("is_superuser") == "True":
                user.is_superuser = True
            else:
                user.is_superuser = False

            user.save()

            user_profile = UserProfile()
            user_profile.alias = json_data.get("alias")
            user_profile.workplace_name = json_data.get("workplace_name")
            user_profile.user = user
            user_profile.save()
            print "saved userprofile"
            return JsonResponse({'user_profile_id': user_profile.id, 'status':200, 'message':'successful'})

    except KeyError:
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'expected keys are: [username, email, password,first_name, last_name, is_superuser]'})
    except IntegrityError as e:
        print "traceback erros", traceback.print_exc()
        return JsonResponse({'status': 500, 'status_code': 1, 'message': 'not able to save user_profile object'})
    except Exception as e:
        print "there is an exception" + type(e).__name__
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


@api_view(['GET',])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def profile(request, user_id):
    try:
        print("30909835809385903853")
        print(request.user)
        print("0390-390-935-935-93-53")
        user_profile = UserProfile.objects.get(id=user_id)
        return JsonResponse({'status':200, 'username': user_profile.user.username,'email': user_profile.user.email, 'alias': user_profile.alias, 'firstname': user_profile.user.first_name,'lastname': user_profile.user.last_name,'workplace_name': user_profile.workplace_name,'is_superuser': user_profile.user.is_superuser})

    except UserProfile.DoesNotExist:
        return JsonResponse({'status': 0,'message': 'user not found'})


@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def bank_details(request):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            print json_data
            if is_blank(json_data.get("card_holder_name")) or is_blank(json_data.get("cvv")) or is_blank(json_data.get("expiry_date")):
                return JsonResponse({'status': 500, 'status_code': -1, 'message': 'expected keys are: [card_holder_name, cvv, expiry_date]'})

            user_profile = UserProfile.objects.get(user=request.user)

            bank_details = Bank()
            bank_details.card_holder_name = json_data.get("card_holder_name")
            bank_details.cvv = json_data.get("cvv")
            date_string = json_data.get("expiry_date")
            date_format = "%Y-%m"
            date_object = datetime.strptime(date_string, date_format)

            bank_details.expiry_date = date_object
            bank_details.user_profile = user_profile
            bank_details.save()
            print "successfully saved"
            return JsonResponse({'status': 200,  'message': 'successfully saved'})

        if request.method == 'GET':
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                bank_details = Bank.objects.get(user_profile=user_profile)
                return JsonResponse(
                    {'status': 200, 'card_holder_name': bank_details.card_holder_name, 'cvv': bank_details.cvv,
                    'expiry_date': bank_details.expiry_date})

            except Bank.DoesNotExist:
                return JsonResponse({'status': 0,'message': 'bank details not found'})

    except Exception as e:
        #print "ERROR TRACEBACK ", traceback.print_exc()
        print "there is an exception:  " + type(e).__name__
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def board(request):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            print json_data
            if is_blank(json_data.get("title")):
                return JsonResponse({'status': 500, 'status_code': -1, 'message': 'expected key in JSON:["title"]'})
            user_profile = UserProfile.objects.get(user=request.user)

            board = Board()
            board.title = json_data.get("title")
            board.created_at = datetime.now()
            board.user_profile = user_profile
            board.save()

            list_obj_1 = List()
            list_obj_2 = List()
            list_obj_3 = List()
            list_obj_1.title = "To Do"
            list_obj_2.title = "Doing"
            list_obj_3.title = "Done"
            list_obj_1.created_at = datetime.now()
            list_obj_2.created_at = datetime.now()
            list_obj_3.created_at = datetime.now()

            list_obj_1.created_by = user_profile
            list_obj_1.board = board
            list_obj_1.save()

            list_obj_2.created_by = user_profile
            list_obj_2.board = board
            list_obj_2.save()

            list_obj_3.created_by = user_profile
            list_obj_3.board = board
            list_obj_3.save()

            print "successfully saved"
            return JsonResponse({'status':200, 'message':"successfully saved"})

    except Exception as e:
        #print "ERROR TRACEBACK ", traceback.print_exc()
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_lst(request, board_id):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)

            if is_blank(json_data.get("title")):
                return JsonResponse({'status': 500, 'status_code': -1, 'message': 'expected key in JSON:["title"]'})

            user_profile = UserProfile.objects.get(user=request.user)
            board = Board.objects.get(id=board_id)

            list_obj = List()
            list_obj.title = json_data.get("title")
            list_obj.created_at = datetime.now()
            list_obj.created_by = user_profile
            list_obj.board = board
            list_obj.save()

            return JsonResponse({'status': 200, 'message': "successfully saved"})

    except Exception as e:
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})
