from rest_framework.authentication import BaseAuthentication
from firebase_admin import auth
from users.models import User

def verify_token(id_token):
    """
    Verifies the Firebase ID token.
    """
    if not id_token:
        print("No token provided.")
        return None
    
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        
        # Optionally log the decoded token or parts of it
        print(f"Decoded token: {decoded_token}")
        
        # Return the decoded token, which includes user information like UID
        return decoded_token
        
    except auth.ExpiredIdTokenError:
        print("Error: Token has expired.")
        return None
    except auth.RevokedIdTokenError:
        print("Error: Token has been revoked.")
        return None
    except auth.InvalidIdTokenError:
        print("Error: Invalid ID token.")
        return None
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        id_token = auth_header.split('Bearer ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user, _ = User.objects.get_or_create(uid=uid)
            return (user, None)
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None