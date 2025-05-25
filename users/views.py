from django.http import JsonResponse
from firebase_config.auth import verify_token
from firebase_config.firestore import get_user_email,get_user_details
from users.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

def calculate_age(dob_str):
    # Handles 'YYYY-MM-DD' and 'YYYY-MM-DDTHH:MM:SS.sss' formats
    if 'T' in dob_str:
        dob = datetime.strptime(dob_str.split('T')[0], "%Y-%m-%d").date()
    else:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    today = datetime.today().date()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# def get_user_details(uid):
#     from firebase_admin import firestore
#     db = firestore.client()
#     doc = db.collection('users').document(uid).get()
#     if doc.exists:
#         return doc.to_dict()
#     return None

def current_user_view(request):
    """
    Retrieves the current logged-in user's email.
    """
    id_token = request.headers.get('Authorization').split('Bearer ')[-1]
    print(f"id_token{id_token}")
    if not id_token:
        return JsonResponse({'error': 'Authorization token missing'}, status=401)

    # Verify the ID token
    decoded_token = verify_token(id_token)
    if not decoded_token:
        return JsonResponse({'error': 'Invalid or expired token'}, status=401)

    # Get UID from the decoded token
    uid = decoded_token.get('uid')
    email = decoded_token.get('email')  # Email from decoded token (direct from Firebase)
    print(f"uid:{uid}")
    print(f"email:{email}")

    # Fetch date of birth from Firestore
    user_details = get_user_details(uid)  # Should return dict with 'userDob'
    print(f"user_details:{user_details}")
    date_of_birth = user_details.get('userDob') if user_details else None

    print(f"date_of_birth:{date_of_birth}")    

    # Calculate age if DOB is available
    age = calculate_age(date_of_birth) if date_of_birth else None

    # Check if the user already exists in the database, update or create age
    user, created = User.objects.update_or_create(
        uid=uid,
        email=email,
        defaults={'age': age}
    )

    if created:
        print(f"User with UID {uid} and email {email} created.")
    else:
        print(f"User with UID {uid} and email {email} already exists or updated.")

    return JsonResponse({'uid': uid, 'email': email, 'age': age})

@csrf_exempt
def delete_user_view(request):
    """
    Deletes a user based on their UID.
    """
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid HTTP method. Use DELETE.'}, status=405)

    try:
        body = json.loads(request.body)
        uid = body.get('uid')

        if not uid:
            return JsonResponse({'error': 'UID is required to delete a user.'}, status=400)

        # Attempt to find and delete the user
        try:
            user = User.objects.get(uid=uid)
            user.delete()
            return JsonResponse({'message': f'User with UID {uid} has been deleted.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with UID {uid} does not exist.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
