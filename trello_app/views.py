from trello_app.models import UserProfile, User
import requests, json
from django.http import JsonResponse
from django.db import IntegrityError
import traceback
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


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
