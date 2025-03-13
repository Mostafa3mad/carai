# #%% register
# import requests
#
# files = {
#     'password':  'Mo_3032003' ,
#     'username':  'fady5' ,
#     'first_name': 'mostafa45',
#     'last_name': 'emad',
#     'email':  'mostafaemadss21@gmail.com' ,
#     'phone_number':  '1256325489' ,
#     'gender':  'male' ,
#     'age':  '15' ,
#     'role':  'patient' ,
#     'password_confirm':  'Mo_3032003' ,
# }
#
# response = requests.post('http://127.0.0.1:8000/accounts/api/auth/register/', json=files)
# print(response.json())
#
#
# #%% login
#
#
# import requests
# files = {
#     'password':  'Mo_3032003' ,
#     'login' : 'fady5' ,
# }
# response = requests.post('http://127.0.0.1:8000/accounts/api/auth/login/', json=files)
# print(response.json())
# #%% shell
#
# from register_user.models import CustomUser
# doctors_with_specialization = CustomUser.objects.filter(role='doctor', specialization__isnull=False)
# print(doctors_with_specialization)
#

#%% logout


import requests




import requests

# Replace with your actual refresh token
payload = {
    'refresh': 'w30QVvv6BN1HOhIrWrTXS1AV7qxF4KYm6Xjp3sV2NgSAKbX0EdFMqu5b7q27eOSL',
}

url = 'https://mostafa3mad.pythonanywhere.com/api/logout/'

headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN_HERE'  # Replace with actual token if needed
}

response = requests.post(url, json=payload, headers=headers)

try:
    print(response.json())
except ValueError:
    print("Response is not in valid JSON format")
    print(response.text)  # Print raw response content


