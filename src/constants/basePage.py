#add url constant here
import requests
import json


class Baseclass:
    file_path = "src/resources/mw.tech"

    netlist_file_path = "src/resources/mw.spice"

    def get_base_url(self):
        return "http://13.202.227.36:8001"
        #return "http://13.200.63.95:3001"

    def get_user_login(self):
        return self.get_base_url() + "/user/login/"

    def create_project(self):
        return self.get_base_url() + "/project/create/"

    def check_project_status(self):
        return self.get_base_url()+"/project/checkproject/"

    def run_layout(self):
        return self.get_base_url() + "/run/project/"

    def clear_stage_result(self):
        return self.get_base_url() + "/run/clear/result/"

    def edit_stage_project(self, project_id):
        return self.get_base_url() + f"/project/edit/{project_id}/"

    def get_netlist(self):
        return self.get_base_url() + "/netlist/getlist/"

    def get_techlist(self):
        return self.get_base_url() + "/tech/getlist/"


    def stage1_result(self):
        return self.get_base_url() + "/stage/result/"

    def get_gds_images(self):
        return self.get_base_url() + "/stage/gdsimg/"

    def get_techdata(self):
        return self.get_base_url() + "/tech/getdata/"

    def get_netlist_data(self):
        return self.get_base_url() + "/netlist/getdata/"

    def get_stage_download_all_layout(self):
        return self.get_base_url() + "/stage/download/result/"

    def single_gds_download(self):
        return self.get_base_url() + "/stage/download/gds/"

    def get_job_list(self):
        return self.get_base_url() + "/run/list/"

    def project_list(self):
        return self.get_base_url() + "/project/list/"

    def password_update(self):
        return self.get_base_url() + "/profile/password/update/"

    def get_job_run(self, jobid):
        return self.get_base_url() + f"/run/job/{jobid}"

    def get_stage1_ready(self):
        return self.get_base_url() + "/project/stage1_ready/"

    def get_project_details(self, projectid):
        return self.get_base_url() + f"/project/details/{projectid}"

    def get_file_upload(self):
        return self.get_base_url() + "/administrator/tech/upload/"

    def get_netlist_upload(self):
        return self.get_base_url() + "/administrator/netlist/upload/"

    def get_file_list(self):
        return self.get_base_url() + "/administrator/getlist/"

    def get_modify_file(self):
        return self.get_base_url() + "/administrator/modify/file/"

    def delete_tech_file(self):
        return self.get_base_url() + "/administrator/delete/file/"

    def create_user(self):
        return self.get_base_url() + "/profile/create/"

    def modify_user_details(self, UserId):
        return self.get_base_url() + f"/profile/modify/{UserId}/"

    def user_profile_list(self):
        return self.get_base_url() + f"/profile/list/"

    def delete_project(self, projectid):
        return self.get_base_url() + f"/project/delete/{projectid}/"

    def refresh_token(self):
        return self.get_base_url()+f"/token/refresh/"

    def about_API(self):
        return self.get_base_url()+f"/user/about"


    def get_request(self, url, auth, headers, in_json):
        response = requests.get(url=url, auth=auth, headers=headers)
        if in_json is True:
            return response.json()
        return response

    def post_request(self, url, auth, headers, payload, in_json):
        post_response_data = requests.post(url=url, auth=auth, headers=headers, data=json.dumps(payload))
        if in_json is True:
            return post_response_data.json()
        return post_response_data

    def patch_request(self, url, auth, headers, payload, in_json):
        post_response_data = requests.patch(url=url, auth=auth, headers=headers, data=json.dumps(payload))
        if in_json is True:
            return post_response_data.json()
        return post_response_data

    def put_request(self, url, auth, headers, payload, in_json):
        post_response_data = requests.put(url=url, auth=auth, headers=headers, data=json.dumps(payload))
        if in_json is True:
            return post_response_data.json()
        return post_response_data

    def delete_request(self, url, auth, headers, in_json):
        post_response_data = requests.delete(url=url, auth=auth, headers=headers)
        if in_json is True:
            return post_response_data.json()
        return post_response_data

    def delete_file(self, url, auth, headers,payload, in_json):
        post_response_data = requests.delete(url=url, auth=auth, headers=headers,data=json.dumps(payload))
        if in_json is True:
            return post_response_data.json()
        return post_response_data


    def common_header(self):
        headers = {
            "Content-Type": "application/json",

        }
        return headers

    def common_header1(self, token):
        headers = {

            "Authorization": f"Bearer {token}",  # Add the Bearer token dynamically
        }
        return headers
