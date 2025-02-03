# import requests
# import json
#
#
# def get_request(url, auth, in_json):
#     response = requests.get(url=url, auth=auth)
#     if in_json is True:
#         return response.json()
#     return response
#
#
# def post_request(url, auth,headers, payload, in_json):
#     post_response_data = requests.post(url=url, auth=auth,headers=headers, data=json.dumps(payload))
#     if in_json is True:
#         return post_response_data.json()
#     return post_response_data
#
#
#
# def patch_request(url, auth, headers, payload, in_json):
#     post_response_data = requests.patch(url=url, auth=auth,headers=headers, data=json.dumps(payload))
#     if in_json is True:
#         return post_response_data.json()
#     return post_response_data
