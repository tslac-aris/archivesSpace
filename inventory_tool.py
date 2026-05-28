import pandas as PD
import os
import sys
import PySimpleGUI as SG
import requests
import json

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
    if values['-SECTION-'] == "":
        location_section = list(set(location_section))
        location_section.append("")
        location_section.sort()
        window['-SECTION-'].update(values=location_section)
    if values['-SHELF-'] == "":
        location_shelf = list(set(location_shelf))
        location_shelf.append("")
        location_shelf.sort()
        window['-SHELF-'].update(values=location_shelf)
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
        SG.Push(),
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
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Pane([SG.Column(bottom_left_layout), SG.Column(bottom_middle_layout), SG.Column(bottom_right_layout)], orientation='h', expand_x=True, expand_y=True),
        SG.Push()
    ],
]

window = SG.Window(title="Barcoder GUI", layout=layout)

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
        window['-TOP_CONTAINERS-'].update(values=[''])
        window['-LOCATION_URI-'].update("", readonly=True)
        window['-LOCATION_BARCODE-'].update("", readonly=False)
        window['-TOP_CONTAINER_BARCODE-'].update("", readonly=False)
        window['-LOCATION_PROFILE-'].update("")
        window['-LOCATION_PROFILE_DROP-'].update(values=["", "GemTrac", "Narrow Width", "Standard Width"])
        some_text = values['-LOCATIONS-']
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
    #to query spreadsheet by stacks coordinates. especially meant for times when no location barcode exists yet
    #can be iterable against floor/room. not iterable on range/section/shelf as those are a single field in the spreadsheet
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


