import math
import random
import sympy


#my data 
p = 35083
q = 35401
N = p*q #1241973283 
phi_N = (p-1)*(q-1) #1241902800
e = 7
d = 709658743
# print(N, e, phi_N )

# encryption
MY_MESSAGE = "Secure Data"
MY_MESSAGE_chunks = ["Sec", "ure", "Dat", "a"]


# my partner data
PARTNER_N = 1796284849 
PARTNER_e = 239
PARTNER_CIPHERTEXT = [970323699, 251476315, 1104506380, 198954320]


# sign
MY_MESSAGE_TO_BE_SIGNED = "Tawsif Chowdhury"
MY_MESSAGE_TO_BE_SIGNED_chunks = ["Taw", "sif", " Ch", "owd", "hur", "y"]

# verfiy the signature
PARTNER_SIGNED_MESSAGE = "Sree Lakshme"
PARTNER_SIGNATURE = [763561406, 205616144, 208542228, 1665748221]
PARTNER_SIGNATURE_FROM_MESSAGE = ''

def generate_prime():
    while True:
        number = random.randint(32768, 35535)
        if sympy.isprime(number):
            return number
        

def generate_public_exponent(phi_N):
    while True:
        e = random.randint(4, 10)
        if sympy.isprime(e):
            if math.gcd(e, phi_N) == 1:
                return e

def generate_private_key(e, phi_N):
    d = pow(e, -1, phi_N)
    return d

def str_to_hex(chunk):
    # print(chunk)
    hex_chunk = ''
    for char in chunk:
        hex_chunk += hex(ord(char))[2:]
    return hex_chunk

def hex_to_int(hex_chunks):
    int_chunk = int(hex_chunks, 16)
    return int_chunk


def encrypt_int(int_value):
    encrypted_int =  pow(int_value, PARTNER_e, PARTNER_N)
    return encrypted_int

def decrypt_message(int_value):
    decrypted_int = pow(int_value, d, N)
    hex_code = int_to_hex( decrypted_int)
    return hex_code


def int_to_hex(n):
    if n < 0:
        return "-" + int_to_hex(-n)
    result = ""
    while n > 0:
        digit = n & 0xf
        if digit < 10:
            result = chr(ord('0') + digit) + result
        else:
            result = chr(ord('a') + digit - 10) + result
        n >>= 4
    return result


def hex_to_str(hex_code):
    hex_code_as_int = int(hex_code, 16)
    hex_code_as_bytes = hex_code_as_int.to_bytes((hex_code_as_int.bit_length() + 7) // 8, 'big')
    result = hex_code_as_bytes.decode('utf-8')
    return result

def sign_int(int_value):
    signed_int =  pow(int_value, d, N)
    return signed_int

def verify_signature(int_value):

    for val in int_value:
        decrypted_signed_int = pow(val, PARTNER_e, PARTNER_N)
        hex_code_for_signature = int_to_hex( decrypted_signed_int)
        partner_signature_chunk = hex_to_str(hex_code_for_signature)
        global PARTNER_SIGNATURE_FROM_MESSAGE
        PARTNER_SIGNATURE_FROM_MESSAGE += partner_signature_chunk 
    print('Decrypted signature from Partner: ',PARTNER_SIGNATURE_FROM_MESSAGE)
    return PARTNER_SIGNATURE_FROM_MESSAGE == PARTNER_SIGNED_MESSAGE 


hex_chunks = [str_to_hex(chunk) for chunk in MY_MESSAGE_chunks]
int_chunks = [hex_to_int(chunk) for chunk in hex_chunks]




MY_CIPHERTEXT = [encrypt_int(val) for val in int_chunks]
#[750720873, 1023323278, 1619672158, 1303098949]

decrypted_hex_code = [decrypt_message(chunk) for chunk in PARTNER_CIPHERTEXT]
PARTNER_MESSAGE_chunks_AFTER_DECRYPT = [hex_to_str(hex_code) for hex_code in decrypted_hex_code]
PARTNER_MESSAGE_AFTER_DECRYPT = ''.join(PARTNER_MESSAGE_chunks_AFTER_DECRYPT )


signed_text_hex_chunk = [str_to_hex(chunk) for chunk in MY_MESSAGE_TO_BE_SIGNED_chunks]
signed_text_int_chunk = [hex_to_int(chunk) for chunk in signed_text_hex_chunk]

MY_SIGNATURE = [sign_int(val) for val in signed_text_int_chunk]
# [673304102, 962047565, 456232556, 843603427, 9733931, 115944615]
IS_VALID_SIGNATURE = verify_signature(PARTNER_SIGNATURE)


print('Prime Number p: ', generate_prime()) 
print('Prime Number q: ', generate_prime()) 
print ('N: ', N)
print('My e: ',generate_public_exponent(phi_N)) 
# print(math.gcd(e, phi_N))
print('d: ',generate_private_key(e, phi_N))

# print(hex_chunks)
# print(int_chunks)

print(f'MY_CIPHERTEXT: {MY_CIPHERTEXT}')

# print(f'PARTNER_MESSAGE_chunks_AFTER_DECRYPT: {PARTNER_MESSAGE_chunks_AFTER_DECRYPT}')
print(f'PARTNER_MESSAGE_AFTER_DECRYPT: {PARTNER_MESSAGE_AFTER_DECRYPT}')

# print(signed_text_hex_chunk)
# print(signed_text_int_chunk)


print('My Signature',MY_SIGNATURE)


print('Is partner Signature valid: ', IS_VALID_SIGNATURE)


