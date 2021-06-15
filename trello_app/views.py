from trello_app.models import UserProfile, User, Bank, Board, List, Card, Attachement
import json, traceback
from django.http import JsonResponse
from django.db import IntegrityError
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
        user_profile = UserProfile.objects.get(id=user_id)
        return JsonResponse({'status':200, 'username': user_profile.user.username,'email': user_profile.user.email, 'alias': user_profile.alias, 'firstname': user_profile.user.first_name,'lastname': user_profile.user.last_name,'workplace_name': user_profile.workplace_name,'is_superuser': user_profile.user.is_superuser})

    except UserProfile.DoesNotExist:
        return JsonResponse({'status': 0,'message': 'user not found'})


@api_view(['GET','POST','DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def bank_details(request):
    try:
        if request.method == 'DELETE':
            user_profile = UserProfile.objects.get(user=request.user)
            bank_details = Bank.objects.get(user_profile=user_profile)
            bank_details.delete()
            return JsonResponse({'status': 200, 'message': 'bank details deleted successfully'})

        if request.method == 'POST':
            json_data = json.loads(request.body)
            print json_data
            if is_blank(json_data.get("card_holder_name")) or is_blank(json_data.get("cvv")) or is_blank(json_data.get("expiry_date")):
                return JsonResponse({'status': 500, 'status_code': -1, 'message': "expected keys are: [card_holder_name, cvv, expiry_date]"})

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
def create_lst(request, board_id):
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


@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_card(request, lst_id):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            if is_blank(json_data.get("title")):
                return JsonResponse({'status': 500, 'status_code': -1, 'message': 'expected key in JSON:["title"]'})

            user_profile = UserProfile.objects.get(user=request.user)
            lst = List.objects.get(id=lst_id)
            card_obj_for_count = Card.objects.filter(list=lst).count()
            print "card_obj_for_count", card_obj_for_count
            card_obj = Card()

            card_obj.title = json_data.get("title")
            card_obj.position = card_obj_for_count
            card_obj.description = json_data.get("description")
            date_string = json_data.get("due_date")
            date_format = "%Y-%m-%d"
            date_object = datetime.strptime(date_string, date_format)
            card_obj.due_date = date_object
            card_obj.created_at = datetime.now()
            card_obj.created_by = user_profile
            card_obj.list = lst
            card_obj.save()
            print "successfully saved"

            return JsonResponse({'status': 200, 'message': "successfully saved"})

    except Exception as e:
        print "ERROR TRACEBACK ", traceback.print_exc()
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_attachements(request, card_id):
    print "checking"
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            print json_data

            user_profile = UserProfile.objects.get(user=request.user)
            card = Card.objects.get(id=card_id)
            links = json_data.get("attachements")

            for link in links:
                attachment_obj = Attachement()
                attachment_obj.link = link
                attachment_obj.attached_at = datetime.now()
                attachment_obj.card = card
                attachment_obj.user_profile = user_profile
                attachment_obj.save()
                print "successfully saved"
            return JsonResponse({'status': 200, 'message': "attachements added"})

    except Exception as e:
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


def deletion_of_card(request, card_id):
    try:
        card_obj = Card.objects.get(id=card_id)
        card_position = card_obj.position
        card_obj.delete()

        card = Card.objects.filter(position__gt=card_position, list=card_obj.list)
        for i in card:
            i.position -= 1
            i.save()
        return JsonResponse({'status': 200, 'message': "card successfully deleted"})

    except Card.DoesNotExist:
        return JsonResponse({'status': 0, 'message': 'card not found'})


@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def change_card_position(request, card_id):
    try:
        card_obj = Card.objects.get(id=card_id)
        current_position = card_obj.position
        print "current_position", current_position

        # fetching all cards after the current card
        cards_in_source_list = Card.objects.filter(position__gte=current_position, list=card_obj.list)
        for i in cards_in_source_list:
            i.position -= 1
            i.save()

        json_data = json.loads(request.body)
        destination_lst_id = json_data.get("destination_lst_id")
        destination_position = json_data.get("destination_position")

        destination_list_object = List.objects.get(id=destination_lst_id)
        cards_in_destination_lst = Card.objects.filter(position__gte=destination_position, list=destination_list_object)
        for i in cards_in_destination_lst:
            i.position += 1
            i.save()

        card_obj.position = destination_position
        card_obj.list = destination_list_object
        card_obj.save()

        return JsonResponse({'status': 200, 'message': "position of card is changed"})

    except Card.DoesNotExist:
        return JsonResponse({'status': 0, 'message': 'card not found'})

    except Exception as e:
        print "traceback erros", traceback.print_exc()
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


@api_view(['GET','DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def board_details(request, board_id):
    try:
        user_profile_obj = UserProfile.objects.get(user=request.user)
        board_obj = Board.objects.get(id=board_id)

        dic_of_board = {}
        dic_of_board['title'] = board_obj.title
        dic_of_board['created_at'] = board_obj.created_at
        dic_of_board['created_by'] = user_profile_obj.alias
        dic_of_board['created_by_id'] = user_profile_obj.id
        dic_of_board['list'] = []
        lst_objs = List.objects.filter(board=board_obj)
        list = []
        for list_obj in lst_objs:
            dic_of_list = {}
            dic_of_list['title'] = list_obj.title
            dic_of_list['created_at'] = list_obj.created_at
            dic_of_list['created_by_alias'] = user_profile_obj.alias
            dic_of_list['created_by_id'] = user_profile_obj.id
            dic_of_list['cards'] = []
            list.append(dic_of_list)
            dic_of_board['list'] = list
            card_objs = Card.objects.filter(list=list_obj)
            card_lst = []
            for card_obj in card_objs:
                dic_of_card = {}
                dic_of_card['title'] = card_obj.title
                dic_of_card['description'] = card_obj.description
                dic_of_card['due_date'] = card_obj.due_date
                dic_of_card['position'] = card_obj.position
                dic_of_card['created_at'] = card_obj.created_at
                dic_of_card['created_by_alias'] = user_profile_obj.alias
                dic_of_card['created_by_id'] = user_profile_obj.id
                card_lst.append(dic_of_card)
                dic_of_list['cards'] = card_lst

        return JsonResponse({'board_details': dic_of_board})

    except Exception as e:
        print "traceback erros", traceback.print_exc()
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def card_details(request, card_id):
    try:
        user_profile_obj = UserProfile.objects.get(user=request.user)
        card_obj = Card.objects.get(id=card_id)
        card_detail_obj = {}
        card_detail_obj['title'] = card_obj.title
        card_detail_obj['description'] = card_obj.description
        card_detail_obj['due_date'] = card_obj.due_date
        card_detail_obj['position'] = card_obj.position
        card_detail_obj['created_at'] = card_obj.created_at
        card_detail_obj['created_by_alias'] = user_profile_obj.alias
        card_detail_obj['created_by_id'] = user_profile_obj.id
        card_detail_obj['attachments'] = user_profile_obj.id

        attachments = Attachement.objects.filter(card= card_obj)
        for attachment in attachments:
            attach = {'id': attachment.id, 'url': attachment.url}
            card_detail_obj['attachments'].append(attach)
        return JsonResponse({'card_details': card_detail_obj})

    except Exception as e:
        print "traceback erros", traceback.print_exc()
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})


@api_view(['GET','DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_details(request, list_id):
    try:
        user_profile_obj = UserProfile.objects.get(user=request.user)
        if request.method == 'DELETE':
            list_obj = List.objects.get(id=list_id)
            if list_obj.created_by.id == user_profile_obj.id:
                list_obj.delete()
            else:
                return JsonResponse({'status': 500, 'status_code':5, 'message': 'only owner can delete the list'})
            return JsonResponse({'status': 200, 'message': 'list deleted successfully'})
        list_obj = List.objects.get(id=list_id)
        dic_of_list = {}
        dic_of_list['title'] = list_obj.title
        dic_of_list['created_at'] = list_obj.created_at
        dic_of_list['created_by_alias'] = user_profile_obj.alias
        dic_of_list['created_by_id'] = user_profile_obj.id
        return JsonResponse({'list details': dic_of_list})

    except Exception as e:
        print "traceback erros", traceback.print_exc()
        return JsonResponse({'status': 500, 'status_code': -1, 'message': 'unknown error'})