from django.http import JsonResponse
from firebase_config.auth import verify_token
from firebase_config.firestore import get_user_email
from users.models import User
from django.views.decorators.csrf import csrf_exempt
import json

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

    # Check if the user already exists in the database
    user, created = User.objects.get_or_create(
        uid=uid,
        email=email
    )

    if created:
        print(f"User with UID {uid} and email {email} created.")
    else:
        print(f"User with UID {uid} and email {email} already exists.")

    return JsonResponse({'uid': uid, 'email': email})

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
