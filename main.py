import requests
from tabulate import tabulate

choices_list = {"1": "Total Incident Count", "2": "Incident count by Police District",
                "3": "Incident count by Day of the Week", "4": "Incident count by Type"}

keys_list = {"1": "", "2": "police_district", "3": "incident_day_of_week", "4": "incident_category"}


def valid_year_input():
    global user_input
    try:
        user_input = int(input("⌨️ Type a year to search through (2018-2023): "))
    except ValueError:
        print("Invalid Input ❌. Try again.\n")
        valid_year_input()
    else:
        if int(user_input) < 2018 or int(user_input) > 2023:
            print("Invalid Year ❌. Try again.\n")
            valid_year_input()
    return user_input


def filter_by_year(user_input):
    global user_year_dataset
    user_year_dataset = []
    for section in range(0, len(dataset)):
        small_dataset = dataset[section]
        if small_dataset.get("incident_year") == str(user_input):
            user_year_dataset.append(small_dataset)
    return len(user_year_dataset)


def parse_data(key_from_API):
    result_dict = {}
    for section in range(0, len(user_year_dataset)):
        value = user_year_dataset[section].get(key_from_API)
        if value in result_dict.keys():
            count = result_dict.get(value) + 1
            result_dict.update({f"{value}": (count)})
        else:
            result_dict.update({f"{value}": 1})
    result_dict = sort_data(result_dict)
    return result_dict


def sort_data(data):
    sorted_result_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return sorted_result_dict


def format_output(data, descriptive_header):
    headers = [f"{descriptive_header}", "# of Incidents"]
    print(tabulate(data, headers, tablefmt="simple_outline", numalign="center"))


def validate_user_choice(filter_method):
    global should_continue, user_year, PDI_incidents
    if filter_method not in keys_list.keys():
        if filter_method == "q":
            should_continue = False
        elif filter_method == 'cy':
            user_year = valid_year_input()
            PDI_incidents = filter_by_year(user_year)
        else:
            print("Invalid Input ❌. Try Again.")
    else:
        return True


# Source (San Francisco Police Department’s (SFPD)):
# https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/about_data
DataSF_API_ENDPOINT = "https://data.sfgov.org/resource/wg3w-h783.json?$query=SELECT%0A%20%20%60incident_datetime%60" \
                      "%2C%0A%20%20%60incident_date%60%2C%0A%20%20%60incident_time%60%2C%0A%20%20%60incident_year%60" \
                      "%2C%0A%20%20%60incident_day_of_week%60%2C%0A%20%20%60report_datetime%60%2C%0A%20%20%60row_id" \
                      "%60%2C%0A%20%20%60incident_id%60%2C%0A%20%20%60incident_number%60%2C%0A%20%20%60cad_number%60" \
                      "%2C%0A%20%20%60report_type_code%60%2C%0A%20%20%60report_type_description%60%2C%0A%20%20" \
                      "%60filed_online%60%2C%0A%20%20%60incident_code%60%2C%0A%20%20%60incident_category%60%2C%0A%20" \
                      "%20%60incident_subcategory%60%2C%0A%20%20%60incident_description%60%2C%0A%20%20%60resolution" \
                      "%60%2C%0A%20%20%60intersection%60%2C%0A%20%20%60cnn%60%2C%0A%20%20%60police_district%60%2C%0A" \
                      "%20%20%60analysis_neighborhood%60%2C%0A%20%20%60supervisor_district%60%2C%0A%20%20" \
                      "%60supervisor_district_2012%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20" \
                      "%20%60point%60%2C%0A%20%20%60%3A%40computed_region_jwn9_ihcz%60%2C%0A%20%20%60%3A" \
                      "%40computed_region_jg9y_a9du%60%2C%0A%20%20%60%3A%40computed_region_h4ep_8xdi%60%2C%0A%20%20" \
                      "%60%3A%40computed_region_n4xg_c4py%60%2C%0A%20%20%60%3A%40computed_region_nqbw_i6c3%60%2C%0A" \
                      "%20%20%60%3A%40computed_region_viu7_rrfi%60%2C%0A%20%20%60%3A%40computed_region_26cr_cadq%60" \
                      "%2C%0A%20%20%60%3A%40computed_region_qgnn_b9vv%60 "
dataset = requests.get(url=DataSF_API_ENDPOINT)
dataset = (dataset.json())

print("""+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-++-+-+-+-
 Welcome To San Francisco Incident Analyzer
 +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+ +-+-++\n""")

user_year = valid_year_input()
PDI_incidents = filter_by_year(user_year)

should_continue = True


def search_dataset():
    print(f"\nHow would you like to filter the results of {user_year}?")
    print(
        f"\t1) {choices_list.get('1')}\n\t2) {choices_list.get('2')}\n\t3) {choices_list.get('3')}\n\t4) {choices_list.get('4')}")
    filter_method = input("⌨️ Type 1, 2, 3 or 4 for filtering. Type 'cy' to change year or 'q' to quit: ").lower()

    if filter_method == "1":
        v = [(user_year, PDI_incidents)]
        format_output(v, "Year")

    elif filter_method == "2":
        data = parse_data("police_district")
        format_output(data, "Police District")

    elif filter_method == "3":
        data = parse_data("incident_day_of_week")
        format_output(data, "Day of Week")

    elif filter_method == "4":
        data = parse_data("incident_category")
        format_output(data, "Incident Category")

    else:
        validate_user_choice(filter_method)


while should_continue:
    search_dataset()

print(f"See you next time! 👋")
