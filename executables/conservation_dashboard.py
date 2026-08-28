import PySimpleGUI as SG
from PIL import Image, ImageTk
import pandas as pd
import configparser
import os
import io
import datetime
from pdfme import build_pdf
from pdfme import color


my_icon64 = b'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'

SG.theme("Purple")

supported_images = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')

filename = ""

report_captions_dict = {}
treatment_plan_dict = {}
treatment_plan_list = []

def report_creator(dictionary_of_dictionaries, pdf_name):
    first_page_dict = {}
    first_page_dict['Unique identifier:'] = values['-official_consID-']
    first_page_dict['Requested by:'] = values['-requestor-']
    first_page_dict['Date examined:'] = values['-examined_date-']
    first_page_dict['Examined by:'] = values['-examined_by-']
    first_page_dict['Date created:'] = values['-created_year-']
    first_page_dict['Creator:'] = values['-creator-']
    first_page_dict['Dimensions:'] = df.loc[int(values['index_key']), 'Dimensions (cm)']
    first_page_dict['Extent:'] = values['-extent-']

    images_dict = dictionary_of_dictionaries['images_dict']


    with open(pdf_name, "wb") as pdf_file:
        build_pdf(document, pdf_file)
    pdf_file.close()


def report_captioner(image_dict, filepath):
    my_text = '''<div class="images_section">
        <h2 class="images_title">Report Images</h2>
        '''
    image_text = ""
    image_counter = 0

    for key in image_dict.keys():
        filename = os.path.join(filepath, key)
        file_caption = image_dict[key]
        image_counter += 1
        image_text += f'<div class="single_image"><h3>Image {str(image_counter)}</h3><br/><img src="{filename}" title="{file_caption}" style="max-width: 450px"><br/><p>{file_caption}</p></div>'
    my_text = f"{my_text}{image_text}</div>"
    print(my_text)
    return my_text

def report_first_images(filepath):
    recto = ""
    verso = ""
    finished_text = ""
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            filename_root = filename.split(".")[0]
            if filename_root == "recto" or filename_root == "Recto":
                recto = os.path.join(dirpath, filename)
            if filename_root == "verso" or filename_root == "Verso":
                verso = os.path.join(dirpath, filename)
    if recto != "":
        recto = f'''<div class="top_images">
                        <h2>Recto</h2>
                        <img src="{recto}" title="Front of item"/>
                </div>'''
    if verso != "":
        verso = f'''<div class="top_images">
                        <h2>Verso</h2>
                        <img src="{verso}" title="Back of item"/>
                </div>'''
    if recto != "" or verso != "":
        finished_text = f'''<div class="top_image_section">
                                {recto}
                                {verso}
                        </div>'''
    return finished_text

def treatment_text_parser(treatment_block):
    treatment_plan_dict = {}
    if "|" in treatment_block:
        treatment_block_chunks = treatment_block.split("||")
        for treatment_block in treatment_block_chunks:
            treatment_list = treatment_block.split("|")
            if len(treatment_list) < 2:
                treatment_plan_dict[treatment_list[0]] = ["name", "date", "text", "#"]
            else:
                treatment_plan_dict[treatment_list[0]] = [treatment_list[1],
                                                      treatment_list[2],
                                                      treatment_list[3],
                                                      treatment_list[4]]
    return treatment_plan_dict

def total_hours(treatment_plan_dict):
    current_value = 0
    for key in treatment_plan_dict.keys():
        try:
            new_value = float(treatment_plan_dict[key][-1])
            current_value += new_value
        except:
            SG.popup_error(f"Error in treatment plan: {key}\nActual time: {treatment_plan_dict[key][-1]} not in number-compatible format")
    return str(current_value)

def convert_image(filename, maxsize=(400, 400), first=False):
    img = Image.open(filename)
    img.thumbnail(maxsize)
    if first:
        to_bytes = io.BytesIO()
        img.save(to_bytes, format='PNG')
        del img
        return to_bytes.getvalue()
    return ImageTk.PhotoImage(img)

layout_homes = [
    [
        SG.Push(),
        SG.Text("Conservation spreadsheet"),
        SG.In(default_text="filepath and filename for conservation spreadsheet", key = "-spreadsheet-"),
        SG.FileBrowse(file_types=(("excel spreadsheet", "*.xlsx"),))
    ],
    [
        SG.Push(),
        SG.Text("Configuration file"),
        SG.In(default_text="config file filepath and name", key="-config-"),
        SG.FileBrowse(file_types=[("cfg file extension", "*.cfg"), ("text file extension", "*.txt")])
    ],
    [
        SG.Push(),
        SG.Button("Load Spreadsheet and Config file", key="-load_spreadsheet-"),
        SG.Push()
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Push(),
        SG.Text("Create new entry", text_color="darkblue", font=("Arial", 16, "bold")),
        SG.Push()
    ],
    [
        SG.Text("Title: ", size=(25,1)),
        SG.Input(default_text="Enter title", key="-new_title-"),
        SG.Push(),
        SG.Button("Create new entry", key="-create_new_entry-"),
    ],
    [
        SG.Text("Initial status: ", size=(25,1)),
        SG.Combo(values=['some status'], key="-initial_status-")
    ],
    [
        SG.Text("Fiscal Year: ", size=(25,1)),
        SG.Input(default_text="Enter fiscal year", key="-fiscal_year-"),
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Push(),
        SG.Text("Filter data by...", text_color="darkblue", font=("Arial", 16, "bold")),
        SG.Push()
    ],
    [
        SG.Text("Status: "),
        SG.Combo(values=['some status'], key="-status_filter-"),
        SG.Text("Conservation ID: "),
        SG.Input(default_text="Enter conservation ID", key="-consID-"),
        SG.Text("Priority: "),
        SG.Combo(values=['some priority'], key="-priority_filter-"),
    ],
    [
        SG.Push(),
        SG.Button("Filter data", key="-filter-"),
        SG.Push(),
        SG.Button("Reload spreadsheet data", key="-reload_spreadsheet-"),
        SG.Push()
    ],
    [
        SG.Text("Filtered data preview")
    ],
    [
        SG.Push(),
        SG.Table(
            values=([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]),
            headings=['Status', 'ConsID', 'Title', 'Unique ID', 'Creator', 'Year of Creation', 'Link to Catalog', 'Request by', 'Request Date'],
            justification='left',
            key="-table_filter-"
        ),
        SG.Push(),
    ],
    [
        SG.Text("Select record by filtered ID"),
        SG.Combo(values=[], key='-filtered_identifiers-'),
        SG.Push(),
        SG.Button("Load record", key="-load_record-"),
    ]
]

layout_reviews = [
    [
        SG.Push(),
        SG.Text("Item information"),
        SG.Push()
    ],
    [
        SG.Text("Title: "),
        SG.Input("Title goes here", key="-title-"),
    ],
    [
        SG.Text("Conservation identifier: "),
        SG.Text("Conservation identifier goes here", key="-consID2-")
    ],
    [
        SG.Text("Creator: "),
        SG.Input(default_text="Enter creator", key="-creator-"),
        SG.Push(),
        SG.Text("Year of Creation: "),
        SG.Input(default_text="Enter year of creation", key="-created_year-"),
    ],
    [
        SG.Text("Unique identifier: "),
        SG.Input(default_text="Non-conservation unique identifier", key="-unique_identifier-"),
        SG.Push(),
        SG.Text("Link to ArchivesSpace or catalog record"),
        SG.Input(default_text="Enter link", key="-Aspace-"),
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Push(),
        SG.Text("Request information"),
        SG.Push()
    ],
    [
        SG.Text("Requested by: "),
        SG.Input(default_text="Enter requester", key="-requestor-"),
        SG.Push(),
        SG.Text("Request date: "),
        SG.Input(default_text="Enter date", key="-request_date-"),
    ],
    [
        SG.Text("Department: "),
        SG.Combo(values=['Department'], key="-request_dept-"),
    ],
    [
        SG.Text("Request reason: "),
        SG.Multiline(default_text="Enter reason", key="-request_reason-", size=(50,3)),
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Push(),
        SG.Text("Review"),
        SG.Push()
    ],
    [
        SG.Text("Reviewed by:"),
        SG.Combo(values=['Review'], key="-reviewed_by-"),
        SG.Push(),
        SG.Text("Review date:"),
        SG.Input(default_text="Enter yyyy-mm-dd", key="-reviewed_date-"),
    ],
    [
        SG.Text("Reviewer notes: "),
    ],
    [
        SG.Multiline(default_text="Review notes", key="-reviewed_notes-", size=(100,10)),
    ]

]

layout_exams = [
    [
        SG.Text("Examined by: "),
        SG.Input(default_text="Enter examined by", key="-examined_by-"),
        SG.Push(),
        SG.Text("Examination date: "),
        SG.Input(default_text="yyyy-mm-dd", size=(12, 1), key="-examined_date-"),
    ],
    [
        SG.Text("Priority level: "),
        SG.Combo(values=['Priority level'], key="-current_priority-"),
        SG.Push(),
        SG.Text("Current Status: "),
        SG.Combo(values=['current status'], key="-current_status-"),
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Push(),
        SG.Text("Description"),
        SG.Push()
    ],
    [
        SG.Text("Dimensions: "),
        SG.Text("Height"),
        SG.Input("", size=(6, 1), key="-dimensions_h-"),
        SG.Text("cm"),
        SG.Push(),
        SG.Text("Width"),
        SG.Input("", size=(6, 1), key="-dimensions_w-"),
        SG.Text("cm"),
        SG.Push(),
        SG.Text("Depth"),
        SG.Input("", size=(6, 1), key="-dimensions_d-"),
        SG.Text("cm")
    ],
    [
        SG.Text("Extent: "),
        SG.Input(default_text="Enter extent", key="-extent-"),
        SG.Push(),
        SG.Text("Number of items: "),
        SG.Input(default_text="", size=(6, 1), key="-number_of_items-"),
    ],
    [
        SG.Text("format: "),
        SG.Combo(values=['format type goes here'], key="-format-"),
        SG.Push(),
        SG.Text("Substrate: "),
        SG.Combo(values=['Substrate'], key="-substrate-"),
        SG.Push(),
        SG.Text("Media type: "),
        SG.Combo(values=['Media type'], key='-media_type-'),
    ],
    [
        SG.Text("Provenance: "),
        SG.Push(),
        SG.Multiline(default_text="output message goes here", key="-provenance-", size=(100,5))
    ],
    [
        SG.Text("Description/Condition Notes: "),
        SG.Push(),
        SG.Multiline(default_text="Enter notes", key="-item_notes-", size=(100, 5)),
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Push(),
        SG.Text("Condition"),
        SG.Push()
    ],
    [
        SG.Combo(values=[], key="-condition_list-", size=(40, 5)),
        SG.Push(),
        SG.Button("Add Condition to List"),
        SG.Push(),
        SG.Multiline(size=(40,5), key="-applicable_conditions-"),
        SG.Input("", key="-condition_plan_list-", readonly=True, disabled_readonly_background_color="PeachPuff2")
    ],
    [
        SG.Push(),
        SG.Text("Treatment plan"),
        SG.Push()
    ],
    [
        SG.Combo(values=[], key="-exam_treatment_plan_drop-", size=(40, 5)),
        SG.Push(),
        SG.Button("Add Treatment to List"),
        SG.Push(),
        SG.Multiline(key="-treatment_plan-", size=(40,5)),
        SG.Input("", key="-treatment_plan_list-", readonly=True, disabled_readonly_background_color="PeachPuff2"),
    ],
    [
        SG.Text("Estimated treatment hours: "),
        SG.Input("", size=(6, 1), key="-estimated_treatment_hours-"),
        SG.Text("hrs"),
        SG.Push()
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Text("Testing results:"),
        SG.Push(),
        SG.Multiline(key="-testing_results-", size=(100,5)),
    ],
]

layout_treatments = [
    [
        SG.Push(),
        SG.Text("Treatment plan"),
        SG.Push(),
    ],
    [
        SG.Text("Treatment: "),
        SG.Combo(values=[], key="-treatment_drop-", size=(40, 5), enable_events=True),
        SG.Push(),
        SG.Text("Treated by: "),
        SG.Combo(values=[], key="-treated_by-"),
        SG.Push(),
        SG.Text("Date: "),
        SG.Input(default_text="Enter date as YYYY-MM-DD", key="-treatment_date-"),
    ],
    [
        SG.Text("Notes: "),
        SG.Push()
    ],
    [
        SG.Multiline(key="-treatment_notes-", size=(100,10)),
        SG.Push(),
        SG.Button("Update Treatment Notes"),
    ],
    [
        SG.Text("Actual time: "),
        SG.Input("", key="-actual_time-"),
        SG.Text("hrs")
    ],
    [
        SG.Input("", key="-treatment_text_block-", disabled_readonly_background_color="PeachPuff2", readonly=True),
    ],
    # treatment type separated by ||, intraitem separated by |. [0] = treatment type [1] = notes, [2] = treated by [3] = date [4] = hours to complete
    [
        SG.Push(),
        SG.Text("DON'T FORGET TO TAKE PHOTOS!", font=("Courier", 14, "bold"), text_color="darkred"),
        SG.Push()
    ]
]

layout_reports = [
    [
        SG.Text("Treated by: "),
        SG.Input(default_text="Enter treated by", key="-treated_by2-"),
        SG.Push(),
        SG.Text("Total actual time: "),
        SG.Input(default_text="Enter total actual time", key="-total_actual_time-"),
    ],
    [
        SG.Push(),
        SG.Text("Conservation Summary: "),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="enter summary narrative of conservation actions", key="-summary-", size=(100,5)),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Button("Create Report"),
        SG.Push()
    ],
    [
        SG.HorizontalSeparator(),
    ],
    [
        SG.Push(),
        SG.Text("Image captions: "),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Input("Folder path to images", key="-report_images_folder-"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Button("Load report images"),
        SG.Push()
    ],
    [
        SG.Listbox(values=[], change_submits=True, size=(40, 25), key="-report_images-"),
        SG.VerticalSeparator(),
        SG.Push(),
        SG.Image(key="-current_report_image-"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Image filename:"),
        SG.Text("No image loaded", key="-image_filename_report-"),
        SG.Push(),
        SG.Button("Add image to report"),
    ],
    [
        SG.Combo(values=[], key="-report_images2-", enable_events=True, size=(60,5)),
        SG.Push(),
        SG.Text("Image caption:"),
        SG.Input(key="-image_caption-"),
        SG.Button("Add or Update Caption")
    ],
]

layout_images = [
    [
        SG.Push(),
        SG.Text("path to images folder"),
        SG.Input(default_text="Enter path to images folder", key="-treatment_images-"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Button("Load image list"),
        SG.Push()
    ],
    [
        SG.Listbox(values=[], change_submits=True, size=(40, 25), key="-image_list-"),
        SG.VerticalSeparator(),
        SG.Image(key="-current_image-")
    ],
    [
        SG.Push(),
        SG.Text("Image filename:"),
        SG.Text("No image loaded", key="-image_filename-"),
        SG.Push()
    ]
]

layout = [
    [
        SG.Push(),
        SG.Text("Conservation ID: status", text_color="darkblue", font=("Arial", 16, "bold"), key="-header_info-"),
        SG.Push(),
        SG.Button("Save changes", key="-save-")
    ],
    [
        SG.Text("title", text_color="darkblue", font=("Arial", 14, "bold"), key="-title_info-"),
        SG.Push(),
        SG.Input("Data index", key="index_key", readonly=True, disabled_readonly_background_color="PeachPuff2", size=(9, 1)),
        SG.Input("", key="-official_consID-", readonly=True, disabled_readonly_background_color="PeachPuff2", visible=False),
    ],
    [
        SG.Push(),
        SG.TabGroup([
            [
                SG.Tab("Home", layout_homes, font=("Ariel", 14, "bold")),
                SG.Tab("Review", layout_reviews),
                SG.Tab("Examination", layout_exams),
                SG.Tab("Treatment", layout_treatments),
                SG.Tab("Images", layout_images),
                SG.Tab("Report", layout_reports),
            ]
        ], key="-tab_group-", expand_x=True, expand_y=True),
        SG.Push()
    ],
    [
        SG.Button('Close'),
        SG.Push(),
        SG.Button("Generate New Conservation Workbook")
    ]
]

window = SG.Window(title="Conservation management GUI",
                   layout=layout,
                   icon=my_icon64)

event, values = window.read()
while True:
    event, values = window.read()
    #set to variables
    Status = ""
    ConsID = ""
    Title = ""
    Unique_ID = ""
    Creator = ""
    Year_of_Creation = ""
    Link_to_Catalog = ""
    Request_By = ""
    Request_Date = ""
    Request_Reason = ""
    Department = ""
    Reviewed_By = ""
    Review_Date = ""
    Review_Notes = ""
    Exam_By = ""
    Exam_Date = ""
    Priority = ""
    Dimensions = ""
    Item_Format = ""
    Item_Substrate = ""
    Item_Media = ""
    History = ""
    Notes = ""
    Condition_Issues = ""
    Treatment_Plan = ""
    Number_of_Items = ""
    Estimated_Time = ""
    Treatment = ""
    Treatment_Notes = ""
    Actual_Time = ""
    Treated_By = ""
    Total_Actual_Time = ""
    Date_Completed = ""
    # now continue
    if event == '-load_spreadsheet-':
        proceed_flag = True
        print("something")
        if os.path.isfile(values['-spreadsheet-']):
            print("spreadsheet exists")
        else:
            SG.popup_error("spreadsheet does not exist, try again")
            proceed_flag = False
        if os.path.isfile(values['-config-']):
            print("config file exists")
        else:
            SG.popup_error("config file does not exist, try again")
            proceed_flag = False
        if proceed_flag is True:
            print("proceeding")
            my_config = configparser.RawConfigParser()
            my_config.optionxform = lambda option: option
            my_config.read(values['-config-'])
            print(my_config['statusDD'])
            status_list = []
            for item in my_config['statusDD'].items():
                status_list.append(item[0])
            status_list.sort()
            window['-status_filter-'].update(values=status_list)
            window['-initial_status-'].update(values=status_list)
            window['-current_status-'].update(values=status_list)
            print("loaded status list")
            priority_list = []
            for item in my_config['highPriorityDD'].items():
                priority_list.append(item[0])
            priority_list.sort()
            window['-priority_filter-'].update(values=priority_list)
            window['-current_priority-'].update(values=priority_list)
            requestor_list = []
            for item in my_config['departmentDD'].items():
                requestor_list.append(item[0])
            requestor_list.sort()
            window['-request_dept-'].update(values=requestor_list)
            format_list = []
            for item in my_config['descriptionDD_format'].items():
                format_list.append(item[0])
            format_list.sort()
            window['-format-'].update(values=format_list)
            substrate_list =[]
            for item in my_config['descriptionDD_substrate'].items():
                substrate_list.append(item[0])
            substrate_list.sort()
            window['-substrate-'].update(values=substrate_list)
            media_type_list = []
            for item in my_config['descriptionDD_media'].items():
                media_type_list.append(item[0])
            media_type_list.sort()
            window['-media_type-'].update(values=media_type_list)
            exam_treatment_drop_list = []
            for item in my_config['treatmentDD'].items():
                exam_treatment_drop_list.append(item[0])
            exam_treatment_drop_list.sort()
            window['-exam_treatment_plan_drop-'].update(values=exam_treatment_drop_list, size=(40,5))
            condition_list = []
            for item in my_config['conditionDD'].items():
                condition_list.append(item[0])
            condition_list.sort()
            window['-condition_list-'].update(values=condition_list, size=(40,5))
            treated_by_list = []
            for item in my_config['treatmentStaff'].items():
                treated_by_list.append(item[0])
            treated_by_list.sort()
            window['-reviewed_by-'].update(values=treated_by_list)
            window['-treated_by-'].update(values=treated_by_list)
            df = pd.read_excel(values['-spreadsheet-'], dtype=object, sheet_name='Conservation Reports')
            print("loaded spreadsheet")
            df.fillna('', inplace=True)
            new_df = df
            window['-table_filter-'].update(values=new_df.values.tolist())
            window['-filtered_identifiers-'].update(values=new_df['ConsID'].tolist())
    if event == '-create_new_entry-':
        if values['-fiscal_year-'] != "" and values['-fiscal_year-'] != "Enter fiscal year":
            if len(values['-fiscal_year-']) == 4:
                newer_df = new_df['ConsID'].str.startswith(values['-fiscal_year-'])
                new_df = new_df[newer_df]
                if len(new_df) > 0:
                    id_list = new_df['ConsID'].tolist()
                    id_list.sort()
                    largest_id = id_list[-1]
                    largest_id = str(int(largest_id.split("_")[-1]) + 1)
                    while len(largest_id) < 3:
                        largest_id = f"0{largest_id}"
                    ConsID = f"{values['-fiscal_year-']}_{largest_id}"
                else:
                    ConsID = f"{values['-fiscal_year-']}_001"
                print(ConsID)
                Status = values['-initial_status-']
                Title = values['-new_title-']
                small_df = pd.DataFrame([[Status, ConsID, Title]], columns=['Status', 'ConsID', 'Title'])
                df = pd.concat([df, small_df], ignore_index=True)
                new_df = df
                window['-official_consID-'].update(ConsID)
                window['-table_filter-'].update(values=new_df.values.tolist())
                window['-header_info-'].update(f"{ConsID}: {Status}")
                title_for_window = Title
                if len(Title) > 50:
                    title_for_window = f"{Title[:47]}..."
                window['-title_info-'].update(f"{title_for_window}")
                An_Index = df.loc[df['ConsID'] == ConsID].index.tolist()[0]
                window['index_key'].update(f"{An_Index}")
    if event == "-filter-":
        if values['-status_filter-'] != "":
            newer_df = new_df[new_df['Status'] == values['-status_filter-']]
            new_df = newer_df
        if values['-consID-'] != "" and values['-consID-'] != "Enter conservation ID":
            newer_df = new_df['ConsID'].str.startswith(values['-consID-'])
            new_df = new_df[newer_df]
        if values['-priority_filter-'] != "":
            newer_df = new_df[new_df['High Priority?'] == values['-priority_filter-']]
            new_df = newer_df
        window['-table_filter-'].update(values=new_df.values.tolist())
        window['-filtered_identifiers-'].update(values=new_df['ConsID'].tolist())
    if event == '-reload_spreadsheet-':
        df = pd.read_excel(values['-spreadsheet-'], dtype=object, sheet_name='Conservation Reports')
        df.fillna('', inplace=True)
        new_df = df
        window['-table_filter-'].update(values=new_df.values.tolist())
        window['-filtered_identifiers-'].update(values=new_df['ConsID'].tolist())
    if event == '-load_record-':
        if values['-filtered_identifiers-'] != "":
            ConsID = values['-filtered_identifiers-']
            Status = new_df.loc[new_df['ConsID'] == ConsID, 'Status'].values[0]
            Title = new_df.loc[new_df['ConsID'] == ConsID, 'Title'].values[0]
            Unique_ID = new_df.loc[new_df['ConsID'] == ConsID, 'Unique ID'].values[0]
            Creator = new_df.loc[new_df['ConsID'] == ConsID, 'Creator'].values[0]
            Year_of_Creation = new_df.loc[new_df['ConsID'] == ConsID, 'Year of Creation'].values[0]
            Link_to_Catalog = new_df.loc[new_df['ConsID'] == ConsID, 'Link to Catalog'].values[0]
            Request_By = new_df.loc[new_df['ConsID'] == ConsID, 'Requested by'].values[0]
            Request_Date = new_df.loc[new_df['ConsID'] == ConsID, 'Request Date'].values[0]
            if isinstance(Request_Date, datetime.datetime):
                Request_Date = Request_Date.strftime('%Y-%m-%d')
            Request_Reason = new_df.loc[new_df['ConsID'] == ConsID, 'Request Reason'].values[0]
            Department = new_df.loc[new_df['ConsID'] == ConsID, 'Department'].values[0]
            Reviewed_By = new_df.loc[new_df['ConsID'] == ConsID, 'Rev. by'].values[0]
            Review_Date = new_df.loc[new_df['ConsID'] == ConsID, 'Review Date'].values[0]
            if isinstance(Review_Date, datetime.datetime):
                Review_Date = Review_Date.strftime('%Y-%m-%d')
            Review_Notes = new_df.loc[new_df['ConsID'] == ConsID, 'Review Notes'].values[0]
            Exam_By = new_df.loc[new_df['ConsID'] == ConsID, 'Exam By'].values[0]
            Exam_Date = new_df.loc[new_df['ConsID'] == ConsID, 'Exam Date'].values[0]
            if isinstance(Exam_Date, datetime.datetime):
                Exam_Date = Exam_Date.strftime('%Y-%m-%d')
            Priority = new_df.loc[new_df['ConsID'] == ConsID, 'High Priority?'].values[0]
            Dimensions = new_df.loc[new_df['ConsID'] == ConsID, 'Dimensions (cm)'].values[0]
            Extent = new_df.loc[new_df['ConsID'] == ConsID, 'Extent'].values[0]
            Item_Format = new_df.loc[new_df['ConsID'] == ConsID, 'Format'].values[0]
            Item_Substrate = new_df.loc[new_df['ConsID'] == ConsID, 'Substrate'].values[0]
            Item_Media = new_df.loc[new_df['ConsID'] == ConsID, 'Media'].values[0]
            History = new_df.loc[new_df['ConsID'] == ConsID, 'History'].values[0]
            Notes = new_df.loc[new_df['ConsID'] == ConsID, 'Notes'].values[0]
            Condition_Issues = new_df.loc[new_df['ConsID'] == ConsID, 'Condition Issues'].values[0]
            window['-condition_plan_list-'].update(Condition_Issues)
            Testing_Results = new_df.loc[new_df['ConsID'] == ConsID, "Testing Results"].values[0]
            window['-testing_results-'].update(Testing_Results)
            Treatment_Plan = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment Plan'].values[0]
            window['-treatment_plan_list-'].update(Treatment_Plan)
            Number_of_Items = new_df.loc[new_df['ConsID'] == ConsID, 'Number of Items'].values[0]
            Estimated_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Est. Time (hrs)'].values[0]
            Treatment = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment'].values[0]
            Treatment_Notes = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment Notes'].values[0]
            Actual_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Actual Time'].values[0]
            Treated_By = new_df.loc[new_df['ConsID'] == ConsID, 'Treated by'].values[0]
            Total_Actual_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Total Actual Time'].values[0]
            Date_Completed = new_df.loc[new_df['ConsID'] == ConsID, 'Date Completed'].values[0]
            if isinstance(Date_Completed, datetime.datetime):
                Date_Completed = Date_Completed.strftime('%Y-%m-%d')
            Treatment_Images = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment Images'].values[0]
            print("values loaded")
            window['-header_info-'].update(f"{ConsID}: {Status}")
            title_for_window = Title
            if len(Title) > 50:
                title_for_window = f"{Title[:47]}..."
            window['-title_info-'].update(f"{title_for_window}")
            An_Index = df.loc[df['ConsID'] == ConsID].index.tolist()[0]
            window['index_key'].update(f"{An_Index}")
            window['-title-'].update(Title)
            window['-consID2-'].update(ConsID)
            window['-official_consID-'].update(ConsID)
            window['-creator-'].update(Creator)
            window['-unique_identifier-'].update(Unique_ID)
            window['-Aspace-'].update(Link_to_Catalog)
            window['-created_year-'].update(Year_of_Creation)
            window['-requestor-'].update(Request_By)
            window['-request_date-'].update(Request_Date)
            window['-request_dept-'].update(value=Department)
            window['-request_reason-'].update(Request_Reason)
            window['-reviewed_by-'].update(value=Reviewed_By)
            window['-reviewed_date-'].update(Review_Date)
            window['-reviewed_notes-'].update(Review_Notes)
            window['-examined_by-'].update(Exam_By)
            window['-examined_date-'].update(Exam_Date)
            window['-current_priority-'].update(value=Priority)
            window['-current_status-'].update(value=Status)
            Dimensions_list = Dimensions.split("x")
            if len(Dimensions_list) > 0:
                for item in Dimensions_list:
                    if item.endswith("h"):
                        window['-dimensions_h-'].update(item[:-1])
                    if item.endswith("w"):
                        window['-dimensions_w-'].update(item[:-1])
                    if item.endswith("d"):
                        window['-dimensions_d-'].update(item[:-1])
            window['-number_of_items-'].update(Number_of_Items)
            window['-extent-'].update(Extent)
            window['-format-'].update(value=Item_Format)
            window['-substrate-'].update(value=Item_Substrate)
            window['-media_type-'].update(value=Item_Media)
            window['-provenance-'].update(History)
            window['-item_notes-'].update(Notes)
            if len(Condition_Issues) > 0:
                for item in Condition_Issues:
                    window['-applicable_conditions-'].update(f"{item}\n", append=True)

            window['-estimated_treatment_hours-'].update(Estimated_Time)
            print(Treatment)
            Treatment_Plan_list = Treatment_Plan.split("|")
            window['-treatment_drop-'].update(values=Treatment_Plan_list)
            window['-treatment_drop-'].update(value=Treatment_Plan_list[0], size=(40,5))
            window['-treatment_plan-'].update("")
            if len(Treatment_Plan_list) > 0:
                for item in Treatment_Plan_list:
                    if item == "":
                        Treatment_Plan_list.remove(item)
                    else:
                        window['-treatment_plan-'].update(f"{item}\n", append=True)
                window['-treatment_plan-'].update("\n", append=True)
            if len(Treatment_Notes) > 0:
                treatment_plan_dict = treatment_text_parser(Treatment_Notes)
                my_key = list(treatment_plan_dict.keys())[0]
                window['-treated_by-'].update(value=treatment_plan_dict[my_key][0])
                window['-treatment_date-'].update(value=treatment_plan_dict[my_key][1][:10])
                window['-treatment_notes-'].update(value=treatment_plan_dict[my_key][2])
                window['-actual_time-'].update(value=treatment_plan_dict[my_key][3])
            else:
                window['-treated_by-'].update(value=Treated_By)
                window['-treatment_date-'].update(Date_Completed[:10])
                window['-actual_time-'].update(Total_Actual_Time)
            window['-treatment_text_block-'].update(Treatment_Notes)
            window['-treatment_images-'].update(Treatment_Images)
            window['-report_images_folder-'].update(Treatment_Images)
    if event == "-save-":
        print(An_Index)
        if values['index_key'] == "":
            print("load or create a record before trying to save")
        else:
            window['-total_actual_time-'].update(total_hours(treatment_plan_dict))
            print("saving data")
            dimensions_text = ""
            if values['-dimensions_h-'] != "":
                dimensions_text = f"{dimensions_text}{values['-dimensions_h-']}Hx"
            if values['-dimensions_w-'] != "":
                dimensions_text = f"{dimensions_text}{values['-dimensions_w-']}Wx"
            if values['-dimensions_d-'] != "":
                dimensions_text = f"{dimensions_text}{values['-dimensions_d-']}Dx"
            while dimensions_text.endswith("x"):
                dimensions_text = dimensions_text[:-1]
            quick_math = 0
            treatment_plan_dict = treatment_text_parser(values['-treatment_text_block-'])
            for key in treatment_plan_dict.keys():
                my_float = float(treatment_plan_dict[key][3])
                quick_math += my_float
            df.loc[int(values['index_key']), "Status"] = str(values['-current_status-'])
            df.loc[int(values['index_key']), "ConsID"] = values['-official_consID-']
            df.loc[int(values['index_key']), "Title"] = values['-title-']
            df.loc[int(values['index_key']), "Unique ID"] = values['-unique_identifier-']
            df.loc[int(values['index_key']), "Creator"] = values['-creator-']
            df.loc[int(values['index_key']), "Year of Creation"] = values['-created_year-'][:4]
            df.loc[int(values['index_key']), "Link to Catalog"] = values['-Aspace-']
            df.loc[int(values['index_key']), "Requested by"] = values['-requestor-']
            df.loc[int(values['index_key']), "Request Date"] = values['-request_date-'][:10]
            df.loc[int(values['index_key']), "Request Reason"] = values['-request_reason-']
            df.loc[int(values['index_key']), "Department"] = values['-request_dept-']
            df.loc[int(values['index_key']), "Rev. By"] = values['-reviewed_by-']
            df.loc[int(values['index_key']), "Review Date"] = values['-reviewed_date-'][:10]
            df.loc[int(values['index_key']), "Review Notes"] = values['-reviewed_notes-']
            df.loc[int(values['index_key']), "Exam By"] = values['-examined_by-']
            df.loc[int(values['index_key']), "Exam Date"] = values['-examined_date-'][:10]
            df.loc[int(values['index_key']), "High Priority?"] = values['-current_priority-']
            df.loc[int(values['index_key']), "Dimensions (cm)"] = dimensions_text
            df.loc[int(values['index_key']), "Extent"] = values['-extent-']
            df.loc[int(values['index_key']), "Format"] = values['-format-']
            df.loc[int(values['index_key']), "Substrate"] = values['-substrate-']
            df.loc[int(values['index_key']), "Media"] = values['-media_type-']
            df.loc[int(values['index_key']), "History"] = values['-provenance-']
            df.loc[int(values['index_key']), "Notes"] = values['-item_notes-']
            df.loc[int(values['index_key']), "Condition Issues"] = values['-condition_plan_list-']
            df.loc[int(values['index_key']), "Treatment Plan"] = values['-treatment_plan_list-']
            df.loc[int(values['index_key']), "Number of Items"] = values['-number_of_items-']
            df.loc[int(values['index_key']), "Est. Time (hrs)"] = values['-estimated_treatment_hours-']
            df.loc[int(values['index_key']), "Testing Results"] = values['-testing_results-']
            df.loc[int(values['index_key']), "Treatment"] = values['-treatment_plan_list-']
            df.loc[int(values['index_key']), "Treatment Notes"] = values['-treatment_text_block-']
            df.loc[int(values['index_key']), "Actual Time"] = str(quick_math)
            df.loc[int(values['index_key']), "Treated by"] = values['-treated_by-']
            df.loc[int(values['index_key']), "Total Actual Time"] = total_hours(treatment_plan_dict)
            df.loc[int(values['index_key']), "Date Completed"] = values['-treatment_date-'][:10]
            df.loc[int(values['index_key']), "Treatment Images"] = values['-treatment_images-']
            writer = df.to_excel(values['-spreadsheet-'], sheet_name="Conservation Reports", index=False)
            print("data saved")
    if event == "Load image list":
        files_list = os.listdir(values['-treatment_images-'])
        image_list = [f for f in files_list if os.path.isfile(os.path.join(values['-treatment_images-'], f)) and f.lower().endswith(supported_images)]
        if len(image_list) == 0:
            SG.popup_error("No images found")
        else:
            window['-image_list-'].update(values=image_list)
    if event == "-image_list-":
        filename = os.path.join(values['-treatment_images-'], values['-image_list-'][0])
        window['-current_image-'].update(data=convert_image(filename, first=True))
        window['-image_filename-'].update(filename.split("\\")[-1])
    if event == "Load report images":
        report_files_list = os.listdir(values['-report_images_folder-'])
        report_images = [f for f in report_files_list if os.path.isfile(os.path.join(values['-report_images_folder-'], f)) and f.lower().endswith(supported_images)]
        if len(report_images) == 0:
            SG.popup_error("No images found")
        else:
            window['-report_images-'].update(values=report_images)
    if event == "-report_images-":
        filename2 = os.path.join(values['-report_images_folder-'], values['-report_images-'][0])
        window['-current_report_image-'].update(data=convert_image(filename2, first=True))
        window['-image_filename_report-'].update(filename2.split("\\")[-1])
    if event == "Add image to report":
        if not values['-report_images-'][0] in report_captions_dict.keys():
            report_captions_dict[values['-report_images-'][0]] = ""
        report_image_list = list(report_captions_dict.keys())
        window['-report_images2-'].update(values=report_image_list, size=(60,5))
    if event == "Add or Update Caption":
        report_captions_dict[values['-report_images2-']] = values['-image_caption-']
        print(report_captions_dict)
    if event == "-report_images2-":
        window['-image_caption-'].update(report_captions_dict[values['-report_images2-']])
    if event == "Add Condition to List":
        Condition_Issues = values['-condition_plan_list-'].split("|")
        if not values['-condition_list-'] in Condition_Issues:
            Condition_Issues.append(values['-condition_list-'])
        print(Condition_Issues)
        window['-applicable_conditions-'].update(f"{values['-condition_list-']}\n", append=True)
        window['-condition_plan_list-'].update(f"{values['-condition_plan_list-']}{values['-condition_list-']}|")
        for item in Condition_Issues:
            if item in condition_list:
                condition_list.remove(item)
        window['-condition_list-'].update(values=condition_list, size=(40,5))
    if event == "Add Treatment to List":
        Treatment_Plan = list(set(values['-treatment_plan_list-'].split("|")))
        Treatment_Plan.sort()
        if not values['-exam_treatment_plan_drop-'] in Treatment_Plan:
            Treatment_Plan.append(values['-exam_treatment_plan_drop-'])
            window['-treatment_plan-'].update(f"{values['-exam_treatment_plan_drop-']}\n", append=True)
            window['-treatment_plan_list-'].update(f"{values['-treatment_plan_list-']}{values['-exam_treatment_plan_drop-']}|")
        for item in Treatment_Plan:
            if item in exam_treatment_drop_list:
                exam_treatment_drop_list.remove(item)
        window['-exam_treatment_plan_drop-'].update(values=exam_treatment_drop_list, size=(40,5))
        window['-treatment_drop-'].update(values=Treatment_Plan)
    if event == "Update Treatment Notes":
        treatment_plan_dict = treatment_text_parser(values['-treatment_text_block-'])
        treated_by = values['-treated_by-']
        if treated_by == "":
            treated_by = "Nobody"
        treatment_date = values['-treatment_date-']
        if treatment_date == "":
            treatment_date = "1835-09-01"
        treatment_notes = values['-treatment_notes-']
        if treatment_notes == "":
            treatment_notes = "No notes yet"
        actual_time = values['-actual_time-']
        if actual_time == "":
            actual_time = "0"
        new_list = [treated_by, treatment_date, treatment_notes, actual_time]
        print(new_list)
        treatment_plan_dict[values['-treatment_drop-']] = new_list
        temp_text = ""
        for key in treatment_plan_dict.keys():
            temp_text = f"{temp_text}{key}|{treatment_plan_dict[key][0]}|{treatment_plan_dict[key][1]}|{treatment_plan_dict[key][2]}|{treatment_plan_dict[key][3]}||"
        temp_text = temp_text[:-2]
        window['-treatment_text_block-'].update(temp_text)
        window['-total_actual_time-'].update(total_hours(treatment_plan_dict))
    if event == "-treatment_drop-":
        if values['-treatment_drop-'] in treatment_plan_dict.keys() and treatment_plan_dict[values['-treatment_drop-']] != []:
            window['-treated_by-'].update(value=treatment_plan_dict[values['-treatment_drop-']][0])
            window['-treatment_date-'].update(value=treatment_plan_dict[values['-treatment_drop-']][1])
            window['-treatment_notes-'].update(value=treatment_plan_dict[values['-treatment_drop-']][2])
            window['-actual_time-'].update(value=treatment_plan_dict[values['-treatment_drop-']][3])
        else:
            treatment_plan_dict[values['-treatment_drop-']] = ['placeholder','placeholder','placeholder','placeholder']
            window['-treated_by-'].update(value="Nobody")
            window['-treatment_date-'].update(value='1835-09-01')
            window['-treatment_notes-'].update(value='No text yet')
            window['-actual_time-'].update(value='0')
        print(treatment_plan_dict)
    if event == "Create Report":
        style = '''table, th, td{border: 2px solid black;border-collapse:collapse;padding-left:2px;padding-right:2px;}
                    .top_images>img{max-width:450px}
                    .top_image_section{display:inline-table;padding-left:25%;padding-right:25%;}
                    .top_images{display:table-cell;padding:10px}
                    .single_image{text-align:center;}
                    table{width:100%;}
                    .table-left{width: 30%}
                    .table-right{width: 70%}
                    '''
        top_images = report_first_images(values['-report_images_folder-'])
        my_images = report_captioner(report_captions_dict, values['-report_images_folder-'])
        uuid = ""
        if values['-unique_identifier-'] != "" or values['-unique_identifier_'] != "Non-conservation unique identifier":
            uuid = f"<tr><td>Other Unique Identifier</td><td>{values['-unique_identifier-']}</td></tr>"

        report = f'''<html>
            <head>
                <style type="text/css">
                    {style}
                </style>
            <h1 style="text-align: center">Conservation Report and Treatment Plan</h1>
            <h1 style="text-align: center">{values['-title-']}</h1>
            <p style="text-align: center">Texas State Library and Archives Commission</p>
            <p style="text-align: center">Archives and Information Services | Conservation</p>
            {top_images}
            <table>
                <tr>
                    <td class="table-left">Name of piece:</td>
                    <td class="table-right">{values['-title-']}</td>
                </tr>
                <tr>
                    <td>Unique identifier:</td>
                    <td>{values['-official_consID-']}</td>
                </tr>
                {uuid}
                <tr>
                    <td>ArchivesSpace Link:</td>
                    <td>{values['-Aspace-']}</td>
                </tr>
                <tr>
                    <td>Date inspected:</td>
                    <td>{values['-examined_date-']}</td>
                </tr>
                <tr>
                    <td>Inspected by:</td>
                    <td>{values['-examined_by-']}</td>
                </tr>
                <tr>
                    <td>Date created:</td>
                    <td>{values['-created_year-']}</td>
                </tr>
                <tr>
                    <td>Creator:</td>
                    <td>{values['-creator-']}</td>
                </tr>
                <tr>
                    <td>Dimensions:</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Description:</td>
                    <td>{values['-item_notes-']}</td>
                </tr>
                <tr>
                    <td>Condition concerns:</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Treatment plan:</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Estimated time for treatment:</td>
                    <td>{values['-estimated_treatment_hours-']}</td>
                </tr>
                <tr>
                    <td>Treatment undertaken:</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Actual total time:</td>
                    <td>{values['-total_actual_time-']}</td>
                </tr>
            </table>
            {my_images}
        </html>
        '''
        with open(f"{values['-official_consID-']}_report.html", 'w', encoding='utf-8') as f:
            f.write(report)
        f.close()
    if event == "Generate New Conservation Workbook":
        df_list = []
        for item in my_config['spreadsheet_columns'].items():
            df_list.append(item[0])
        df = pd.DataFrame(columns=df_list)
        writer = df.to_excel("New_ConservationReportingSS_WIP.xlsx", index=False, sheet_name="Conservation Reports")
        SG.popup("generated new conservation workbook")
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()