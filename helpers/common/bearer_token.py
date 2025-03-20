import jwt
import datetime

# Define payload data
payload = {
    'username': 'env.user'
    'password': 'env.pass'
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)  # 10 hour expiry
}

# Generate the JWT token
token = jwt.encode(payload, secret_key, algorithm='HS256')

print('Generated JWT (Bearer Token):', token)