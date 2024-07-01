import os

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64
import string
import random

from ecw.constants import log_path


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


def write_to_file(content):
    file_path = os.path.join(os.path.dirname(__file__), f'{log_path}\log.txt')
    with open(file_path, 'a') as file:
        file.write(content + '\n')


def signPassword(TrxPassword):
    # Encode the transaction password to bytes
    TrxPassword_bytes = TrxPassword.encode()

    # Create a new SHA-256 hash object and update it with the transaction password bytes
    hash_object = SHA256.new(TrxPassword_bytes)

    # Get the binary (raw bytes) representation of the hash
    hash_bytes = hash_object.digest()
    base64_string = base64.b64encode(hash_bytes).decode()

    return base64_string
