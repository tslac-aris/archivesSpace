import PySimpleGUI as SG
import PIL
import pandas as pd

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
        SG.FileBrowse(file_types=[("text file extension", "*.txt"), ("cfg file extension", "*.cfg")])
    ],
    [
        SG.Push(),
        SG.Button("Load Spreadsheet and Config file"),
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
        SG.Input(default_text="Enter title"),
    ],
    [
        SG.Text("Conservation identifier: ", size=(25,1)),
        SG.Input(default_text="Enter conservation identifier"),
    ],
    [
        SG.Text("Initial status: ", size=(25,1)),
        SG.Combo(values=['some status'])
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
        SG.Combo(values=['some status']),
        SG.Text("Conservation ID: "),
        SG.Input(default_text="Enter conservation ID"),
        SG.Text("Priority: "),
        SG.Combo(values=['some priority'])
    ],
    [
        SG.Push(),
        SG.Button("Filter data", key="-filter-"),
        SG.Push()
    ],
    [
        SG.Text("Options preview"),
        SG.Multiline(default_text="output message goes here")
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
        SG.Combo(values=['Department']),
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
        SG.Combo(values=['Review']),
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
        SG.Combo(values=['Priority level']),
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
        SG.Combo(values=['format type goes here']),
        SG.Push(),
        SG.Text("Substrate: "),
        SG.Combo(values=['Substrate']),
        SG.Push(),
        SG.Text("Media type: "),
        SG.Combo(values=['Media type']),
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
        SG.Combo(values=['Treatment']),
        SG.Push(),
        SG.Text("Treated by: "),
        SG.Combo(values=['Treated by']),
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
        SG.Button("Save changes")
    ],
    [
        SG.Text("title", text_color="darkblue", font=("Arial", 14, "bold"), key="-title_info-"),
        SG.Push(),
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
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()