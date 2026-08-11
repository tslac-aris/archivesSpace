import PySimpleGUI as SG
from PIL import Image, ImageTk
import pandas as pd
import configparser
import os
import io

SG.theme("Purple")

supported_images = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')

filename = ""

report_captions_dict = {}
treatment_plan_dict = {}
treatment_plan_list = []

def treatment_text_parser(treatment_block):
    treatment_plan_dict = {}
    if "|" in treatment_block:
        treatment_block_chunks = treatment_block.split("||")
        for treatment_block in treatment_block_chunks:
            treatment_list = treatment_block.split("|")
            treatment_plan_dict[treatment_list[0]] = [treatment_list[1],
                                                      treatment_list[2],
                                                      treatment_list[3],
                                                      treatment_list[4]]
    return treatment_plan_dict

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
        SG.Input("", key="-condition_plan_list-")
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
        SG.Input("", key="-treatment_plan_list-"),
    ],
    [
        SG.Text("Estimated treatment hours: "),
        SG.Input("", size=(6, 1), key="-estimated_treatment_hours-"),
        SG.Text("hrs"),
        SG.Push()
    ]
]

layout_treatments = [
    [
        SG.Push(),
        SG.Text("Treatment plan"),
        SG.Push(),
    ],
    [
        SG.Text("treatment: "),
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
        SG.Input("", key="-treatment_text_block-")
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
        SG.Button('Close')
    ]
]

window = SG.Window(title="Conservation management GUI",
                   layout=layout)

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
            Request_Reason = new_df.loc[new_df['ConsID'] == ConsID, 'Request Reason'].values[0]
            Department = new_df.loc[new_df['ConsID'] == ConsID, 'Department'].values[0]
            Reviewed_By = new_df.loc[new_df['ConsID'] == ConsID, 'Rev. by'].values[0]
            Review_Date = new_df.loc[new_df['ConsID'] == ConsID, 'Review Date'].values[0]
            Review_Notes = new_df.loc[new_df['ConsID'] == ConsID, 'Review Notes'].values[0]
            Exam_By = new_df.loc[new_df['ConsID'] == ConsID, 'Exam By'].values[0]
            Exam_Date = new_df.loc[new_df['ConsID'] == ConsID, 'Exam Date'].values[0]
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
            Treatment_Plan = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment Plan'].values[0]
            window['-treatment_plan_list-'].update(Treatment_Plan + "|")
            Number_of_Items = new_df.loc[new_df['ConsID'] == ConsID, 'Number of Items'].values[0]
            Estimated_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Est. Time (hrs)'].values[0]
            Treatment = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment'].values[0]
            Treatment_Notes = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment Notes'].values[0]
            Actual_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Actual Time'].values[0]
            Treated_By = new_df.loc[new_df['ConsID'] == ConsID, 'Treated by'].values[0]
            Total_Actual_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Total Actual Time'].values[0]
            Date_Completed = new_df.loc[new_df['ConsID'] == ConsID, 'Date Completed'].values[0]
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
            window['-treatment_drop-'].update(value=Treatment, size=(40,5))
            if len(Treatment_Plan) > 0:
                for item in Treatment_Plan:
                    window['-treatment_plan-'].update(f"{item}", append=True)
                window['-treatment_plan-'].update("\n", append=True)
            window['-treated_by-'].update(value=Treated_By)
            window['-treatment_date-'].update(Date_Completed)
            window['-treatment_notes-'].update(Treatment_Notes)
            window['-actual_time-'].update(Total_Actual_Time)
            window['-treatment_images-'].update(Treatment_Images)
    if event == "-save-":
        print(An_Index)
        if values['index_key'] == "":
            print("load or create a record before trying to save")
        else:
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
            df.loc[int(values['index_key'])] = [
                str(values['-current_status-']),
                values['-official_consID-'],
                values['-title-'],
                values['-unique_identifier-'],
                values['-creator-'],
                values['-created_year-'],
                values['-Aspace-'],
                values['-requestor-'],
                values['-request_date-'],
                values['-request_reason-'],
                values['-request_dept-'],
                values['-reviewed_by-'],
                values['-reviewed_date-'],
                values['-reviewed_notes-'],
                values['-examined_by-'],
                values['-examined_date-'],
                values['-current_priority-'],
                dimensions_text,
                values['-extent-'],
                values['-format-'],
                values['-substrate-'],
                values['-media_type-'],
                values['-provenance-'],
                values['-item_notes-'],
                values['-condition_plan_list-'],
                values['-treatment_plan_list-'],
                values['-number_of_items-'],
                values['-estimated_treatment_hours-'],
                values['-treatment_plan_list-'],
                values['-treatment_text_block-'],
                str(quick_math),
                values['-treated_by-'],
                str(quick_math),
                values['-treatment_date-'],
                values['-treatment_images-']
            ]
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
        treatment_plan_dict[values['-treatment_drop-']] = [values['-treated_by-'], values['-treatment_date-'], values['-treatment_notes-'], values['-actual_time-']]
        temp_text = ""
        for key in treatment_plan_dict.keys():
            temp_text = f"{temp_text}{key}|{treatment_plan_dict[key][0]}|{treatment_plan_dict[key][1]}|{treatment_plan_dict[key][2]}|{treatment_plan_dict[key][3]}||"
        temp_text = temp_text[:-2]
        window['-treatment_text_block-'].update(temp_text)
    if event == "-treatment_drop-":
        if values['-treatment_drop-'] in treatment_plan_dict.keys() and treatment_plan_dict[values['-treatment_drop-']] != []:
            window['-treated_by-'].update(value=treatment_plan_dict[values['-treatment_drop-']][0])
            window['-treatment_date-'].update(value=treatment_plan_dict[values['-treatment_drop-']][1])
            window['-treatment_notes-'].update(value=treatment_plan_dict[values['-treatment_drop-']][2])
            window['-actual_time-'].update(value=treatment_plan_dict[values['-treatment_drop-']][3])
        else:
            treatment_plan_dict[values['-treatment_drop-']] = []
            window['-treatment_date-'].update(value='')
            window['-treatment_notes-'].update(value='')
            window['-actual_time-'].update(value='')
        print(treatment_plan_dict)
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()