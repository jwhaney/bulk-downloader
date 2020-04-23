import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import requests
import time, sys, os
from datetime import datetime
from uuid import UUID
import threading

# master/parent window contains all gui elements
window = tk.Tk()
window.maxsize(1300, 1200)
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
bottom_frame_left = tk.Frame(bottom_frame, borderwidth=10)
bottom_frame_right = tk.Frame(bottom_frame, borderwidth=10)
frame_list = [
              top_frame,
              middle_frame_1,
              middle_frame_2,
              middle_frame_3,
              middle_frame_4,
              bottom_frame,
              bottom_frame_left,
              bottom_frame_right
              ]
# for loop to pack all frames
for frame in frame_list:
    frame.pack(fill='both')

# label variables
label_1 = tk.Label(top_frame, text="Enter a TNRIS DataHub Collection ID: ")
label_2 = tk.Label(middle_frame_1, text="If the Collection ID entered has multiple resource types, you can filter them here.")
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

label_5 = tk.Label(middle_left_frame_2, text="Lidar Filters")
label_6 = tk.Label(middle_right_frame_2, text="Imagery Filters")
filter_lbl_list = [label_5, label_6]
for lbl in filter_lbl_list:
    lbl.configure(font=('Courier', 9, 'bold'))
    lbl.pack(side='top',anchor='w')

# resource types check box variables - onvalue string is used in the api query (resource_type_abbreviation)
type_value = tk.StringVar()
type_value.set("")
type_1 = tk.Checkbutton(middle_left_frame_2, text="Lidar Point Cloud", var=type_value, onvalue="LPC", offvalue="")
type_2 = tk.Checkbutton(middle_left_frame_2, text="Hypsography", var=type_value, onvalue="HYPSO", offvalue="")
type_3 = tk.Checkbutton(middle_left_frame_2, text="Digital Elevation Model", var=type_value, onvalue="DEM", offvalue="")
type_4 = tk.Checkbutton(middle_right_frame_2, text="Color Infrared (3 Band)", var=type_value, onvalue="CIR", offvalue="")
type_5 = tk.Checkbutton(middle_right_frame_2, text="Natural Color (3 Band)", var=type_value, onvalue="NC", offvalue="")
type_6 = tk.Checkbutton(middle_right_frame_2, text="Natural Color/Color Infrared (4 Band)", var=type_value, onvalue="NC-CIR", offvalue="")
type_7 = tk.Checkbutton(middle_right_frame_2, text="Black & White (1 Band)", var=type_value, onvalue="BW", offvalue="")
type_list = [type_1, type_2, type_3, type_4, type_5, type_6, type_7]
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
    # Allow user to select a directory and store it in global var called folder_path
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

    # function to check if a valid uuid is provided
    def is_valid_uuid(val):
        try:
            UUID(str(val))
            return True
        except ValueError:
            return False

    # first check to make sure the collection id string is valid
    # then assign data variable based on checkbox selections (build the url string requests needs to get data from rest endpoint)
    if is_valid_uuid(c):
        if c and not t:
            # if no selections made, build url string to get all resources for that collection id
            print('no selections made')
            data = requests.get(base_url + id_query + c).json()
        elif c and t:
            # if type selection made but not area, build the url string
            print('type selection made. type = {}'.format(t))
            '''
            possible future enhancement here to add ability to handle multiple resource type filters
            '''
            data = requests.get(base_url + id_query + c + type_abbr_query + t).json()

        # progress bar update function
        def p_bar(value):
            progress['value'] = value
            progress.update_idletasks()

        # show user how many collection resources returned from query
        display_message_1.set("{} resources found for tnris collection id {}".format(data['count'], c))
        message_area_1.update_idletasks()

        """
        main logic
        1) make sure data download directory (folder_path variable) is provided and exists; else throw error message
        2) check that there are no incorrect type filters applied so that the request actually has api results - based on
           the api request count > 0.
        3) loop through all object resources for the provided collection and save them to file using same name as s3 .zip
           and save it in the provided directory
        4) update the progress bar and message feedback for user to see progress as files are being downloaded
        5) throw any specific request library exceptions / errors to the user for feedback
        """

        if os.path.exists(folder_path.get()):
            if data['count'] > 0:
                # api data count variables - string and integer
                api_str_count = str(data['count'])
                api_num_count = data['count']

                print("beginning dowload process")

                # start time to be used later to calculate total program run time
                start_time = datetime.now().replace(microsecond=0)

                for obj in data['results']:
                    try:
                        print("downloading resource id: {}".format(obj['resource'].rsplit('/', 1)[-1]))
                        # assign next object['resource'] url to file variable
                        file = requests.get(obj["resource"], stream=True)
                        # write file variable to actual local zipfile saving to user provided directory and doing it in chunks
                        with open('{}/{}'.format(folder_path.get(), obj['resource'].rsplit('/', 1)[-1]), 'wb') as zipfile:
                            for chunk in file.iter_content(chunk_size=1024):
                                if chunk:
                                    zipfile.write(chunk)
                        # count each file written
                        count += 1
                        # update progress_value variable by dividing new count number by total api object count
                        progress_value = round((count/api_num_count)*100)
                        print(str(progress_value) + '% downloaded')
                        # feed new progress value into p_bar function to update gui
                        p_bar(progress_value)
                        # show display message/text as progress percentage string
                        display_message_1.set("{}/{} resources downloaded".format(count, api_str_count))
                        display_message_2.set("download progress: " + str(progress_value) + "%")
                        # make sure message area/labels are updated
                        message_area_1.update_idletasks()
                        message_area_2.update_idletasks()
                        if progress_value == 100:
                            end_time = datetime.now().replace(microsecond=0)
                            print('total_time is:', str(end_time - start_time))
                            display_message_2.set("100% complete. total time = {}".format(end_time - start_time))
                            message_area_2.update_idletasks()
                    # sepcific requests library exceptions to catch errors getting data from the api
                    except requests.exceptions.HTTPError as http_error:
                        print ("http error:", http_error)
                        error_message.set("http error: ", http_error)
                        message_area_3.update_idletasks()
                    except requests.exceptions.ConnectionError as connection_error:
                        print ("error connecting:", connection_error)
                        error_message.set("error connecting: ", connection_error)
                        message_area_3.update_idletasks()
                    except requests.exceptions.Timeout as timeout_error:
                        print ("timeout error:", timeout_error)
                        error_message.set("timeout error: ", timeout_error)
                        message_area_3.update_idletasks()
                    # general catch all requests library exception to catch an error if it is outside the above exceptions
                    except requests.exceptions.RequestException as general_error:
                        print ("OOps, there was some error: ", general_error)
                        error_message.set("OOps, there was some error: ", general_error)
                        message_area_3.update_idletasks()

                print("completed. {} out of {} resource(s) successfully downloaded.".format(count, api_str_count))
                display_message_1.set("completed. {} out of {} resource(s) downloaded.".format(count, api_str_count))
                # update message area/label
                message_area_1.update_idletasks()
            else:
                # return a message to the user that there is an error with either the  collection id string or the filter applied
                print("Error. No resource results. Please check your collection id or the filter applied.")
                error_message.set("Error. No resource results. Please check your collection id or the filter applied.")
                # update error message/label
                message_area_3.update_idletasks()
        else:
            print("Error. There was a problem with the directory provided to save data.")
            error_message.set("Error. There was a problem with the directory provided to save data.")
            # update error message/label
            message_area_3.update_idletasks()
    else:
        print("Error. There was a problem with the collection id provided.")
        error_message.set("Error. There was a problem with the collection id provided.")
        message_area_3.update_idletasks()

def start():
    main_thread = threading.Thread(name='bulk_download', target=bulk_download)
    main_thread.start()

def kill():
    print('killing the bulk_download function')
    window.quit()

def stop():
    print('stopping the bulk downloader')
    kill_thread = threading.Thread(name='killer', target=kill)
    kill_thread.start()

# buttons that do stuff
browse = tk.Button(top_frame, text="Browse", command=browse_button)
browse.pack()
# on macos, button color doesn't seem to be properly reflected; comment out for now and use default color
# getdata_button = tk.Button(bottom_frame, text="Get Data", command=bulk_download, bg="#009933", fg="white", activebackground="green", activeforeground="white")
getdata = tk.Button(bottom_frame_right, text="Get Data", command=start)
getdata.pack(side='right')
stop_it = tk.Button(bottom_frame_left, text="Stop", command=stop)
stop_it.pack(side='left')
# fire tkinter mainloop() on window to run the program
window.mainloop()
