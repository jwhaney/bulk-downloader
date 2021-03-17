# ---------- Imports ----------

import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import Scrollbar
import requests, os
from datetime import datetime
from uuid import UUID
import threading

# ---------- Main ----------

class BulkDownloader(object):

    def __init__(self, base_url, id_query, type_query, data, running, count):
        self.base_url = base_url
        self.id_query = id_query
        self.type_query = type_query
        self.data = data
        self.running = running
        self.count = count

    def gui(self):
        # master/parent window contains all gui elements
        window = tk.Tk()
        window.title("TNRIS DataHub Bulk Download Utility")

        # frame variables - parent is window
        top_frame = tk.Frame(window, borderwidth=10)
        middle_frame_1 = tk.Frame(window, borderwidth=10)
        middle_frame_2 = tk.Frame(window, borderwidth=10)
        middle_left_frame_2 = tk.Frame(middle_frame_2, borderwidth=10)
        middle_left_frame_2.pack(side='left', expand=1)
        middle_right_frame_2 = tk.Frame(middle_frame_2, borderwidth=10)
        middle_right_frame_2.pack(side='right', expand=1)
        middle_frame_3 = tk.Frame(window, borderwidth=10, padx=10)
        middle_frame_4 = tk.Frame(window, borderwidth=10)
        bottom_frame = tk.Frame(window, borderwidth=10, pady=10)
        frame_list = [
                      top_frame,
                      middle_frame_1,
                      middle_frame_2,
                      middle_frame_3,
                      middle_frame_4,
                      bottom_frame
                      ]
        # for loop to pack all frames
        for frame in frame_list:
            frame.pack(fill='both')

        # label variables
        label_1 = tk.Label(top_frame, text="Enter a TNRIS DataHub Collection ID: ")
        label_2 = tk.Label(middle_frame_1, text="If the collection entered has multiple resource types, filter them here.")
        label_3 = tk.Label(middle_frame_1, text="No filter selection will result in all collection resources downloaded.")
        label_list = [label_1, label_2, label_3]
        # for loop to configure all labels with font
        for label in label_list:
            label.configure(font=('Courier', 10, 'bold'))
            label.pack(fill='both')

        # collection id entry
        collection_id = tk.Entry(top_frame, width=45, font=('Courier', 10))
        collection_id.pack()
        collection_id.focus()

        label_4 = tk.Label(top_frame, text="Browse to a directory where you can save your downloaded data.")
        label_5 = tk.Label(middle_left_frame_2, text="Lidar")
        label_6 = tk.Label(middle_right_frame_2, text="Imagery")
        lbl_list = [label_4, label_5, label_6]
        for lbl in lbl_list:
            lbl.config(font=('Courier', 10, 'bold'), pady=10)
            lbl.pack(fill='both')

        # resource types check box variables - onvalue string is used in the api query (resource_type_abbreviation)
        type_value = tk.StringVar()
        type_value.set("")
        type_1 = tk.Checkbutton(middle_left_frame_2, text="Lidar Point Cloud", var=type_value, onvalue="LPC", offvalue="")
        type_2 = tk.Checkbutton(middle_left_frame_2, text="Hypsography", var=type_value, onvalue="HYPSO", offvalue="")
        type_3 = tk.Checkbutton(middle_left_frame_2, text="Digital Elevation Model", var=type_value, onvalue="DEM", offvalue="")
        type_placeholder = tk.Label(middle_left_frame_2, text="") # this empty label is used for alignment
        type_4 = tk.Checkbutton(middle_right_frame_2, text="Color Infrared (3 Band)", var=type_value, onvalue="CIR", offvalue="")
        type_5 = tk.Checkbutton(middle_right_frame_2, text="Natural Color (3 Band)", var=type_value, onvalue="NC", offvalue="")
        type_6 = tk.Checkbutton(middle_right_frame_2, text="Natural Color/Color Infrared (4 Band)", var=type_value, onvalue="NC-CIR", offvalue="")
        type_7 = tk.Checkbutton(middle_right_frame_2, text="Black & White (1 Band)", var=type_value, onvalue="BW", offvalue="")
        type_list = [type_1, type_2, type_3, type_placeholder, type_4, type_5, type_6, type_7]
        # for loop to pack & configure checkbuttons
        for l in type_list:
            l.config(font=('Courier', 10))
            l.pack(fill="both")

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
        message_area_1 = tk.Label(middle_frame_4, textvariable=display_message_1, font=('Courier', 10))
        message_area_2 = tk.Label(middle_frame_4, textvariable=display_message_2, font=('Courier', 10), fg='green')
        message_area_3 = tk.Label(middle_frame_4, textvariable=error_message, font=('Courier', 10), fg='red')
        message_area_list = [message_area_1, message_area_2, message_area_3]
        # for loop to pack message areas
        for area in message_area_list:
            area.pack(fill='both')

        folder_path = tk.StringVar()
        label_4 = tk.Label(top_frame, textvariable=folder_path)
        label_4.configure(font=('Courier', 10), pady=10)
        label_4.pack(fill='both')

        def browse_button():
            # Allow user to select a directory and store it in global var called folder_path
            global folder_path
            filename = filedialog.askdirectory()
            folder_path.set(filename)
            print('folder_path variable:', folder_path.get())

    def downerator(self, data, running, count):
        # main method that iterates over api results and downloads collection resources
        # variables
        base_url = "https://api.tnris.org/api/v1/resources/"
        id_query = "?collection_id="
        type_query = "&resource_type_abbreviation="
        data = requests.get(base_url + id_query).json()
        running = True
        count = 0

        if data['count'] > 0:
            for obj in data['results']:
                if running:
                    try:
                        # count each file written
                        count += 1
                        print("{} downloading resource id: {}".format(count, obj['resource'].rsplit('/', 1)[-1]))
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
                        # assign next object['resource'] url to file variable
                        file = requests.get(obj["resource"], stream=True)
                        # write file variable to actual local zipfile saving to user provided directory and doing it in chunks
                        # with open('{}/{}'.format(folder_path.get(), obj['resource'].rsplit('/', 1)[-1]), 'wb') as zipfile:
                        #     for chunk in file.iter_content(chunk_size=1024):
                        #         if chunk:
                        #             zipfile.write(chunk)
                    # sepcific requests library exceptions to catch any errors getting data from the api
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
            # checks if next value present for pagination; if so, use it as data variable and re-run function
            if data['next']:
                data = requests.get(data['next']).json()
                self.pagerator(data, running, count)


if __name__ == "__main__":
    # variables
    base_url = "https://api.tnris.org/api/v1/resources/"
    id_query = "?collection_id="
    type_query = "&resource_type_abbreviation=DEM"
    data = requests.get(base_url + id_query).json()
    running = True
    count = 0

    script = BulkDownloader(base_url, id_query, type_query, data, running, count)
    script.gui()
    script.downerator(data, running, count)
