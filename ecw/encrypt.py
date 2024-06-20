from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64
import time
import string
import random


def signMsg(message):
    # Hash the message using SHA-256
    hash_obj = SHA256.new(message)

    # Load the private key

    #E: / ftb_uat_mtls / msg / ftb_rsa_signing.pem

    with open('E:/ftb_uat_mtls/msg/ftb_signing.key', 'rb') as f:
        private_key = RSA.import_key(f.read())

    # Sign the hashed message using the private key
    signature = pkcs1_15.new(private_key).sign(hash_obj)
    signature_base64 = base64.b64encode(signature).decode('utf-8')

    #print(f"Signature: {signature.hex()}")
    return signature_base64


def verfySif(message, signature_64):
    # Message to be verified (UTF-8 encoded)
    #message = "The quick brown fox jumps over the lazy dog".encode('utf-8')

    # Hash the message using SHA-256
    hash_obj = SHA256.new(message)

    #E:/ftb_uat_mtls/msg/ftb_signing.pub
    with open('E:/ftb_uat_mtls/msg/ftb_public_key.key', 'rb') as f:
        public_key = RSA.import_key(f.read())

    signature_base64 = signature_64
    signature = base64.b64decode(signature_base64)

    # Verify the signature
    try:
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        print("Signature is valid.")
    except (ValueError, TypeError):
        print("Signature verification failed.")


def generate_random_challenge():
    characters = string.ascii_letters + string.digits
    random_challenges = ''.join(random.choices(characters, k=26))
    return random_challenges


def generate_random_trx_id():
    characters = string.ascii_letters + string.digits
    random_challenges = ''.join(random.choices(characters, k=15))
    return random_challenges


def get_challenge(x_signature):
    return x_signature.split(";")[0]
