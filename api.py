# # API dan foydalanish
# import requests
# import json

# URL= 'http://127.0.0.1:8000/api'

# def get_user(telegram_id):
#     try:
#         response = requests.post(url=f"{URL}/get_user/", data={'telegram_id': telegram_id})
#         if response.status_code == 204:
#             return 'Not Found'
#         else:
#             return json.loads(response.text)
#     except:
#         pass

# def create_user(telegram_id:str,language:str=None,name:str=None, add_date:str=None):
#     try:
#         response = requests.post(url=f"{URL}/botuser/",
#                                  data={'telegram_id': telegram_id, 'full_name': name, 'add_date': add_date })
#         return 'Ok'
#     except:
#         return 'Bad'
# def get_all_users():
#     try:
#         response = requests.get(url=f"{URL}/botuser/")
#         return json.loads(response.text)
#     except:
#         return []
    
# def get_all_employee():
#     try:
#         response = requests.get(url=f"{URL}/employees/")
#         return json.loads(response.text)
#     except:
#         return []
    
# def get_employee(telegram_id):
#     try:
#         response = requests.post(url=f"{URL}/get_employee/",
#                                  data={'telegram_id':telegram_id})
#         if response.status_code==206:
#             return json.loads(response.text)
#         else:
#             return {}
#     except:
#         return {}
#     # done
# def get_all_task():
#     try:
#         response = requests.get(url=f"{URL}/tasks/")
#         return json.loads(response.text)
#     except:
#         return []
    
# def get_task(id):
#     try:
#         response = requests.post(url=f"{URL}/get_task/",
#                                  data={'id':id})
#         if response.status_code==206:
#             return json.loads(response.text)
#         else:
#             return {}
#     except:
#         return {}
#     # done
# def get_all_advance():
#     try:
#         response = requests.get(url=f"{URL}/advances/")
#         return json.loads(response.text)
#     except:
#         return []
    
# def get_advance(id):
#     try:
#         response = requests.post(url=f"{URL}/get_advance/",
#                                  data={'id':id})
#         if response.status_code==206:
#             return json.loads(response.text)
#         else:
#             return {}
#     except:
#         return {}
#     # done

# def get_all_offer():
#     try:
#         response = requests.get(url=f"{URL}/offers/")
#         return json.loads(response.text)
#     except:
#         return []
    
# def get_offer(id):
#     try:
#         response = requests.post(url=f"{URL}/get_offer/",
#                                  data={'id':id})
#         if response.status_code==206:
#             return json.loads(response.text)
#         else:
#             return {}
#     except:
#         return {}
#     # done

# def get_all_complaint():
#     try:
#         response = requests.get(url=f"{URL}/complaints/")
#         return json.loads(response.text)
#     except:
#         return []
    
# def get_get_complaint(id):
#     try:
#         response = requests.post(url=f"{URL}/get_complaint/",
#                                  data={'id':id})
#         if response.status_code==206:
#             return json.loads(response.text)
#         else:
#             return {}
#     except:
#         return {}