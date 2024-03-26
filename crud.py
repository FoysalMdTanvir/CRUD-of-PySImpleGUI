import PySimpleGUI as sg
import sqlite3

conn = sqlite3.connect('client_reg.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS patients(
        name text,
        dob text,
        gender text,
        address text,
        phone integer  
    ) """)

conn.commit()
conn.close()

sg.theme('Default')
sg.set_options(font=('TimesNewRoman11'), text_color='black')

layout = [
    [sg.T('Registration form')],
    [sg.T('NAME',size=(10, 1)),sg.Push(),sg.I(size=(43,3),key='name')],
     [
        sg.T('Date of Birth', size=(10, 1)),
        sg.I(size=(26, 3), key='dob', readonly=True),
        sg.CalendarButton('Select', target='dob', format='%Y-%m-%d',pad=None),
    ],
    [sg.T('GENDER',size=(10, 1)),sg.Push(),sg.Combo(size=(41,3),values=['Male','Female'],key='gender', readonly=True)],
    [sg.T('ADDRESS',size=(10,1)),sg.Push(),sg.ML(size=(41,3),key='address')],
    [sg.T('CONTACT',size=(10,1)),sg.Push(),sg.I(size=(43,3),key='phone')],
    [sg.Button('SUBMIT', expand_x=True), sg.Button('CLEAR', expand_x=True),sg.Button('SHOW ALL', expand_x=True), sg.Button('EXIT', expand_x=True)],
]

window = sg.Window('IME CRUD APP', layout)

#this 3 function for viewing all records
def retrieve_patient_records():
    results = []
    conn=sqlite3.connect('client_reg.db')
    c = conn.cursor()
    query = "SELECT name,dob,gender, address, phone from patients"
    c.execute(query)
    for row in c:
        results.append(list(row))
    return results

def get_patient_records():
    client_records=retrieve_patient_records()
    return client_records

def create_records():
    client_records_array=get_patient_records()
    headings = ['NAME', 'DATE OF BIRTH', 'GENDER', 'ADDRESS', 'CONTACT']
    
    layout_for_display = [
        [sg.Table(values=client_records_array,
                headings=headings,
                max_col_width=35,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='left',
                num_rows=10,
                key='PATIENTTABLE',
                row_height=60,
                enable_events=True,
                tooltip='all patients results'
                  )],
    ]
    windr=sg.Window('Summary Results', layout_for_display, modal=True)

    while True:
        event, values=windr.read()
        if event == sg.WIN_CLOSED:
            break
        
# CLEAR button function
def clear_inputs():
    for key in values:
        window['name'].update('')
        window['dob'].update('')
        window['gender'].update('')
        window['address'].update('')
        window['phone'].update('')
    return None
def save_data_to_database():
    conn = sqlite3.connect('client_reg.db')
    c = conn.cursor()
    c.execute("INSERT INTO patients VALUES(:name, :dob, :gender, :address, :phone)",
        {
            'name': values['name'],
            'dob': values['dob'],
            'gender': values['gender'],
            'address': values['address'],
            'phone': values['phone'],
        }
    )

    conn.commit()
    conn.close()

while True:
    event, values = window.read()
    if event==sg.WIN_CLOSED or event=='EXIT':
        break
    elif event=='CLEAR':
        clear_inputs()
    elif event == 'SHOW ALL':
        create_records()
        # Check if any required field is blank
        required_fields = ['name','dob','gender','address','phone']
        if any(values[field] == '' for field in required_fields):
            sg.popup_error('Please fill in all fields.')
            continue
        else:
            try:
                summary_list="The following information has been added to database."
                na="\nName: "+values['name']
                summary_list+=na
                db="\nDate of Birth: "+values['dob']
                summary_list+=db
                ge="\nGender: "+values['gender']
                summary_list+=ge
                ad="\nAddress: "+values['address']
                summary_list+=ad
                cn="\nContact: "+values['phone']
                summary_list+=cn
                choice=sg.PopupOKCancel(summary_list, 'Please confirm entry')
                if choice=='OK':
                    clear_inputs()
                    save_data_to_database()
                    sg.PopupQuick('Saved to database!')
                else:
                    sg.PopupOk('Edit entry')
            except:
                sg.Popup('Some error, kindly report to the admin team!')

    """if event == 'SUBMIT':
        name=values['name']
        if name=='':
            sg.PopupError('Missing name', )
        dob=values['dob']
        if dob=='':
            sg.PopupError('Missing Date of Birth', )
        gender=values['gender']
        if gender=='':
            sg.PopupError('Missing gender', )
        address=values['address']
        if address=='':
            sg.PopupError('Missing Address', )
        phone=values['phone']
        if phone=='':
            sg.PopupError('Missing phone', )"""
    
window.close()