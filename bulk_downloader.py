import requests
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import time, sys

# master/parent window contains all gui elements
window = tk.Tk()
# window.geometry("1300x850")
window.maxsize(1300, 900)
window.resizable(width=False,height=False)
window.title("TNRIS DataHub Bulk Download Utility")

# frame variables - parent is window
top_frame = tk.Frame(window, borderwidth=20, pady=10)
middle_frame_1 = tk.Frame(window, borderwidth=20)
middle_frame_2 = tk.Frame(window, borderwidth=20)
middle_left_frame_2 = tk.Frame(middle_frame_2, borderwidth=10)
middle_left_frame_2.grid(column=0,row=1)
middle_right_frame_2 = tk.Frame(middle_frame_2, borderwidth=10)
middle_right_frame_2.grid(column=1,row=1)
middle_frame_3 = tk.Frame(window, borderwidth=20)
middle_frame_4 = tk.Frame(window, borderwidth=20)
bottom_frame = tk.Frame(window, borderwidth=20, pady=10)
frame_list = [top_frame, middle_frame_1, middle_frame_2, middle_frame_3, middle_frame_4, bottom_frame]
# for loop to pack all frames
for frame in frame_list:
    frame.pack(fill='both')

# label variables
label_1 = tk.Label(top_frame, text="Enter a TNRIS DataHub Collection ID: ")
label_2 = tk.Label(middle_frame_1, text="**Optional: Select the resource type you want to download from the Collection ID entered.")
label_3 = tk.Label(middle_frame_1, text="If no selection is made, all resources for the collection will be downloaded.")
label_list = [label_1, label_2, label_3]
# for loop to configure all labels with font
for label in label_list:
    label.configure(font=('Courier', 9, 'bold'))
    label.pack(fill='both')

# collection id entry
collection_id = tk.Entry(top_frame, width=45, font=('Courier', 9))
collection_id.pack()
collection_id.focus()

label_4 = tk.Label(top_frame, text="Browse to a directory where you would like to save your downloaded data.")
label_4.configure(font=('Courier', 9, 'bold'), pady=10)
label_4.pack(fill='both')

# resource types check box variables - onvalue string is used in the api query (resource_type_abbreviation)
type_value = tk.StringVar()
type_value.set("")
type_1 = tk.Checkbutton(middle_left_frame_2, text="Lidar Point Cloud", var=type_value, onvalue="LPC", offvalue="")
type_2 = tk.Checkbutton(middle_left_frame_2, text="Hypsography", var=type_value, onvalue="HYPSO", offvalue="")
type_3 = tk.Checkbutton(middle_left_frame_2, text="Digital Elevation Model", var=type_value, onvalue="DEM", offvalue="")
type_4 = tk.Checkbutton(middle_left_frame_2, text="Land Cover", var=type_value, onvalue="LC", offvalue="")
# type_5 = tk.Checkbutton(middle_left_frame_2, text="Vector", var=type_value, onvalue="VECTOR", offvalue="")
type_6 = tk.Checkbutton(middle_right_frame_2, text="Color Infrared (3 Band)", var=type_value, onvalue="CIR", offvalue="")
type_7 = tk.Checkbutton(middle_right_frame_2, text="Natural Color (3 Band)", var=type_value, onvalue="NC", offvalue="")
type_8 = tk.Checkbutton(middle_right_frame_2, text="Natural Color/Color Infrared (4 Band)", var=type_value, onvalue="NC-CIR", offvalue="")
type_9 = tk.Checkbutton(middle_right_frame_2, text="Black & White (1 Band)", var=type_value, onvalue="BW", offvalue="")
# type_10 = tk.Checkbutton(middle_right_frame_2, text="Map", var=type_value, onvalue="MAP", offvalue="")
type_list = [type_1, type_2, type_3, type_4, type_6, type_7, type_8, type_9]
# for loop to configure all checkbuttons with font
for type in type_list:
    type.configure(font=('Courier', 9))
    type.pack(side='top',anchor='w')

# Progress bar widget
progress = Progressbar(middle_frame_3, orient='horizontal')
progress.pack(fill='both')
# Progress bar config
progress.config(mode='determinate', value=0, maximum=100)

# print messages from the bulk_download function
display_message_1 = tk.StringVar()
display_message_2 = tk.StringVar()
error_message = tk.StringVar()
display_message_1.set("Messages here provide download progress feedback.")
message_area_1 = tk.Label(middle_frame_4, textvariable=display_message_1, font=('Courier', 9))
message_area_2 = tk.Label(middle_frame_4, textvariable=display_message_2, font=('Courier', 9), fg='green')
message_area_3 = tk.Label(middle_frame_4, textvariable=error_message, font=('Courier', 9), fg='red')
message_area_list = [message_area_1, message_area_2, message_area_3]
# for loop to pack message areas
for area in message_area_list:
    area.pack(fill='both')

folder_path = tk.StringVar()
label_4 = tk.Label(top_frame, textvariable=folder_path)
label_4.configure(font=('Courier', 9))
label_4.pack(fill='both')

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print('folder_path variable:', folder_path.get())

# function to make requests to api.tnris.org resources endpoint to download data
def bulk_download():
    # variables
    display_message_1.set("Messages here provide download progress feedback.") # reset feedback message
    display_message_2.set("") # reset feedback message
    error_message.set("") # reset any error messages
    base_url = "https://api.tnris.org/api/v1/resources/"
    id_query = "?collection_id="
    type_query = "&resource_type_name="
    type_abbr_query = "&resource_type_abbreviation="
    area_query = "&area_type="
    data = ""
    count = 0
    progress_value = 0
    c = collection_id.get()
    t = type_value.get()

    # print('folder_path variable = ', folder_path)

    # assign data variable based on checkbox selections (build the url string requests needs to get data from rest endpoint)
    if c and not t:
        # if no selections made, build url string to get all resources for that collection id
        print('no selections made')
        data = requests.get(base_url + id_query + c).json()
    elif c and t:
        # if type selection made but not area, build the url string
        print('type selections made. type = {}'.format(t))
        '''
        future enhancement to add and handle multiple selections for type only
        '''
        data = requests.get(base_url + id_query + c + type_abbr_query + t).json()

    # progress bar function
    def p_bar(value):
        progress['value'] = value
        middle_frame_3.update_idletasks()

    # loop through all object resources for a collection id and save them to file using same name as s3 .zip name
    # also update progress bar feedback for user to see progress
    if data['count'] > 0:
        # api data count variables - string and integer
        api_str_count = str(data['count'])
        api_num_count = data['count']

        # show user how many collection resources returned from query
        display_message_1.set("{} resources found for tnris collection id {}".format(data['count'],c))
        middle_frame_4.update_idletasks()
        time.sleep(1)
        print("beginning dowload process")

        for obj in data['results']:
            try:
                print("downloading resource id: {}".format(obj['resource'].rsplit('/', 1)[-1]))
                # assign next object['resource'] url to file variable
                file = requests.get(obj["resource"], stream=True)
                # write file variable to actual local file to this projects data directory
                open('{}/{}'.format(folder_path.get(), obj['resource'].rsplit('/', 1)[-1]), 'wb').write(file.content)
                # count each file written
                count += 1
                # update progress_value variable by dividing new count number by total api object count
                progress_value = round((count/api_num_count)*100)
                print(progress_value)
                # feed new progress value into p_bar function to update gui
                p_bar(progress_value)
                # show display message as progress percentage string
                display_message_1.set("{}/{} resources downloaded".format(count, api_str_count))
                display_message_2.set("download progress: " + str(progress_value) + "%")
                # make sure message is updated
                middle_frame_4.update_idletasks()
            except requests.ConnectionError:
                print("requests connection error")
                error_message.set("requests connection error")
            except requests.ConnectTimeout:
                print("requests timeout error")
                error_message.set("requests timeout error")

        print("Script process completed. {} out of {} resource(s) successfully downloaded.".format(count, api_str_count))
        display_message_1.set("Script process completed. {} out of {} resource(s) successfully downloaded.".format(count, api_str_count))
        # make sure message is updated
        middle_frame_4.update_idletasks()

    else:
        # return a message to the user that there is an error with either the  collection id string or filters applied
        print("ERROR. No resource results. Please check your collection id string or filters applied.")
        error_message.set("ERROR. No resource results. Please check your collection id string or filters applied.")
        # make sure message is updated
        middle_frame_4.update_idletasks()

# buttons that do stuff
browse = tk.Button(top_frame, text="Browse", command=browse_button)
browse.pack()
# on macos, button color doesn't seem to be properly reflected; comment out for now and use default color
# getdata_button = tk.Button(bottom_frame, text="Get Data", command=bulk_download, bg="#009933", fg="white", activebackground="green", activeforeground="white")
getdata = tk.Button(bottom_frame, text="Get Data", command=bulk_download)
getdata.pack()

window.mainloop()
