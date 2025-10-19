from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import serialization, hashes

from cryptography.hazmat.primitives.asymmetric import padding



# Generate a public-private key pair

private_key = rsa.generate_private_key(

    public_exponent=65537,

    key_size=2048,

    backend=default_backend()

)

public_key = private_key.public_key()



# Serialize the keys (optional)

pem_private = private_key.private_bytes(

    encoding=serialization.Encoding.PEM,

    format=serialization.PrivateFormat.TraditionalOpenSSL,

    encryption_algorithm=serialization.NoEncryption()  # No encryption for the private key

)

pem_public = public_key.public_bytes(

    encoding=serialization.Encoding.PEM,

    format=serialization.PublicFormat.SubjectPublicKeyInfo

)



# Print the keys (for demonstration purposes)

print("Private Key:")

print(pem_private.decode())

print("Public Key:")

print(pem_public.decode())



# Get user input for the message

message = input("Enter a message to encrypt: ").encode()



# Encrypt the message with the public key

encrypted_message = public_key.encrypt(

    message,

    padding.OAEP(

        mgf=padding.MGF1(algorithm=hashes.SHA256()),

        algorithm=hashes.SHA256(),

        label=None

    )

)



print("\nEncrypted Message (in bytes):")

print(encrypted_message)



# Decrypt the message with the private key

decrypted_message = private_key.decrypt(

    encrypted_message,

    padding.OAEP(

        mgf=padding.MGF1(algorithm=hashes.SHA256()),

        algorithm=hashes.SHA256(),

        label=None

    )

)



print("\nDecrypted Message:")

print(decrypted_message.decode())

