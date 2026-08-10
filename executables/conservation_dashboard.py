import PySimpleGUI as SG
import PIL
import pandas as pd
import configparser
import os

SG.theme("Purple")


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
        SG.Text("Title goes here", key="-title-"),
    ],
    [
        SG.Text("Conservation identifier: "),
        SG.Text("Conservation identifier goes here")
    ],
    [
        SG.Text("Creator: "),
        SG.Input(default_text="Enter creator"),
        SG.Push(),
        SG.Text("Year of Creation: "),
        SG.Input(default_text="Enter year of creation"),
    ],
    [
        SG.Text("Link to ArchivesSpace or catalog record"),
        SG.Input(default_text="Enter link"),
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
        SG.Input(default_text="Enter requester"),
        SG.Push(),
        SG.Text("Request date: "),
        SG.Input(default_text="Enter date"),
    ],
    [
        SG.Text("Department: "),
        SG.Combo(values=['Department'], key="-requestor-"),
    ],
    [
        SG.Text("Request reason: "),
        SG.Input(default_text="Enter reason"),
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
        SG.Input(default_text="Enter yyyy-mm-dd"),
    ],
    [
        SG.Text("Reviewer notes: "),
    ],
    [
        SG.Multiline(default_text="Review notes"),
    ]

]

layout_exams = [
    [
        SG.Text("Examined by: "),
        SG.Input(default_text="Enter examined by"),
        SG.Push(),
        SG.Text("Examination date: "),
        SG.Input(default_text="yyyy-mm-dd", size=(12            , 1)),
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
        SG.Input("", size=(6, 1)),
        SG.Text("cm"),
        SG.Push(),
        SG.Text("Width"),
        SG.Input("", size=(6, 1)),
        SG.Text("cm"),
        SG.Push(),
        SG.Text("Depth"),
        SG.Input("", size=(6, 1)),
        SG.Text("cm")
    ],
    [
        SG.Text("Extent: "),
        SG.Input(default_text="Enter extent"),
        SG.Push(),
        SG.Text("Number of items: "),
        SG.Input(default_text="", size=(6, 1)),
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
        SG.Text("Provenance")
    ],
    [
        SG.Multiline(default_text="output message goes here")
    ],
    [
        SG.Text("Notes: "),
        SG.Push(),
        SG.Multiline(default_text="Enter notes"),
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
        SG.Multiline(default_text="condition list goes here"),
        SG.Push(),
        SG.Multiline(default_text="List of issues")
    ],
    [
        SG.Text("treatment plan")
    ],
    [
        SG.Multiline(default_text="treatment plan goes here"),
        SG.Push(),
        SG.Multiline(default_text="List of selected POAs")
    ],
    [
        SG.Text("Notes:")
    ],
    [
        SG.Multiline(default_text="notes goes here"),
    ],
    [
        SG.Text("Estimated treatment hours: "),
        SG.Input("", size=(6, 1)),
        SG.Text("hrs"),
        SG.Push()
    ]
]

layout_treatments = [
    [
        SG.Text("Treatment plan"),
        SG.Push(),
        SG.Multiline(default_text="treatment plan items goes here")
    ],
    [
        SG.Text("treatment: "),
        SG.Combo(values=['Treatment'], key="-treatment_drop-"),
        SG.Push(),
        SG.Text("Treated by: "),
        SG.Combo(values=['Treated by'], key="-treated_by-"),
        SG.Push(),
        SG.Text("Date: "),
        SG.Input(default_text="Enter date as YYYY-MM-DD"),
    ],
    [
        SG.Text("Notes: "),
        SG.Push()
    ],
    [
        SG.Multiline()
    ],
    [
        SG.Text("Actual time: "),
        SG.Input(""),
        SG.Text("hrs")
    ],
    # treatment type separated by |, intraitem separated by ~. [0] = treatment type [1] = notes, [2] = treated by [3] = date [4] = hours to complete
    [
        SG.Push(),
        SG.Text("DON'T FORGET TO TAKE PHOTOS!", font=("Courier", 14, "bold"), text_color="darkred"),
        SG.Push()
    ]
]

layout_reports = [
    [
        SG.Text("Treated by: "),
        SG.Input(default_text="Enter treated by"),
        SG.Push(),
        SG.Text("Total actual time: "),
        SG.Input(default_text="Enter total actual time"),
    ],
    [
        SG.Push(),
        SG.Text("Conservation Summary: "),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="enter summary narrative of conservation actions")
    ],
    [
        SG.Push(),
        SG.Button("Create Report"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Image captions: "),
        SG.Push()
    ],
    [
        SG.Multiline("filename"),
        SG.Input(default_text="Enter image captions"),
    ],
    [
        SG.Text("Image preview"),
        SG.Multiline("image previewer goes here")
    ]
]

layout_images = [
    [
        SG.Text("Image text goes here")
    ],
    [
        SG.Push(),
        SG.Text("path to images folder"),
        SG.Input(default_text="Enter path to images folder"),
        SG.FileBrowse()
    ],
    [
        SG.Push(),
        SG.Button("Load image list"),
        SG.Push()
    ],
    [
        SG.Multiline(default_text="filelist goes here"),
        SG.VerticalSeparator(),
        SG.Multiline("image rendering goes here")
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
            window['-requestor-'].update(values=requestor_list)
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
            treatment_drop_list = []
            for item in my_config['treatmentDD'].items():
                treatment_drop_list.append(item[0])
            treatment_drop_list.sort()
            window['-treatment_drop-'].update(values=treatment_drop_list)
            treated_by_list = []
            for item in my_config['treatmentStaff'].items():
                treated_by_list.append(item[0])
            treated_by_list.sort()
            window['-reviewed_by-'].update(values=treated_by_list)
            window['-treated_by-'].update(values=treated_by_list)
            df = pd.read_excel(values['-spreadsheet-'], dtype=object, sheet_name='Conservation Reports')
            print("loaded spreadsheet")
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
                new_df = pd.concat([new_df, small_df], ignore_index=True)
                window['-table_filter-'].update(values=new_df.values.tolist())
                window['-header_info-'].update(f"{ConsID}: {Status}")
                title_for_window = Title
                if len(Title) > 50:
                    title_for_window = f"{Title[:47]}..."
                window['-title_info-'].update(f"{title_for_window}")
                An_Index = new_df.loc[new_df['ConsID'] == ConsID].index.tolist()[0]
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
            Item_Format = new_df.loc[new_df['ConsID'] == ConsID, 'Format'].values[0]
            Item_Substrate = new_df.loc[new_df['ConsID'] == ConsID, 'Substrate'].values[0]
            Item_Media = new_df.loc[new_df['ConsID'] == ConsID, 'Media'].values[0]
            History = new_df.loc[new_df['ConsID'] == ConsID, 'History'].values[0]
            Notes = new_df.loc[new_df['ConsID'] == ConsID, 'Notes'].values[0]
            Condition_Issues = new_df.loc[new_df['ConsID'] == ConsID, 'Condition Issues'].values[0]
            Treatment_Plan = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment Plan'].values[0]
            Number_of_Items = new_df.loc[new_df['ConsID'] == ConsID, 'Number of Items'].values[0]
            Estimated_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Est. Time (hrs)'].values[0]
            Treatment = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment'].values[0]
            Treatment_Notes = new_df.loc[new_df['ConsID'] == ConsID, 'Treatment Notes'].values[0]
            Actual_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Actual Time'].values[0]
            Treated_By = new_df.loc[new_df['ConsID'] == ConsID, 'Treated by'].values[0]
            Total_Actual_Time = new_df.loc[new_df['ConsID'] == ConsID, 'Total Actual Time'].values[0]
            Date_Completed = new_df.loc[new_df['ConsID'] == ConsID, 'Date Completed'].values[0]
            print("values loaded")
            window['-header_info-'].update(f"{ConsID}: {Status}")
            title_for_window = Title
            if len(Title) > 50:
                title_for_window = f"{Title[:47]}..."
            window['-title_info-'].update(f"{title_for_window}")
            An_Index = new_df.loc[new_df['ConsID'] == ConsID].index.tolist()[0]
            window['index_key'].update(f"{An_Index}")
            print(An_Index)
    if event == "-save-":
        print(An_Index)
        if values['index_key'] == "":
            print("load or create a record before trying to save")
        else:
            print("saving data")
            writer = df.to_excel(values['-spreadsheet-'], sheet_name="Conservation Reports", index=False)
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()