from django.http import JsonResponse
from firebase_config.auth import verify_token
from firebase_config.firestore import get_user_email
from users.models import User

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
