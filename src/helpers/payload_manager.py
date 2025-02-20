import json

import json
import os


class Payload():

    def get_payload_create_project(self):
        try:
            # Check if the file exists before opening
            file_path = "src/resources/create_project.json"
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file `{file_path}` does not exist.")

            # Open the JSON file
            with open(file_path, "r") as file_data:
                # Load the file content as a dictionary
                data = json.load(file_data)

            # Debug: print the data to ensure it's being loaded correctly
            # print("Payload data loaded:", data)

            return data

        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in `create_project.json`. Error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_payload_run_project(self):
        with open("src/resources/run_layout.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_stage1_result(self):
        with open("src/resources/stage1_result.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_stage2_result(self):
        with open("src/resources/stage2_result.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_gds_images(self):
        with open("src/resources/get_gds_image.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_stage1_download_All(self):
        with open("src/resources/download_stage1_result.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_stage2_download_All(self):
        with open("src/resources/download_stage2_result.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_netlist_getdata(self):
        with open("src/resources/netlist_getdata.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_single_gds_payload(self):
        with open("src/resources/single_jds_download.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def clear_result_stage1(self):
        with open("src/resources/clear_result_stage1.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def clear_result_stage2(self):
        with open("src/resources/clear_result_stage2.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_stage1_edit_project(self):
        with open("src/resources/edit_stage1_project.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_stage2_edit_project(self):
        with open("src/resources/edit_stage2_project.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_dummy_user(self):
        with open("src/resources/dummy_user.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_password_update(self):
        with open("src/resources/user_password_update.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_single_gds_payload_stage2(self):
        with open("src/resources/single_gds_download_stage2.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_run_list_payload(self):
        with open("src/resources/runlist.json", "r") as file_data:
            data = json.load(file_data)
        return data

    def get_payload_auth(self):
        with open("src/resources/auth.json", "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)  # json.load reads directly from the file object
        return data

    def get_payload_refresh_token(self):
        with open("src/resources/refresh_token.json", "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)  # json.load reads directly from the file object
        return data

    # def get_payload_techdata():
    #     try:
    #         # Check if the file exists before opening
    #         file_path = "src/resources/techdata.json"
    #         if not os.path.exists(file_path):
    #             raise FileNotFoundError(f"The file `{file_path}` does not exist.")
    #
    #         # Open the JSON file
    #         with open(file_path, "r") as file_data:
    #             # Load the file content as a dictionary
    #             data = json.load(file_data)
    #
    #         # Debug: print the data to ensure it's being loaded correctly
    #        # print("Payload data loaded:", data)
    #
    #         return data
    #
    #     except FileNotFoundError as e:
    #         print(f"Error: {e}")
    #         raise
    #     except json.JSONDecodeError as e:
    #         print(f"Error: Invalid JSON format in `techdata.json`. Error: {e}")
    #         raise
    #     except Exception as e:
    #         print(f"Unexpected error: {e}")
    #         raise

    def get_payload_techdata(self):
        with open("src/resources/techdata.json", "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_delete_techfile(self):
        with open("src/resources/delete_tech_file.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_delete_netlistfile(self):
        with open("src/resources/delete_netlist_file.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_modify_netlist(self):
        with open("src/resources/modify_netlist.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            # print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_modify_techfile(self):
        with open("src/resources/modify_techfile.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            # print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_create_user(self):
        with open("src/resources/create_user.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            # print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_modify_user(self):
        with open("src/resources/modify_user.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            # print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_profile_list(self):

        with open("src/resources/profile_list.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            # print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_get_techfile(self):
        with open("src/resources/get_techfiles.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_create_hyperexpressivity(self):
        with open("src/resources/create_project_hyperexpressivity.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_create_action3(self):
        with open("src/resources/create_project_action3.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_run_layout_Action3(self):
        with open("src/resources/run_layout_action3.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_check_project_status(self):
        with open("src/resources/check_project.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_get_netlistfile(self):
        with open("src/resources/get_netlistfile.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def get_payload_validate_netlist(self):
        with open("src/resources/validate_netlist.json",
                  "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)
            #print("techdata is", data)  # json.load reads directly from the file object
        return data

    def download_global_netlist(self):
        with open("src/resources/download_global_netlist.json","r") as file_data:
            data=json.load(file_data)
        return data

    def get_payload_stage_summary(self):
        with open("src/resources/stage_summary.json","r") as file_data:
            data=json.load(file_data)
        return data

    def get_payload_invalid_credentials(self):
        with open("src/resources/invalid_credentials.json", "r") as file_data:  # Use 'with' to automatically close the file
            data = json.load(file_data)  # json.load reads directly from the file object
        return data


    # def get_payload(file_path, modifications=None):
    #     # Load the base payload from the specified file
    #     with open(file_path, "r") as file:
    #         payload = json.load(file)
    #
    #     # Apply modifications from the scenario
    #     if modifications:
    #         payload.update(modifications)
    #
    #     return payload

    #
    # def load_scenarios(scenarios_file="src/resources/techdata_scenario.json"):
    #     """
    #     Load all scenarios from the variations config file.
    #
    #     Args:
    #         scenarios_file (str): Path to the JSON file with scenario variations.
    #
    #     Returns:
    #         list: List of scenarios to be used in the tests.
    #     """
    #     with open(scenarios_file, "r") as file:
    #         scenarios_data = json.load(file)
    #
    #     return scenarios_data.get("scenarios", [])
