import pandas as PD
import PySimpleGUI as SG
import requests
from datetime import datetime
from pdfme import build_pdf

my_icon64 = b'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'

space_dict = {'LittleMS': 2.5,
              "MS": 5.0,
              "RS": 12.0,
              "Standard Width": 36.0,
              "Narrow Width": 24.0,
              "no value": 0.0,
              "Art Rack": 0.0,
              "Card Cabinet": 0.0,
              "Electronic records": 0.0,
              "GemTrac": 0.0,
              "Library Materials": 0.0,
              "Map drawer": 0.0,
              "Offsite storage": 0.0,
              "OS Deep Shelving": 0.0,
              "OS Narrow Width": 0.0,
              "OS Standard Width": 0.0,
              "Tall Volume Narrow": 0.0,
              "Tall Volume Standard": 0.0,
              "Top of Shelf": 12.0}

default_location = {'jsonmodel_type': 'container_location',
                    'ref': 'something',
                    'start_date': '2026-05-11',
                    'status': 'current'}

global_header = {'.': "Shelf list", "style": "title2", "outline": {'level': 1, 'text': 'Shelf list'}}
pdf_style = {'margin_bottom': 8, 'text-align': 'j'}
pdf_formats = {'title': {'b': 1, 's': 13, 'text_align': 'c'}, 'title2': {'b': 2, 's': 13, 'text_align': 'l'}, 'notes': {'s': 10, 'text_align': 'l', 'margin_left': 20}}
document_header = {'x': 'left', 'y': 20, 'height': 'top', 'style': {'text_align': 'r'}, 'content': [{'.b': 'Shelf list'}]}
document_footer = {'x': 'left', 'y': 800, 'height': 'bottom', 'style': {'text_align': 'r'}, 'content': [{'.': ['Page ', {'var': '$page'}]}]}
document_perPage = [{'pages': '1:1000:2', 'style': {'margin': [60, 100, 60, 60]}},
{'pages': '0:1000:2', 'style': {'margin': [60, 60, 60, 100]}},
{'pages': '0:4:2', 'running_sections': {'include': ['header', 'footer']}}]
#to calculate storage on a single shelf
def storage_shelf(item):
    aggregate = 0
    eligible_list = ['RS', 'MS', 'LittleMS', 'no value', "Standard Width", "Narrow Width"]
    if item['location_profile'] == "no value":
        item['location_profile'] = "Standard Width"
    if item['location_profile'] in eligible_list:
        outlier = False
        space = space_dict[item['location_profile']]
        for container in item['top_containers']:
            if container["containers_container_profile"] in eligible_list:
                space = space - space_dict[container["containers_container_profile"]]
            else:
                outlier = True
        if outlier is True:
            return "\tUnable to calculate free space\n"
        if outlier is False:
            if space >= 2.5:
                return f"\tAvailable space {str(space/12)[:4]} cubic ft.\n"
            else:
                return ""
    else:
        return ""

#to manipulate data and calculate available storage
def storage_space(location_dictionary):
    new_space_dictionary = {}
    aggregate = 0
    for key in location_dictionary:
        eligible_list = ['RS', 'MS', 'LittleMS', 'no value']
        location_in_room = location_dictionary[key]['location_in_room']
        if "Range" in location_in_room and "Section" in location_in_room and "Shelf" in location_in_room:
            location_profile = location_dictionary[key]['location_profile']
            if location_profile == "no value":
                location_profile = "Standard Width"
            space = space_dict[location_profile]
            eligible_flag = True
            for container in location_dictionary[key]['top_containers']:
                if container['containers_container_profile'] in eligible_list:
                    space = space - space_dict[container['containers_container_profile']]
                else:
                    eligible_flag = False
            if eligible_flag is True:
                if space >= 2.5:
                    #print(f"{location_dictionary[key]['room']}, {location_dictionary[key]['location_in_room']}: {space} linear inches")
                    new_space_dictionary[key] = location_dictionary[key]
                    aggregate += space
    final_count = str(float(aggregate)/12)
    final_count = final_count.split(".")
    window['-OUTPUT-'].update(f"{final_count[0]}.{final_count[1][:2]} cubic ft. space available in stacks\n", append=True)
    return new_space_dictionary

def circulation(variables_dict, location_dict):
    if values['-SESSION_TOKEN-'] == "":
        window['-OUTPUT-'].update("log in and try again\n", append=True)
        return
    headers = {'X-ArchivesSpace-Session': variables_dict['-SESSION_TOKEN-']}
    window['-OUTPUT-'].update(f"{headers}\n", append=True)
    try:
        top_container = requests.get(f"{variables_dict['-API_URL-']}/repositories/2/find_by_id/top_containers", params={"barcode[]": variables_dict['-BOX_BARCODE-'], "resolve[]": "top_containers"}, headers=headers).json()
        print(top_container)
        top_container_URI = f"{variables_dict['-API_URL-']}{top_container['top_containers'][0]['ref']}"
        print(top_container_URI)
        top_container_data = top_container['top_containers'][0]['_resolved']
        listy = list(location_dict.keys())
        listy = listy[0]
        current_location = location_dict[listy]
        current_time = datetime.today().strftime('%Y-%m-%d')
        new_location = default_location
        new_location['ref'] = listy
        new_location['start_date'] = current_time
        top_container_data.pop("long_display_string")
        if "internal_note" not in top_container_data.keys():
            top_container_data['internal_note'] = ""
        if variables_dict['circulation'] == "reference":
            top_container_data['internal_note'] = f"{top_container_data['internal_note']}Circulated to reference on {current_time} by user {variables_dict['-API_USERNAME-']}.\n"
            top_container_data['container_locations'].append(new_location)
        if variables_dict['circulation'] == "checkout":
            top_container_data['internal_note'] = f"{top_container_data['internal_note']}Checked out to location {current_location['record_title']} by user {variables_dict['-API_USERNAME-']} on {current_time}.\n"
            top_container_data['container_locations'].append(new_location)
        if variables_dict['circulation'] == "return":
            top_container_data['internal_note'] = f"{top_container_data['internal_note']}Container returned to {current_location['record_title']} by user {variables_dict['-API_USERNAME-']} on {current_time}.\n"
            top_container_data['container_locations'] = [new_location]
        if variables_dict['circulation'] == "transfer":
            top_container_data['internal_note'] = f"{top_container_data['internal_note']}Container transferred to {current_location['record_title']} by user {variables_dict['-API_USERNAME-']} on {current_time}.\n"
            top_container_data['container_locations'] = [new_location]
        response = requests.post(top_container_URI, json=top_container_data, headers=headers)
        window['-OUTPUT-'].update(f"{response.status_code}\n", append=True)
        return response.status_code
    except:
        window['-OUTPUT-'].update(f"trouble updating the location of this container, try doing it manually\n", append=True)
        return

#to take a single dataframe row and convert it to a dictionary. used in tandem with dict_converter
def row_converter(row, listy):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in listy:
        pictionary[item] = str(row[count])
        count += 1
    return pictionary

#to log into the ArchivesSpace system and generate an access token for running api-based updates
def runner(variables_dict):
    headers = requests.post(f"{variables_dict['-API_URL-']}/users/{variables_dict['-API_USERNAME-']}/login", params={"password": variables_dict['-API_PASSWORD-']}).json()
    window['-OUTPUT-'].update(f"{headers}\n", append=True)
    window['-SESSION_TOKEN-'].update(headers['session'])
    window['-OUTPUT-'].update(f"{headers}\n", append=True)

#to take a loaded spreadsheet and convert it to a set of dictionaries for further manipulatoin/use
def dict_converter(dataframe):
    location_building = []
    location_floor = []
    location_room = []
    location_range = []
    location_section = []
    location_shelf = []
    location_dictionary = {}
    item_dictionary = {}
    item_barcode_dictionary = {}
    listy = dataframe.columns
    for row in dataframe.itertuples():
        pictionary = row_converter(row, listy)
        if pictionary['location_url'] not in location_dictionary:
            location_dictionary[pictionary['location_url']] = {"top_containers": []}
        location_dictionary[pictionary['location_url']]['record_title'] = pictionary['record_title']
        location_dictionary[pictionary['location_url']]['building'] = pictionary['building']
        location_dictionary[pictionary['location_url']]['floor'] = pictionary['floor']
        location_dictionary[pictionary['location_url']]['room'] = pictionary['room']
        location_dictionary[pictionary['location_url']]['location_barcode'] = pictionary['location_barcode']
        location_dictionary[pictionary['location_url']]['location_in_room'] = pictionary['location_in_room']
        location_dictionary[pictionary['location_url']]['location_profile'] = pictionary['location_profile']
        minidict = {'containers_top_container_indicator': pictionary['containers_top_container_indicator'],
                    'containers_top_container_barcode': pictionary['containers_top_container_barcode'],
                    'containers_container_profile': pictionary['containers_container_profile']}
        location_dictionary[pictionary['location_url']]['top_containers'].append(minidict)
        my_set = pictionary['location_in_room'].split(", ")
        if pictionary['containers_top_container_barcode'] != "":
            item_barcode_dictionary[minidict['containers_top_container_barcode']] = {
                "indicator": minidict['containers_top_container_indicator'],
                "container_profile": minidict['containers_container_profile']}
        item_dictionary[minidict['containers_top_container_indicator']] = {
            "barcode": minidict['containers_top_container_barcode'],
            "container_profile": minidict['containers_container_profile']}
    for key in location_dictionary.keys():
        location_building.append(location_dictionary[key]['building'])
        location_floor.append(location_dictionary[key]['floor'])
        location_room.append(location_dictionary[key]['room'])
        my_set = location_dictionary[key]['location_in_room'].split(", ")
        location_range.append(my_set[0])
        location_section.append(my_set[1])
        location_shelf.append(my_set[2])
    location_building = list(set(location_building))
    location_building.sort()
    if values['-FLOOR-'] == "":
        location_floor = list(set(location_floor))
        location_floor.append("")
        location_floor.sort()
        window['-FLOOR-'].update(values=location_floor)
    if values['-ROOM-'] == "":
        location_room = list(set(location_room))
        location_room.append("")
        location_room.sort()
        window['-ROOM-'].update(values=location_room)
    if values['-RANGE-'] == "":
        location_range = list(set(location_range))
        location_range.append("")
        location_range.sort()
        window['-RANGE-'].update(values=location_range)
        window['-RANGE_RANGE-'].update(values=location_range)
    if values['-SECTION-'] == "":
        location_section = list(set(location_section))
        location_section.append("")
        location_section.sort()
        window['-SECTION-'].update(values=location_section)
        window['-RANGE_SECTION-'].update(values=location_section)
    if values['-SHELF-'] == "":
        location_shelf = list(set(location_shelf))
        location_shelf.append("")
        location_shelf.sort()
        window['-SHELF-'].update(values=location_shelf)
        window['-RANGE_SHELF-'].update(values=location_shelf)
    return location_dictionary, item_dictionary, item_barcode_dictionary

SG.theme("Purple")
bottom_left_layout = [
    [
        SG.Push(),
        SG.Text("General Dialog box"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="Dialog box for tasks as they go\n", size=(45, 9), auto_refresh=True, key="-OUTPUT-", autoscroll=True, border_width=5, reroute_stdout=True, background_color="PeachPuff2"),
        SG.Push(),
    ]
]
bottom_middle_layout = [
    [
        SG.Push(),
        SG.Text("Inventory details"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="Inventory details\n", size=(45, 9), auto_refresh=True, key="-INVENTORY_OUTPUT-", autoscroll=True, border_width=5, background_color="PeachPuff2"),
        SG.Push()
    ],

]
bottom_right_layout = [
    [
        SG.Push(),
        SG.Text("The Buttons"),
        SG.Push()
    ],
    [
        SG.Button("Search By Location Coordinates", size=(25, 1), tooltip="use to filter locations based on stacks coordinates.\n\nCan be used multiple times to refine results\n\nto limit number of range/section/shelf options, search first by room/floor and refine from there"),
        SG.Push(),
    ],
    [
        SG.Button("Search by Location Barcode", size=(25, 1), tooltip="use to find location inventory data by searching the barcode.\n\nrequires full spreadsheet to be loaded"),
        SG.Push(),
    ],
    [
        SG.Button("Search by Container Barcode", size=(25, 1), tooltip="use to find where a container is supposed to go based on its barcode.\n\nrequires full spreadsheet to be loaded"),
        SG.Push(),
    ],
    [
        SG.Button("Reload Spreadsheet", size=(25, 1), tooltip="Reloads the spreadsheet to reset values, needs to be pressed twice to clear all values.\n\nalso unlocks some fields from read-only status"),
        SG.Push(),
    ],
    [
        SG.Button("Close", size=(25, 1), tooltip="will close this program"),
    ],
]
layout = [
    [
        SG.Push(),
        SG.Text("Open login information"),
        SG.Radio("Yes", enable_events=True, key="-LOGIN_YES-", group_id="-login-", default=False),
        SG.Radio("No", enable_events=True, key="-LOGIN_NO-", group_id="-login-", default=True),
        SG.Button("Update", size=(8, 1))
    ],
    [
        SG.Push(),
        SG.Text("ArchivesSpace API address:", key="-ADDRESS-", visible=False),
        SG.Input(size=(50, 1), key="-API_URL-", default_text="enter api address here", visible=False)
    ],
    [
        SG.Push(),
        SG.Text("ArchivesSpace username:", key="-USERNAME-", visible=False),
        SG.Input(size=(50, 1), key="-API_USERNAME-", visible=False)
    ],
    [
        SG.Push(),
        SG.Text("ArchivesSpace password:", key="-PASSWORD-", visible=False),
        SG.Input(size=(50, 1), key="-API_PASSWORD-", password_char="#", visible=False)
    ],
    [
        SG.Push(),
        SG.Button("Test Login", size=(8, 1), key="-TEST_LOGIN-", visible=False),
        SG.Push()
    ],
    [
        SG.Text("Session Token:"),
        SG.Push(),
        SG.Input("", key="-SESSION_TOKEN-", readonly=True, size=(65, 1), disabled_readonly_background_color="PeachPuff2"),
    ],
    [
        SG.Push(),
        SG.Text("Location holdings report spreadsheet: "),
        SG.In(size=(50, 1), enable_events=True, key="-LOCATIONS-"),
        SG.FileBrowse(size=(8, 1), file_types=(("comma-separate values", "*.csv"), ("excel spreadsheet", "*.xlsx")))
    ],
    [
        SG.Push(),
        SG.Button("Load Spreadsheet"),
        SG.Push()
    ],
    [
        SG.HorizontalSeparator()
    ],
    [
        SG.Checkbox("Enable edit", key="-ENABLE_EDIT-"),
        SG.Push(),
        SG.Checkbox("Open container management/Circulation", key="-CONTAINER_MANAGEMENT-")
    ],
    [
        SG.Text("Container management stuff", key="-Test_case-", enable_events=True, visible=False)
    ],
    [
        SG.Push(),
        SG.Radio("Checkout to reference", visible=False, key="-REFERENCE_CHECKOUT-", group_id="-circulation-"),
        SG.Radio("Checkout", visible=False, key="-CHECKOUT-", group_id="-circulation-"),
        SG.Radio("Return", visible=False, key="-RETURN-", group_id="-circulation-"),
        SG.Radio("Transfer", visible=False, key="-TRANSFER-", group_id="-circulation-"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Container barcode: ", key="-BOX_BARCODE_TEXT-", visible=False),
        SG.In("", key="-BOX_BARCODE-", enable_events=True, visible=False),
    ],
    [
        SG.Push(),
        SG.Text("Location barcode: ", key="-CIRCULATION_LOCATION_TEXT-", visible=False),
        SG.In("", key="-CIRCULATION_LOCATION-", visible=False, enable_events=True),
    ],
    [
        SG.Push(),
        SG.Button("Circulate Container", size=(50, 1), enable_events=True, key="-CIRCULATE_CONTAINER-", visible=False),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Needed linear inches: ", key="-INCHES_TEXT-", visible=False),
        SG.In("", key="-INCHES-", visible=False),
    ],
    [
        SG.Button("Calculate Storage", visible=False, key="-CALCULATE_STORAGE-"),
        SG.Push(),
        SG.Button("Find me storage", visible=False, key="-FIND_ME_STORAGE-"),
    ],
    [
        SG.HorizontalSeparator()
    ],
    [
        SG.Push(),
        SG.Text("Location URI: "),
        SG.Input(size=(50, 1), key="-LOCATION_URI-", visible=True, readonly=True, disabled_readonly_background_color="PeachPuff2"),
    ],
    [
        SG.Push(),
        SG.Text("Location Profile: "),
        SG.Input(size=(50, 1), enable_events=True, key="-LOCATION_PROFILE-", readonly=True, disabled_readonly_background_color="PeachPuff2"),
    ],
    [
        SG.Push(),
        SG.Text("Updated location profile to...?"),
        SG.Combo(values=["", "GemTrac", "Narrow Width", "Standard Width"], key="-LOCATION_PROFILE_DROP-", enable_events=True),
        SG.Button("Update location profile", size=(19, 1))
    ],
    [
        SG.Push(),
        SG.Text("Location barcode: "),
        SG.Input(size=(50, 1), enable_events=True, key="-LOCATION_BARCODE-", disabled_readonly_background_color="PeachPuff2"),
        SG.Button("Update location barcode", size=(19, 1))
    ],
    [
        SG.Push(),
        SG.Text("Containers at location: "),
        SG.Combo(values=[""], default_value="", key="-TOP_CONTAINERS-", enable_events=True),
        SG.Text("Container barcode: "),
        SG.Input(size=(50, 1), enable_events=True, key="-TOP_CONTAINER_BARCODE-", disabled_readonly_background_color="PeachPuff2"),
        SG.Button("Update container barcode", size=(19, 1))
    ],
    [
        SG.Checkbox("Inventory range check", key="-INVENTORY_RANGE_CHECK-", enable_events=True, tooltip="Check this box to enable pulling all of the data for a set of shelving.\nNote that shelving must all be on the same floor/stack and end must not precede beginning\nMust not begin and end with same location"),
        SG.Push(),
        SG.Text(" ", key="-INVENTORY_RANGE_START-"),
        SG.Text("Floor: "),
        SG.Combo(values=[''], default_value='', key="-FLOOR-"),
        SG.Text("Room: "),
        SG.Combo(values=[''], default_value="", key="-ROOM-"),
        SG.Text("Range: "),
        SG.Combo(values=[''], key="-RANGE-"),
        SG.Text("Section: "),
        SG.Combo(values=[''], key="-SECTION-"),
        SG.Text("Shelf: "),
        SG.Combo(values=[''], key="-SHELF-"),
        #SG.Push()
    ],
    [
        SG.Checkbox("Whole room", key="-WHOLE_ROOM-", visible=False, enable_events=True),
        SG.Button("Generate Shelf list", key="-SHELF_LIST-", visible=False),
        SG.Push(),
        SG.Text("Range end", key="-INVENTORY_RANGE_END-", visible=False),
        SG.Text("Range: ", key="-RANGE_RANGE_TEXT-", visible=False),
        SG.Combo(values=[''], key="-RANGE_RANGE-", visible=False),
        SG.Text("Section: ", key="-RANGE_SECTION_TEXT-", visible=False),
        SG.Combo(values=[''], default_value='', key="-RANGE_SECTION-", visible=False),
        SG.Text("Shelf: ", key="-RANGE_SHELF_TEXT-", visible=False),
        SG.Combo(values=[''], key="-RANGE_SHELF-", visible=False),
    ],
    [
        SG.Push(),
        SG.Checkbox("Also generate PDF", key="-GEN_PDF-", visible=False, enable_events=True),
        SG.Checkbox("Also generate spreadsheet", key="-GEN_DF-", visible=False, enable_events=True),
    ],
    [
        SG.Text("Inventory range uses auto incrementing and cannot handle large numbers or text by default, include options below include EVERYTHING of that type\nUse Include Bonus for Bonus shelving, Include North/South/East/West for ranges against walls, Include 'atypical' to include locations", key="-WARNING-", visible=False, enable_events=True, text_color="red"),
    ],
    [
        SG.Push(),
        SG.Checkbox("Include Bonus shelving", key="-INCL_BONUS-", visible=False, enable_events=True),
        SG.Checkbox("Include North/South/East/West", key="-INCL_DIRECTIONS-", visible=False, enable_events=True),
        SG.Checkbox("Include atypical", key="-ATYPICAL-", visible=False, enable_events=True),
    ],
    [
        SG.Push(),
        SG.Pane([SG.Column(bottom_left_layout), SG.Column(bottom_middle_layout), SG.Column(bottom_right_layout)], orientation='h', expand_x=True, expand_y=True),
        SG.Push()
    ],
]

window = SG.Window(title="Inventory Management GUI",
                   layout=layout,
                   icon=my_icon64)

event, values = window.read()
while True:
    event, values = window.read()
    variables_dict = {}
    variables_dict["-API_URL-"] = values["-API_URL-"]
    variables_dict["-API_USERNAME-"] = values["-API_USERNAME-"]
    variables_dict["-API_PASSWORD-"] = values["-API_PASSWORD-"]
    variables_dict["-LOCATION_BARCODE-"] = values["-LOCATION_BARCODE-"]
    variables_dict['-TOP_CONTAINERS-'] = values["-TOP_CONTAINERS-"]
    variables_dict["-SESSION_TOKEN-"] = values["-SESSION_TOKEN-"]
    variables_dict['-BOX_BARCODE-'] = values['-BOX_BARCODE-']
    variables_dict['-CIRCULATION_LOCATION-'] = values['-CIRCULATION_LOCATION-']
    if values['-INCHES-'] == "":
        values['-INCHES-'] = "0"
    if values['-LOGIN_YES-'] is True:
        window['-ADDRESS-'].update(visible=True)
        window['-API_URL-'].update(visible=True)
        window['-USERNAME-'].update(visible=True)
        window['-API_USERNAME-'].update(visible=True)
        window['-PASSWORD-'].update(visible=True)
        window['-API_PASSWORD-'].update(visible=True)
        window['-TEST_LOGIN-'].update(visible=True)
    if values['-LOGIN_NO-'] is True:
        window['-ADDRESS-'].update(visible=False)
        window['-API_URL-'].update(visible=False)
        window['-USERNAME-'].update(visible=False)
        window['-API_USERNAME-'].update(visible=False)
        window['-PASSWORD-'].update(visible=False)
        window['-API_PASSWORD-'].update(visible=False)
        window['-TEST_LOGIN-'].update(visible=False)
    variables_dict['circulation'] = ""
    if values['-REFERENCE_CHECKOUT-'] is True:
        variables_dict['circulation'] = "reference"
    if values['-CHECKOUT-'] is True:
        variables_dict['circulation'] = "checkout"
    if values['-RETURN-'] is True:
        variables_dict['circulation'] = "return"
    if values['-TRANSFER-'] is True:
        variables_dict['circulation'] = "transfer"
    headers = {'SESSION': ''}
    location_key = ""
    if event == "-TEST_LOGIN-":
        try:
            headers = runner(variables_dict)
            print(headers)
        except:
            print("something is wrong, try again")
    #to load or relead spreadsheet data. written a little longer so that it returns fields to their native state rather 
    #than refined state
    if event == "Load Spreadsheet" or event == "Reload Spreadsheet":
        window['-LOCATION_PROFILE_DROP-'].update(values=[''])
        window['-FLOOR-'].update(values=[''])
        window['-ROOM-'].update(values=[''])
        window['-RANGE-'].update(values=[''])
        window['-SECTION-'].update(values=[''])
        window['-SHELF-'].update(values=[''])
        window['-RANGE_RANGE-'].update(values=[''])
        window['-RANGE_SECTION-'].update(values=[''])
        window['-RANGE_SHELF-'].update(values=[''])
        window['-TOP_CONTAINERS-'].update(values=[''])
        window['-LOCATION_URI-'].update("", readonly=True)
        window['-LOCATION_BARCODE-'].update("", readonly=False)
        window['-TOP_CONTAINER_BARCODE-'].update("", readonly=False)
        window['-LOCATION_PROFILE-'].update("")
        window['-LOCATION_PROFILE_DROP-'].update(values=["", "GemTrac", "Narrow Width", "Standard Width"])
        some_text = values['-LOCATIONS-']
        try:
            with open(some_text, "r", encoding="utf-8") as r:
                filedata = r.read()
                if not filedata.startswith("record"):
                    while not filedata.startswith("record"):
                        filedata = filedata[1:]
                    with open(some_text, "w") as w:
                        w.write(filedata)
                    w.close()
            inventory_data = PD.read_csv(values['-LOCATIONS-'], dtype=object)
            columns = ['containers_ils_item_id', 'containers_ils_holding_id', 'containers_records_linked_record_type', 'containers_records_identifier', 'containers_records_record_title']
            for item in columns:
                listy = inventory_data.columns
                if item in listy:
                    inventory_data = inventory_data.drop(columns=[item])
            inventory_data = inventory_data.drop_duplicates()
            inventory_data = inventory_data.fillna("no value")
            new_data_set = dict_converter(inventory_data)
            location_dictionary = new_data_set[0]
            item_dictionary = new_data_set[1]
            item_barcode_dictionary = new_data_set[2]
            window['-OUTPUT-'].update("spreadsheet loaded\n", append=True)
        except Exception as e:
            SG.popup_error_with_traceback("trouble loading spreadsheet, READ error message below to see if you can fix it.\n DID YOU REMOVE DIACRITICS FROM LOCATION HOLDINGS REPORT?", e)
            raise
    #to query spreadsheet by stacks coordinates. especially meant for times when no location barcode exists yet
    #can be iterable against floor/room. not iterable on range/section/shelf as those are a single field in the spreadsheet
    if values['-INVENTORY_RANGE_CHECK-'] is False:
        window["-INVENTORY_RANGE_START-"].update(" ")
        window['-WHOLE_ROOM-'].update(visible=False)
        window['-SHELF_LIST-'].update(visible=False)
        window['-INVENTORY_RANGE_END-'].update(visible=False)
        window["-RANGE_RANGE_TEXT-"].update(visible=False)
        window["-RANGE_RANGE-"].update(visible=False)
        window["-RANGE_SECTION_TEXT-"].update(visible=False)
        window["-RANGE_SECTION-"].update(visible=False)
        window["-RANGE_SHELF_TEXT-"].update(visible=False)
        window["-RANGE_SHELF-"].update(visible=False)
        window['-WARNING-'].update(visible=False)
        window['-GEN_PDF-'].update(visible=False)
        window['-GEN_DF-'].update(visible=False)
        window['-INCL_BONUS-'].update(visible=False)
        window['-INCL_DIRECTIONS-'].update(visible=False)
        window['-ATYPICAL-'].update(visible=False)
    if values['-INVENTORY_RANGE_CHECK-'] is True:
        window["-INVENTORY_RANGE_START-"].update("Range start")
        window['-WHOLE_ROOM-'].update(visible=True)
        window['-SHELF_LIST-'].update(visible=True)
        window['-INVENTORY_RANGE_END-'].update(visible=True)
        window["-RANGE_RANGE_TEXT-"].update(visible=True)
        window["-RANGE_RANGE-"].update(visible=True)
        window["-RANGE_SECTION_TEXT-"].update(visible=True)
        window["-RANGE_SECTION-"].update(visible=True)
        window["-RANGE_SHELF_TEXT-"].update(visible=True)
        window["-RANGE_SHELF-"].update(visible=True)
        window['-WARNING-'].update(visible=True)
        window['-GEN_PDF-'].update(visible=True)
        window['-GEN_DF-'].update(visible=True)
        window['-INCL_BONUS-'].update(visible=True)
        window['-INCL_DIRECTIONS-'].update(visible=True)
        window['-ATYPICAL-'].update(visible=True)
    if values["-CONTAINER_MANAGEMENT-"] is True:
        window['-Test_case-'].update(visible=True)
        window['-REFERENCE_CHECKOUT-'].update(visible=True)
        window['-CHECKOUT-'].update(visible=True)
        window['-RETURN-'].update(visible=True)
        window['-TRANSFER-'].update(visible=True)
        window['-BOX_BARCODE_TEXT-'].update(visible=True)
        window['-BOX_BARCODE-'].update(visible=True)
        window['-CIRCULATION_LOCATION_TEXT-'].update(visible=True)
        window['-CIRCULATION_LOCATION-'].update(visible=True)
        window['-CIRCULATE_CONTAINER-'].update(visible=True)
        window['-CALCULATE_STORAGE-'].update(visible=True)
        window['-INCHES_TEXT-'].update(visible=True)
        window['-INCHES-'].update(visible=True)
        window['-FIND_ME_STORAGE-'].update(visible=True)
    if values['-CONTAINER_MANAGEMENT-'] is False:
        window['-Test_case-'].update(visible=False)
        window['-REFERENCE_CHECKOUT-'].update(visible=False)
        window['-CHECKOUT-'].update(visible=False)
        window['-RETURN-'].update(visible=False)
        window['-TRANSFER-'].update(visible=False)
        window['-BOX_BARCODE_TEXT-'].update(visible=False)
        window['-BOX_BARCODE-'].update(visible=False)
        window['-CIRCULATION_LOCATION_TEXT-'].update(visible=False)
        window['-CIRCULATION_LOCATION-'].update(visible=False)
        window['-CIRCULATE_CONTAINER-'].update(visible=False)
        window['-CALCULATE_STORAGE-'].update(visible=False)
        window['-INCHES_TEXT-'].update(visible=False)
        window['-INCHES-'].update(visible=False)
        window['-FIND_ME_STORAGE-'].update(visible=False)
    if event == "-CIRCULATE_CONTAINER-":
        if values['-CIRCULATION_LOCATION-'] == "" or values['-CIRCULATION_LOCATION-'] == "no value":
            window['-OUTPUT-'].update("no barcode provided\nEnter a location barcode and try again\n", append=True)
        else:
            if "inventory_data" in locals() or "inventory_data" in globals():
                new_inventory = inventory_data
                new_inventory = new_inventory[new_inventory['location_barcode'] == values['-CIRCULATION_LOCATION-']]
                new_data = dict_converter(new_inventory)
                window['-OUTPUT-'].update("filtered spreadsheet data to applicable items\n", append=True)
                location_dictionary = new_data[0]
                listy = list(location_dictionary.keys())
                print(listy)
                if len(listy) == 0:
                    window['-OUTPUT-'].update("no matching barcode, check that it is entered into the system\n", append=True)
                if len(listy) > 1:
                    window['-OUTPUT-'].update("more than 1 matching location barcode, manual update needed\n", append=True)
                if len(listy) == 1:
                    my_circulation = circulation(variables_dict, location_dictionary)
                    if my_circulation == 200:
                        barcode = values['-BOX_BARCODE-']
                        #listy = list(location_dictionary.keys())
                        listy = listy[0]
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'record_title'] = location_dictionary[listy]['record_title']
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'building'] = location_dictionary[listy]['building']
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'floor'] = location_dictionary[listy]['floor']
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'room'] = location_dictionary[listy]['room']
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'location_url'] = listy
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'location_profile'] = location_dictionary[listy]["location_profile"]
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'location_barcode'] = location_dictionary[listy]['location_barcode']
                        inventory_data.loc[inventory_data['containers_top_container_barcode'] == barcode, 'location_in_room'] = location_dictionary[listy]['location_in_room']
                        try:
                            writer = inventory_data.to_csv(values['-LOCATIONS-'], index=False)
                        except:
                            window['-OUTPUT-'].update("trouble updating spreadsheet, is it open? If so, update manually and close for further updates\n", append=True)
                    else:
                        window['-OUTPUT-'].update(f"something wrong with location update for box with barcode {values['-BOX_BARCODE-']}\n", append=True)
            else:
                window['-OUTPUT-'].update("load inventory spreadsheet to continue\n", append=True)
    if event == "-CALCULATE_STORAGE-":
        window['-OUTPUT-'].update("trial successful\n", append=True)
        if "inventory_data" in locals() or "inventory_data" in globals():
            new_inventory = inventory_data
            if values['-FLOOR-'] != "":
                an_inventory = new_inventory['floor'].str.contains(values['-FLOOR-'])
                new_inventory = new_inventory[an_inventory]
            if values['-ROOM-'] != "":
                an_inventory = new_inventory['room'].str.contains(values['-ROOM-'])
                new_inventory = new_inventory[an_inventory]
            new_data_set = dict_converter(new_inventory)
            location_dictionary = new_data_set[0]
            new_space_dictionary = storage_space(location_dictionary)
        else:
            print("fail")
            window['-OUTPUT-'].update("you need to load the spreadsheet first\n")
    if event == "-FIND_ME_STORAGE-":
        new_inventory = inventory_data
        if values['-FLOOR-'] != "":
            an_inventory = new_inventory['floor'].str.contains(values['-FLOOR-'])
            new_inventory = new_inventory[an_inventory]
        if values['-ROOM-'] != "":
            an_inventory = new_inventory['room'].str.contains(values['-ROOM-'])
            new_inventory = new_inventory[an_inventory]
        new_data_set = dict_converter(new_inventory)
        location_dictionary = new_data_set[0]
        old_space_dictionary = storage_space(location_dictionary)
        contiguous = 0
        locations_list = []
        window['-OUTPUT-'].update("arranging locations to look through\n", append=True)
        for key in old_space_dictionary.keys():
            locations_list.append(old_space_dictionary[key]['location_in_room'])
        locations_list.sort()
        new_space_dictionary = {}
        for item in locations_list:
            for key in old_space_dictionary.keys():
                if item == old_space_dictionary[key]['location_in_room']:
                    new_space_dictionary[key] = old_space_dictionary[key]
                    window['-OUTPUT-'].update(".", append=True)
        window['-OUTPUT-'].update("\narrangement completed\n", append=True)
        starting_location = ""
        storage_list = "Available space at:\n"
        #starting_location = f"{new_space_dictionary[locations_list[0]]['floor']}, {new_space_dictionary[locations_list[0]]['room']}, {new_space_dictionary[locations_list[0]]['location_in_room']}"
        for key in new_space_dictionary.keys():
            current_location = f"{new_space_dictionary[key]['floor']}, {new_space_dictionary[key]['room']}, {new_space_dictionary[key]['location_in_room']}"
            if not starting_location == "":
                print(prior_location)
                tester = prior_location.split(", ")
                test1 = ""
                if tester[-1].startswith("Shelf"):
                    num1 = str(int(tester[-1].split(" ")[-1]) + 1)
                    while len(num1) < 2:
                        num1 = f"0{num1}"
                    num1 = f"Shelf {num1}"
                    test1 = prior_location.replace(tester[-1], num1)
                test2 = ""
                if tester[-2].startswith("Section") and not tester[-2].endswith("Bonus"):
                    num2 = str(int(tester[-2].split(" ")[-1]) + 1)
                    while len(num2) < 2:
                        num2 = f"0{num2}"
                    num2 = f"Section {num2}"
                    test2 = prior_location.replace(tester[-2], num2).replace(tester[-1], "Shelf 01")
                test3 = ""
                if tester[-3].startswith("Range"):
                    directions = ['North', 'South', 'East', 'West']
                    if not tester[-3].split(" ")[-1] in directions:
                        num3 = str(int(tester[-3].split(" ")[-1]) + 1)
                        while len(num3) < 2:
                            num3 = f"0{num3}"
                        num3 = f"Range {num3}"
                        test3 = prior_location.replace(tester[-3], num3).replace(tester[-2], "Section 01").replace(tester[-1], "Section 01")
                new_flag = True
                if current_location == test1 or current_location == test2 or current_location == test3:
                    new_flag = False
                if new_flag is True:
                    if contiguous >= int(values['-INCHES-']):
                        window['-INVENTORY_OUTPUT-'].update(f"{str(contiguous)} linear inches available starting at {starting_location}\n", append=True)
                        final_count = str(float(contiguous)/12).split(".")
                        storage_list = f"{storage_list}{str(contiguous)} linear inches ({final_count[0]}.{final_count[1][:2]} cubic ft.) available starting at {starting_location}\n"
                    starting_location = current_location
                    contiguous = 0
                prior_location = current_location
            else:
                starting_location = current_location
                prior_location = current_location
            '''
            contiguous_check = int(starting_line.split("/")[-1]) + 1
            if key != f"/locations/{str(contiguous_check)}":
                if contiguous >= int(values['-INCHES-']):
                    window['-INVENTORY_OUTPUT-'].update(f"{str(contiguous)} linear inches available starting at {starting_location}\n", append=True)
                    starting_location = f"{new_space_dictionary[key]['floor']}, {new_space_dictionary[key]['room']}, {new_space_dictionary[key]['location_in_room']}"
                    contiguous = 0
            starting_line = key
            '''
            eligible_list = ['RS', 'MS', 'LittleMS', 'no value']
            location_in_room = new_space_dictionary[key]['location_in_room']
            if "Range" in location_in_room and "Section" in location_in_room and "Shelf" in location_in_room:
                location_profile = new_space_dictionary[key]['location_profile']
                if location_profile == "no value":
                    location_profile = "Standard Width"
                space = space_dict[location_profile]
                for container in location_dictionary[key]['top_containers']:
                    if container['containers_container_profile'] in eligible_list:
                        space = space - space_dict[container['containers_container_profile']]
                contiguous += space
        storage_list = f"{storage_list}To print this out copy text into a text editor"
        SG.popup_scrolled(storage_list, title="Available space at:", size=(100, 35), modal=True)
    if event == "-SHELF_LIST-":
        new_inventory = inventory_data
        if values['-FLOOR-'] == "" and values['-ROOM-'] == "":
            window['-OUTPUT-'].update("At minimum choose a floor or room\n", append=True)
        if values['-FLOOR-'] != "":
            an_inventory = new_inventory['floor'].str.contains(values['-FLOOR-'])
            new_inventory = new_inventory[an_inventory]
        if values['-ROOM-'] != "":
            an_inventory = new_inventory['room'].str.contains(values['-ROOM-'])
            new_inventory = new_inventory[an_inventory]
        new_data_set = dict_converter(new_inventory)
        location_dictionary = new_data_set[0]
        locations_list = []
        for key in location_dictionary.keys():
            locations_list.append(location_dictionary[key]['location_in_room'])
        locations_list.sort()
        new_location_dictionary = {}
        for item in locations_list:
            for key in location_dictionary.keys():
                if item == location_dictionary[key]['location_in_room']:
                    new_location_dictionary[key] = location_dictionary[key]
        #swap newly arrange location
        location_dictionary = new_location_dictionary
        new_location_dictionary = 0
        new_location_dictionary = {}
        window['-OUTPUT-'].update("arranged selection in shelf order\n", append=True)
        if values['-WHOLE_ROOM-'] is True:
            window['-OUTPUT-'].update("compiling data based on whole room\n", append=True)
        if values['-WHOLE_ROOM-'] is False:
            option_list = []
            window['-OUTPUT-'].update("compiling data based on range of selected values\n", append=True)
            current = f"{values['-RANGE-']}, {values['-SECTION-']}, {values['-SHELF-']}"
            option_list.append(current)
            if values['-RANGE-'] != "" and values['-RANGE_RANGE-'] != "":
                end = f"{values['-RANGE_RANGE-']}, {values['-RANGE_SECTION-']}, {values['-RANGE_SHELF-']}"
                try:
                    range = int(values['-RANGE-'].split(" ")[-1])
                    end_range = int(values['-RANGE_RANGE-'].split(" ")[-1])
                except ValueError as e:
                    SG.popup_error_with_traceback("Could not convert location coordinates into something processable. Use checkboxes to include oddball (including map drawers), directional and Bonus shelving!!!", e)
                    raise
                if "Range" not in values['-RANGE-'] or "Range" not in values['-RANGE_RANGE-'] or "Section" not in values['-SECTION-'] or "Section" not in values['-RANGE_SECTION-'] or "Shelf" not in values['-SHELF-'] or "Shelf" not in values['-RANGE_SHELF-']:
                    window['-OUTPUT-'].update("This functionality is meant ONLY for numeric Range/Section/Shelf, for other types of shelving use the checkboxes below or use 'Whole room'")
                else:
                    if values['-SECTION-'] != "":
                        section = int(values['-SECTION-'].split(" ")[-1])
                    else:
                        section = 0
                    if values['-SHELF-'] != "":
                        shelf = int(values['-SHELF-'].split(" ")[-1])
                    else:
                        shelf = 0
                    if values['-RANGE_SECTION-'] != "":
                        end_section = int(values['-RANGE_SECTION-'].split(" ")[-1])
                    else:
                        end_section = 30
                    if values['-RANGE_SHELF-'] != "":
                        end_shelf = int(values['-RANGE_SHELF-'].split(" ")[-1])
                    else:
                        end_shelf = 20
                    while current != end:
                        new_current = ""
                        window['-OUTPUT-'].update(f"{current}\n", append=True)
                        if range == end_range:
                            new_range = str(range)
                            while len(new_range) < 2:
                                new_range = f"0{new_range}"
                            window['-OUTPUT-'].update("Range match\n", append=True)
                            if section == end_section:
                                new_section = str(section)
                                while len(new_section) < 2:
                                    new_section = f"0{new_section}"
                                window['-OUTPUT-'].update("Section match\n", append=True)
                                if shelf != end_shelf:
                                    shelf += 1
                                    new_shelf = str(shelf)
                                    while len(new_shelf) < 2:
                                        new_shelf = f"0{new_shelf}"
                                    new_current = f"Range {new_range}, Section {new_section}, Shelf {new_shelf}"
                                    option_list.append(new_current)
                                    current = new_current
                                    new_current = ""
                            if section != end_section:
                                if shelf == 20:
                                    section += 1
                                    shelf = 0
                                if section == 30:
                                    range += 1
                                shelf += 1
                                new_range = str(range)
                                while len(new_range) < 2:
                                    new_range = f"0{new_range}"
                                new_section = str(section)
                                while len(new_section) < 2:
                                    new_section = f"0{new_section}"
                                new_shelf = str(shelf)
                                while len(new_shelf) < 2:
                                    new_shelf = f"0{new_shelf}"
                                new_current = f"Range {new_range}, Section {new_section}, Shelf {new_shelf}"
                                option_list.append(new_current)
                                current = new_current
                                new_current = ""
                        if range != end_range:
                            if shelf == 20:
                                section += 1
                                shelf = 0
                            if section == 30:
                                range += 1
                                section = 0
                            shelf += 1
                            new_range = str(range)
                            while len(new_range) < 2:
                                new_range = f"0{new_range}"
                            new_section = str(section)
                            while len(new_section) < 2:
                                new_section = f"0{new_section}"
                            new_shelf = str(shelf)
                            while len(new_shelf) < 2:
                                new_shelf = f"0{new_shelf}"
                            new_current = f"Range {new_range}, Section {new_section}, Shelf {new_shelf}"
                            option_list.append(new_current)
                            current = new_current
                            new_current = ""
            option_list.sort()
            for item in option_list:
                for key in location_dictionary.keys():
                    if item == location_dictionary[key]['location_in_room']:
                        new_location_dictionary[key] = location_dictionary[key]
                    if values['-INCL_BONUS-'] is True:
                        if "Bonus" in location_dictionary[key]['location_in_room']:
                            new_location_dictionary[key] = location_dictionary[key]
                    if values['-INCL_DIRECTIONS-'] is True:
                        dir_list = ["North", "South", "West", "East"]
                        for compass_direction in dir_list:
                            if compass_direction in location_dictionary[key]['location_in_room']:
                                new_location_dictionary[key] = location_dictionary[key]
                    if values['-ATYPICAL-'] is True:
                        dir_list = ["Cabinet", "Drawer", "TP", "Case", "OS deep shelving", "GemTrac"]
                        for oddball in dir_list:
                            if oddball in location_dictionary[key]['location_in_room']:
                                new_location_dictionary[key] = location_dictionary[key]
            #update sorting to handle any additions such as Bonus or directional shelving
            re_sort = []
            for key in new_location_dictionary.keys():
                re_sort.append(new_location_dictionary[key]['location_in_room'])
            re_sort.sort()
            location_dictionary = new_location_dictionary
            new_location_dictionary = {}
            for item in re_sort:
                for key in location_dictionary.keys():
                    if location_dictionary[key]['location_in_room'] == item:
                        new_location_dictionary[key] = location_dictionary[key]
            location_dictionary = new_location_dictionary
        print_string = ""
        for key in location_dictionary.keys():
            new_string = f"{location_dictionary[key]['floor']}, {location_dictionary[key]['room']}, {location_dictionary[key]['location_in_room']} ({location_dictionary[key]['location_profile']})\n"
            for container in location_dictionary[key]['top_containers']:
                if len(location_dictionary[key]['top_containers']) == 1 and container['containers_top_container_indicator'] == 'no value':
                    window['-OUTPUT-'].update("Nothing on shelf\n", append=True)
                    new_string = f"{new_string}\tNo holdings\n"
                else:
                    new_string = f"{new_string}\t{container['containers_top_container_indicator']}: {container['containers_container_profile']}\n"
            new_string = f"{new_string}{storage_shelf(location_dictionary[key])}"
            print_string = f"{print_string}{new_string}"
        if values['-GEN_PDF-'] is True:
            try:
                document = "something"
                document = {}
                document['style'] = pdf_style
                document['formats'] = pdf_formats
                document['running_sections'] = {'header': document_header, 'footer': document_footer}
                document['sections'] = []
                section1 = {}
                document['sections'].append(section1)
                section1['running_sections'] = ['footer']
                section1['content'] = content1 = []
                content1.append(global_header)
                content1.append(print_string)
                with open(f"inventory_of_{values['-ROOM-']}.pdf", 'wb') as w:
                    build_pdf(document, w)
                w.close()
            except:
                window['-OUTPUT-'].update("trouble generating pdf\n", append=False)
        if values['-GEN_DF-'] is True:
            list_of_lists = []
            columns = ['in stacks', 'missing', 'coordinates', 'shelf type', 'container', 'container barcode',
                       'container type']
            for key in location_dictionary.keys():
                coordinates = f"{location_dictionary[key]['floor']}, {location_dictionary[key]['room']}, {location_dictionary[key]['location_in_room']}"
                shelf_type = location_dictionary[key]['location_profile']
                for container in location_dictionary[key]['top_containers']:
                    df1 = ["", "", coordinates, shelf_type, container['containers_top_container_indicator'], container['containers_top_container_barcode'], container['containers_container_profile']]
                    list_of_lists.append(df1)
            new_dataframe = PD.DataFrame(list_of_lists, columns=columns)
            writer = new_dataframe.to_excel(f"inventory_of_{values['-ROOM-']}.xlsx", index=False)
        SG.popup_scrolled(print_string, title="Shelf inventory", size=(100, 35), modal=True)
        print("something")
    if event == "Search By Location Coordinates":
        aggregated = f"{values['-RANGE-']}, {values['-SECTION-']}, {values['-SHELF-']}"
        window['-TOP_CONTAINER_BARCODE-'].update("", readonly=False)
        new_inventory = inventory_data
        if values['-FLOOR-'] != "":
            an_inventory = new_inventory['floor'].str.contains(values['-FLOOR-'])
            new_inventory = new_inventory[an_inventory]
        if values['-ROOM-'] != "":
            an_inventory = new_inventory['room'].str.contains(values['-ROOM-'])
            new_inventory = new_inventory[an_inventory]
        if aggregated != ", , ":
            an_inventory = new_inventory['location_in_room'].str.contains(aggregated)
            new_inventory = new_inventory[an_inventory]
        new_data_set = dict_converter(new_inventory)
        location_dictionary = new_data_set[0]
        item_dictionary = new_data_set[1]
        item_barcode_dictionary = new_data_set[2]
        if len(location_dictionary) > 1:
            window['-OUTPUT-'].update(f"filtered down to {len(location_dictionary)} shelves\ncontinue filtering down\n", append=True)
        if len(location_dictionary) == 1:
            window['-OUTPUT-'].update("jackpot\n", append=True)
            for key in location_dictionary.keys():
                window['-LOCATION_URI-'].update(key)
                window['-LOCATION_URI-'].update(readonly=True)
                window['-LOCATION_BARCODE-'].update(location_dictionary[key]['location_barcode'])
                window['-LOCATION_BARCODE-'].update(readonly=False)
                if location_dictionary[key]['location_barcode'] != "no value":
                    window['-LOCATION_BARCODE-'].update(readonly=True)
                window['-LOCATION_PROFILE-'].update(location_dictionary[key]['location_profile'])
                barcode_set = []
                window['-INVENTORY_OUTPUT-'].update("", append=False)
                for container in location_dictionary[key]['top_containers']:
                    window['-INVENTORY_OUTPUT-'].update(f"{container['containers_top_container_indicator']}: barcode {container['containers_top_container_barcode']}\n", append=True)
                    barcode_set.append(container['containers_top_container_indicator'])
                barcode_set = list(set(barcode_set))
                barcode_set.sort()
                window['-TOP_CONTAINERS-'].update(values=barcode_set)
    #to query spreadsheet by location barcode. Will yield all location info including top containers assigned to it
    if event == "Search by Location Barcode":
        if values['-LOCATION_BARCODE-'] == "" or values['-LOCATION_BARCODE-'] == "no value":
            window['-OUTPUT-'].update("no barcode provided\nTry a different method or enter a valid barcode", append=True)
        else:
            new_inventory = inventory_data
            new_inventory = new_inventory[new_inventory['location_barcode'] == values['-LOCATION_BARCODE-']]
            new_data_set = dict_converter(new_inventory)
            location_dictionary = new_data_set[0]
            item_dictionary = new_data_set[1]
            item_barcode_dictionary = new_data_set[2]
            if len(location_dictionary) == 0:
                window['-OUTPUT-'].update("no matching barcode, check that it is entered correctly\n", append=True)
            if len(location_dictionary) > 1:
                window['-OUTPUT-'].update("more than one barcode match, manual system update is needed\n", append=True)
            if len(location_dictionary) == 1:
                window['-OUTPUT-'].update("jackpot\n", append=True)
                for key in location_dictionary.keys():
                    window['-LOCATION_URI-'].update(key, readonly=True)
                    window['-LOCATION_BARCODE-'].update(readonly=True)
                    barcode_set = []
                    window['-INVENTORY_OUTPUT-'].update("", append=False)
                    for container in location_dictionary[key]['top_containers']:
                        window['-INVENTORY_OUTPUT-'].update(f"{container['containers_top_container_indicator']}: barcode {container['containers_top_container_barcode']}\n", append=True)
                        barcode_set.append(container['containers_top_container_indicator'])
                    barcode_set = list(set(barcode_set))
                    barcode_set.sort()
                    window['-TOP_CONTAINERS-'].update(values=barcode_set)
    #to query the spreadsheet by barcode for a container. use for determining where a box goes
    if event == "Search by Container Barcode":
        new_inventory = inventory_data
        new_inventory = new_inventory[new_inventory['containers_top_container_barcode'] == values['-TOP_CONTAINER_BARCODE-']]
        new_data_set = dict_converter(new_inventory)
        location_dictionary = new_data_set[0]
        item_dictionary = new_data_set[1]
        item_barcode_dictionary = new_data_set[2]
        for key in location_dictionary.keys():
            window['-LOCATION_URI-'].update(key, readonly=True)
            window['-LOCATION_BARCODE-'].update(location_dictionary[key]['location_barcode'], readonly=True)
            window['-INVENTORY_OUTPUT-'].update("", append=False)
            window['-INVENTORY_OUTPUT-'].update(f"Box {location_dictionary[key]['top_containers'][0]['containers_top_container_indicator']} should be located at {location_dictionary[key]['building']}, {location_dictionary[key]['floor']}, {location_dictionary[key]['room']}, {location_dictionary[key]['location_in_room']}\n", append=True)
            container_values = location_dictionary[key]['top_containers'][0]['containers_top_container_indicator']
            rss = location_dictionary[key]['location_in_room'].split(', ')
            window['-TOP_CONTAINERS-'].update(values=[container_values])
            if len(rss) > 1:
                window['-FLOOR-'].update(values=[location_dictionary[key]['floor']])
                window['-ROOM-'].update(values=[location_dictionary[key]['room']])
                window['-RANGE-'].update(values=[rss[0]])
                window['-SECTION-'].update(values=[rss[1]])
                window['-SHELF-'].update(values=[rss[2]])
    #to pull out the barcode information for a container as a specific location. operates as on-change from the drop-down menu
    if event == '-TOP_CONTAINERS-':
        top_container = values['-TOP_CONTAINERS-']
        new_data_set = dict_converter(new_inventory)
        location_dictionary = new_data_set[0]
        for container in location_dictionary[values['-LOCATION_URI-']]['top_containers']:
            if container['containers_top_container_indicator'] == top_container:
                window['-TOP_CONTAINER_BARCODE-'].update(container['containers_top_container_barcode'])
                if container['containers_top_container_barcode'] != "no value":
                    window['-TOP_CONTAINER_BARCODE-'].update(readonly=True)
                else:
                    window['-TOP_CONTAINER_BARCODE-'].update(readonly=False)
    #function to assign barcodes to a location while doing inventory work
    #first ensure the edit box is checked and you are logged into the system.
    #if that checks out get the most recent version of the location, add the barcode and push up the changes
    #write barcode for location back to file so you don't have to export a new copy every time
    if event == "Update location barcode":
        if values['-ENABLE_EDIT-'] is True:
            if values['-SESSION_TOKEN-'] != "":
                if len(location_dictionary) == 1:
                    keys = list(location_dictionary.keys())
                    if values['-LOCATION_BARCODE-'] != "no value" and values['-LOCATION_BARCODE-'] != "":
                        if values['-LOCATION_BARCODE-'] != location_dictionary[values['-LOCATION_URI-']]['location_barcode']:
                            the_url = f"{values['-API_URL-']}{keys[0]}"
                            headers = {'X-ArchivesSpace-Session': values['-SESSION_TOKEN-']}
                            something = requests.get(the_url, headers=headers).json()
                            something['barcode'] = values['-LOCATION_BARCODE-']
                            response = requests.post(the_url, json=something, headers=headers)
                            if response.status_code == 200:
                                window['-OUTPUT-'].update("update to location barcode successful\n", append=True)
                                try:
                                    inventory_data.loc[inventory_data['location_url'] == values['-LOCATION_URI-'], 'location_barcode'] = values['-LOCATION_BARCODE-']
                                    writer = inventory_data.to_csv(values['-LOCATIONS-'], index=False)
                                except:
                                    window['-OUTPUT-'].update("trouble updating spreadsheet, is it open? If so, update manually and close for further updates\n", append=True)
                        else:
                            window['-OUTPUT-'].update("trying to update barcode to same value, try again\n", append=False)
                    else:
                        window['-OUTPUT-'].update("will not update to null/no value barcodes\n", append=True)
                else:
                    window['-OUTPUT-'].update("need to narrow location single spot before proceeding\n", append=True)
            else:
                window['-OUTPUT-'].update("need to log into Aspace system to make updates\n", append=True)
        else:
            window['-OUTPUT-'].update("check enable edit to proceed\n", append=True)
    #function to assign a location profile for a shelf location while doing inventory work
    #first ensure the edit box is checked and you are logged into the system.
    #if that checks out get the most recent version of the location data, add or replace existing location profile info  and push up the changes
    #write location profile info for location back to file so you don't have to export a new copy every time
    if event == "Update location profile":
        if values['-ENABLE_EDIT-'] is True:
            if values['-SESSION_TOKEN-'] != "":
                if len(location_dictionary) == 1:
                    keys = list(location_dictionary.keys())
                    the_url = f"{values['-API_URL-']}{keys[0]}"
                    headers = {'X-ArchivesSpace-Session': values['-SESSION_TOKEN-']}
                    if values['-LOCATION_PROFILE_DROP-'] != "" and values['-LOCATION_PROFILE_DROP-'] != values['-LOCATION_PROFILE-']:
                        if values['-LOCATION_PROFILE_DROP-'] == "GemTrac":
                            location_profile = "/location_profiles/2"
                        elif values['-LOCATION_PROFILE_DROP-'] == "Narrow Width":
                            location_profile = "/location_profiles/3"
                        elif values['-LOCATION_PROFILE_DROP-'] == "Standard Width":
                            location_profile = "/location_profiles/1"
                        something = requests.get(the_url, headers=headers).json()
                        if "location_profile" in something.keys():
                            old_value = something['location_profile']['ref']
                            if old_value != location_profile:
                                something['location_profile']['ref'] = location_profile
                                my_response = requests.post(the_url, json=something, headers=headers)
                                if my_response.status_code == 200:
                                    window['-OUTPUT-'].update("location profile update successful\n", append=True)
                                    try:
                                        inventory_data.loc[inventory_data['location_url'] == values['-LOCATION_URI-'], 'location_profile'] = values['-LOCATION_PROFILE_DROP-']
                                        writer = inventory_data.to_csv(values['-LOCATIONS-'], index=False)
                                    except:
                                        window['-OUTPUT-'].update("trouble updating spreadsheet, is it open? If so, update manually and close for further updates\n", append=True)
                                else:
                                    window['-OUTPUT-'].update("location profile update failed\n", append=True)
                            else:
                                window['-OUTPUT-'].update(f"trying to update to same location profile, use something different\n", append=True)
                        else:
                            something['location_profile'] = {'ref': location_profile}
                            my_response = requests.post(the_url, json=something, headers=headers)
                            if my_response.status_code == 200:
                                window['-OUTPUT-'].update("location profile update successful\n", append=True)
                                try:
                                    inventory_data.loc[inventory_data['location_url'] == values['-LOCATION_URI-'], 'location_profile'] = values['-LOCATION_PROFILE_DROP-']
                                    writer = inventory_data.to_csv(values['-LOCATIONS-'], index=False)
                                except:
                                    window['-OUTPUT-'].update("trouble updating spreadsheet, is it open? If so, update manually and close for further updates\n", append=True)
                            else:
                                window['-OUTPUT-'].update("location profile update failed\n", append=True)
                    else:
                        window['-OUTPUT-'].update("need to select a proper location profile\n", append=True)
                else:
                    window['-OUTPUT-'].update("need to narrow the location to a single spot before proceeding\n", append=True)
            else:
                window['-OUTPUT-'].update("need to log into Aspace system to make updates\n", append=True)
        else:
            window['-OUTPUT-'].update(f"check enable edit to proceed\n", append=True)
    #function to assign barcodes to a box while doing inventory work
    #first ensure the edit box is checked and you are logged into the system.
    #if that checks out get the most recent version of the container, add the barcode and push up the changes
    #write barcode for container back to file so you don't have to export a new copy every time
    if event == "Update container barcode":
        if values['-ENABLE_EDIT-'] is True:
            if values['-SESSION_TOKEN-'] != "":
                headers = {"X-ArchivesSpace-Session": values['-SESSION_TOKEN-']}
                if values['-TOP_CONTAINER_BARCODE-'] != "no value" and values['-TOP_CONTAINER_BARCODE-'] != "":
                    container_set = requests.get(f"{values['-API_URL-']}/repositories/2/find_by_id/top_containers", headers=headers, params={"indicator[]": values['-TOP_CONTAINERS-']}).json()
                    if len(container_set['top_containers']) == 1:
                        my_container = container_set['top_containers'][0]
                        my_container_json = requests.get(f"{values['-API_URL-']}{my_container['ref']}", headers=headers).json()
                        my_container_json['barcode'] = values['-TOP_CONTAINER_BARCODE-']
                        response = requests.post(f"{values['-API_URL-']}{my_container['ref']}", headers=headers, json=my_container_json)
                        if response.status_code == 200:
                            window['-OUTPUT-'].update("updated container barcode succesfully\n", append=True)
                            try:
                                inventory_data.loc[inventory_data['containers_top_container_indicator'] == values['-TOP_CONTAINERS-'], 'containers_top_container_barcode'] = values['-TOP_CONTAINER_BARCODE-']
                                writer = inventory_data.to_csv(values['-LOCATIONS-'], index=False)
                            except:
                                window['-OUTPUT-'].update("trouble updating spreadsheet, is it open? If so, update manually and close for further updates\n", append=True)
                        else:
                            window['-OUTPUT-'].update("problem updating top container barcode, you should look into that\n", append=True)
                    else:
                        window['-OUTPUT-'].update("looks like more than one top container has that name, review and try again\n", append=True)
                else:
                    window['-OUTPUT-'].update("will not update to null/no value barcodes\n", append=True)
            else:
                window['-OUTPUT-'].update("need to log into Aspace system to make update\n", append=True)
        else:
            window['-OUTPUT-'].update("check enable edit to proceed\n", append=True)
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()


