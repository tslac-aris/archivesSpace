import requests
import PySimpleGUI as SG
import pandas as PD
from datetime import datetime

default_location = {'jsonmodel_type': 'container_location',
                    'ref': 'something',
                    'start_date': '2026-05-11',
                    'status': 'current'}

def row_converter(row, listy):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in listy:
        pictionary[item] = str(row[count])
        count += 1
    return pictionary

def spreadsheet_converter(spreadsheet):
    df = ""
    spreadsheet = variables_dict['-LOCATIONS-']
    spreadsheet_extension = spreadsheet.split('.')[-1]
    spreadsheet_dict = {}
    try:
        if spreadsheet_extension == 'csv':
            df = PD.read_csv(spreadsheet, dtype=object)
            window['-OUTPUT-'].update("spreadsheet loaded okay\n", append=True)
        if spreadsheet_extension == 'xlsx':
            df = PD.read_excel(spreadsheet, dtype=object)
            window['-OUTPUT-'].update("spreadsheet loaded okay\n", append=True)
        print(df[:5])
        listy = df.columns
        for row in df.itertuples():
            valuables = row_converter(row, listy)
            spreadsheet_dict[valuables['barcode']] = valuables['URI']
        window['-SPREADSHEET-'].update(spreadsheet_dict)
        return spreadsheet_dict
    except:
        window['-OUTPUT-'].update("failed to load spreadsheet, look into problem and try again\n", append=True)

def runner(variables_dict):
    headers = requests.post(f"{variables_dict['-API_URL-']}/users/{variables_dict['-API_USERNAME-']}/login", params={"password": variables_dict['-API_PASSWORD-']}).json()
    window['-OUTPUT-'].update(f"{headers}\n", append=True)
    window['-SESSION_TOKEN-'].update(headers['session'])
    print(headers)

def main_scan(variables_dict, spreadsheet_dict):
    if variables_dict['-SESSION_TOKEN-'] == "":
        try:
            headers = requests.post(f"{variables_dict['-API_URL-']}/users/{variables_dict['-API_USERNAME-']}/login",
                                    params={"password": variables_dict['-API_PASSWORD-']}).json()
            headers = {"session": headers["session"]}
            window['-SESSION_TOKEN-'].update(headers['session'])
            variables_dict['-SESSION_TOKEN-'] = headers['session']
        except:
            window['-OUTPUT-'].update("something wrong with login\n", append=True)
            return
    headers = {'X-ArchivesSpace-Session': variables_dict['-SESSION_TOKEN-']}
    print(headers)
    try:
        if variables_dict['-BOX_BARCODE-'] != "" and variables_dict['-LOCATION_BARCODE-'] != "":
            top_container = requests.get(f"{variables_dict['-API_URL-']}/repositories/2/find_by_id/top_containers", params={"barcode[]": variables_dict['-BOX_BARCODE-'], "resolve[]": "top_containers"}, headers=headers).json()
            top_container_URI = f'{variables_dict["-API_URL-"]}{top_container["top_containers"][0]["ref"]}'
            print(top_container)
            top_container_data = top_container["top_containers"][0]["_resolved"]
            location_uri = spreadsheet_dict[variables_dict["-LOCATION_BARCODE-"]]
            print(top_container_data)
            current_location = default_location
            current_location['ref'] = f"{location_uri}"
            current_time = datetime.today().strftime('%Y-%m-%d')
            current_location['start_date'] = current_time
            top_container_data.pop('long_display_string')
            if "internal_note" not in top_container_data.keys():
                top_container_data['internal_note'] = ""
            if variables_dict['-STATUS-'] == "checked out":
                top_container_data['internal_note'] = f"{top_container_data['internal_note']}Checked out to barcode location {variables_dict['-LOCATION_BARCODE-']} on {current_time}.\n"
                top_container_data['container_locations'].append(current_location)
            if variables_dict['-STATUS-'] == "checked in":
                top_container_data['internal_note'] = f"{top_container_data['internal_note']}Checked in to barcode location {variables_dict['-LOCATION_BARCODE-']} on {current_time}.\n"
                top_container_data['container_locations'] = [current_location]
            if variables_dict['-STATUS-'] == "transferred":
                top_container_data['internal_note'] = f"{top_container_data['internal_note']}Transferred to barcode location {variables_dict['-LOCATION_BARCODE-']} on {current_time}.\n"
                top_container_data['container_locations'] = [current_location]
            response = requests.post(top_container_URI, json=top_container_data, headers=headers)
            window['-OUTPUT-'].update(f"{response.status_code}\n", append=True)
        else:
            window['-OUTPUT-'].update("missing one or both barcodes, fix and try again\n", append=True)
        return headers
    except:
        print("trouble updating the location of this container, try doing it manually")
        return headers


SG.theme("DarkGreen")
layout = [
    [
        SG.Text("Open login information"),
        SG.Radio("Yes", enable_events=True, key="-LOGIN_YES-", group_id="-login-", default=False),
        SG.Radio("No", enable_events=True, key="-LOGIN_NO-", group_id="-login-", default=True),
        SG.Button("Update")
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
        SG.Button("Test Login", key="-TEST_LOGIN-", visible=False),
        SG.Push()
    ],
    [
        SG.Text("Session Token:"),
        SG.Push(),
        SG.Input("", key="-SESSION_TOKEN-", readonly=True, size=(65, 1)),
    ],
    [
        SG.Push(),
        SG.Text("For batch mode only"),
        SG.Checkbox("Batch mode", key="-BATCH_MODE-"),
        SG.In(size=(50, 1), enable_events=True, key="-BATCH_MODE_SPREADSHEET-"),
        SG.FileBrowse(file_types=(("comma-separated values", "*.csv"), ("excel spreadsheet", "*.xlsx")))
    ],
    [
        SG.Push(),
        SG.Text("Location data spreadsheet location: "),
        SG.In(size=(50, 1), enable_events=True, key="-LOCATIONS-"),
        SG.FileBrowse(file_types=(("comma-separate values", "*.csv"), ("excel spreadsheet", "*.xlsx")))
    ],
    [
        SG.Push(),
        SG.Button("Load Spreadsheet"),
        SG.Push()
    ],
    [
        SG.Text("Spreadsheet sample:"),
        SG.Push(),
        SG.In(key="-SPREADSHEET-", readonly=True, size=(65, 1)),
    ],
    [
        SG.HorizontalSeparator()
    ],
    [
        SG.Push(),
        SG.Radio("Checkout", key="-CHECKED_OUT-", group_id="-checkout-", default=True),
        SG.Radio("Return", key="-CHECKED_IN-", group_id="-checkout-", default=False),
        SG.Radio("Transfer", key="-TRANSFER-", group_id="-checkout-", default=False),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Box barcode"),
        SG.In(size=(50, 1), enable_events=True, key="-BOX_BARCODE-")
    ],
    [
        SG.Push(),
        SG.Text("New location barcode"),
        SG.In(size=(50, 1), enable_events=True, key="-LOCATION_BARCODE-")
    ],
    [
        SG.Button("Update location", tooltip="Click to update location data", bind_return_key=False),
        SG.Push(),
        SG.Button("Upload batch update", tooltip="Click to upload batch update"),
    ],
    [
        SG.Push(),
        SG.Button("Close"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="Dialog box for tasks as they go\n", size=(70, 10), auto_refresh=True, key="-OUTPUT-", autoscroll=True, border_width=5),
        SG.Push()
    ]
]

window = SG.Window(title="Barcoder GUI", layout=layout)

event, values = window.read()
while True:
    event, values = window.read()
    variables_dict = {}
    variables_dict["-API_URL-"] = values["-API_URL-"]
    variables_dict["-API_USERNAME-"] = values["-API_USERNAME-"]
    variables_dict["-API_PASSWORD-"] = values["-API_PASSWORD-"]
    variables_dict["-LOCATIONS-"] = values["-LOCATIONS-"]
    variables_dict["-BATCH_MODE-"] = values["-BATCH_MODE-"]
    variables_dict["-BATCH_MODE_SPREADSHEET-"] = values["-BATCH_MODE_SPREADSHEET-"]
    variables_dict["-BOX_BARCODE-"] = values["-BOX_BARCODE-"]
    variables_dict["-LOCATION_BARCODE-"] = values["-LOCATION_BARCODE-"]
    variables_dict["-SESSION_TOKEN-"] = values["-SESSION_TOKEN-"]
    variables_dict["-SPREADSHEET-"] = values["-SPREADSHEET-"]
    variables_dict["-STATUS-"] = "checked out"
    if values['-CHECKED_IN-'] is True:
        variables_dict['-STATUS-'] = "checked in"
    if values['-TRANSFER-'] is True:
        variables_dict['-STATUS-'] = "transferred"
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
    if event == "-TEST_LOGIN-":
        try:
            headers = runner(variables_dict)
            print(headers)
        except:
            print("something is wrong, try again")
    if event == "Load Spreadsheet":
        spreadsheet_dict = spreadsheet_converter(variables_dict['-SPREADSHEET-'])
        print(spreadsheet_dict)
        '''
        df = ""
        spreadsheet = variables_dict['-LOCATIONS-']
        spreadsheet_extension = spreadsheet.split('.')[-1]
        spreadsheet_dict = {}
        try:
            if spreadsheet_extension == 'csv':
                df = PD.read_csv(spreadsheet, dtype=object)
                window['-OUTPUT-'].update("spreadsheet loaded okay\n", append=True)
            if spreadsheet_extension == 'xlsx':
                df = PD.read_excel(spreadsheet, dtype=object)
                window['-OUTPUT-'].update("spreadsheet loaded okay\n", append=True)
            print(df[:5])
            listy = df.columns
            for row in df.itertuples():
                valuables = row_converter(row, listy)
                spreadsheet_dict[valuables['barcode']] = valuables['URI']
            window['-SPREADSHEET-'].update(spreadsheet_dict)
        except:
            window['-OUTPUT-'].update("failed to load spreadsheet, look into problem and try again\n", append=True)
            continue
        '''
    if event == "Update location":
        if values['-BATCH_MODE-'] is False:
            spreadsheet_dict = spreadsheet_converter(variables_dict['-SPREADSHEET-'])
            headers = main_scan(variables_dict, spreadsheet_dict)
            window['-BOX_BARCODE-'].update("")
            window['-LOCATION_BARCODE-'].update("")
        if values['-BATCH_MODE-'] is True:
            with open(variables_dict['-BATCH_MODE_SPREADSHEET-'], "a") as w:
                w.write(f"{variables_dict['-BOX_BARCODE-']},{variables_dict['-LOCATION_BARCODE-']}\n")
            w.close()
            window['-OUTPUT-'].update(f"Appended '{variables_dict['-BOX_BARCODE-']},{variables_dict['-LOCATION_BARCODE-']}' to spreadsheet\n", append=True)
            window['-BOX_BARCODE-'].update("")
            window['-LOCATION_BARCODE-'].update("")
    if event == "Upload batch update":
        with open(variables_dict['-BATCH_MODE_SPREADSHEET-'], "r") as r:
            for line in r:
                line = line[:-1]
                line = line.split(",")
                variables_dict['-BOX_BARCODE-'] = line[0]
                variables_dict['-LOCATION_BARCODE-'] = line[1]
                spreadsheet_dict = spreadsheet_converter(variables_dict['-SPREADSHEET-'])
                headers = main_scan(variables_dict, spreadsheet_dict)
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()

#TODO Add panel for adding information to the system
#TODO add a barcode to a container
#TODO add a barcode to a location