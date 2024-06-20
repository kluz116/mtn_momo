# myapp/decorators.py
from functools import wraps
from django.http import JsonResponse
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import base64


def validate_signature(public_key_pem):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Get the X-Signature header
            x_signature = request.headers.get('X-Signature')
            if not x_signature:
                return JsonResponse({'error': 'X-Signature header missing'}, status=400)

            # Get the raw POST data
            raw_data = request.body

            # Decode the signature
            try:
                signature = base64.b64decode(x_signature)
            except (TypeError, ValueError) as e:
                return JsonResponse({'error': 'Invalid base64 signature'}, status=400)

            # Load the public key
            rsa_key = RSA.import_key(public_key_pem)

            # Verify the signature
            signer = PKCS1_v1_5.new(rsa_key)
            digest = SHA256.new()
            digest.update(raw_data)
            if not signer.verify(digest, signature):
                return JsonResponse({'error': 'Invalid signature'}, status=403)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
