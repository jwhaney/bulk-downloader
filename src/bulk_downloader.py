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
    def __init__(self, window, running, data, count, progress_value):
        # variables
        self.running = running
        self.data = data
        self.count = count
        self.progress_value = progress_value

        # master/parent window contains all gui elements
        self.window = window
        window.title("TNRIS DataHub Bulk Download Utility")

        # frame variables - parent is window
        self.top_frame = tk.Frame(window, borderwidth=10)
        self.middle_frame_1 = tk.Frame(window, borderwidth=10)
        self.middle_frame_2 = tk.Frame(window, borderwidth=10)
        self.middle_left_frame_2 = tk.Frame(self.middle_frame_2, borderwidth=10)
        self.middle_left_frame_2.pack(side='left', expand=1)
        self.middle_right_frame_2 = tk.Frame(self.middle_frame_2, borderwidth=10)
        self.middle_right_frame_2.pack(side='right', expand=1)
        self.middle_frame_3 = tk.Frame(window, borderwidth=10, padx=10)
        self.middle_frame_4 = tk.Frame(window, borderwidth=10)
        self.bottom_frame = tk.Frame(window, borderwidth=10, pady=10)
        self.frame_list = [
                      self.top_frame,
                      self.middle_frame_1,
                      self.middle_frame_2,
                      self.middle_frame_3,
                      self.middle_frame_4,
                      self.bottom_frame
                      ]
        # for loop to pack all frames
        for f in self.frame_list:
            f.pack(fill='both')

        # label variables
        self.label_1 = tk.Label(self.top_frame, text="Enter a TNRIS DataHub Collection ID: ")
        self.label_2 = tk.Label(self.middle_frame_1, text="If the collection entered has multiple resource types, filter them here.")
        self.label_3 = tk.Label(self.middle_frame_1, text="No filter selection will result in all collection resources downloaded.")
        self.label_list = [self.label_1, self.label_2, self.label_3]
        # for loop to configure all labels with font
        for l in self.label_list:
            l.configure(font=('Courier', 10, 'bold'))
            l.pack(fill='both')

        # collection id entry
        self.collection_id = tk.Entry(self.top_frame, width=45, font=('Courier', 10))
        self.collection_id.pack()
        self.collection_id.focus()

        self.label_4 = tk.Label(self.top_frame, text="Browse to a directory where you can save your downloaded data.")
        self.label_5 = tk.Label(self.middle_left_frame_2, text="Lidar")
        self.label_6 = tk.Label(self.middle_right_frame_2, text="Imagery")
        self.lbl_list = [self.label_4, self.label_5, self.label_6]
        for lbl in self.lbl_list:
            lbl.config(font=('Courier', 10, 'bold'), pady=10)
            lbl.pack(fill='both')

        # resource types check box variables - onvalue string is used in the api query (resource_type_abbreviation)
        self.type_value = tk.StringVar()
        self.type_value.set("")
        self.type_1 = tk.Checkbutton(self.middle_left_frame_2, text="Lidar Point Cloud", var=self.type_value, onvalue="LPC", offvalue="")
        self.type_2 = tk.Checkbutton(self.middle_left_frame_2, text="Hypsography", var=self.type_value, onvalue="HYPSO", offvalue="")
        self.type_3 = tk.Checkbutton(self.middle_left_frame_2, text="Digital Elevation Model", var=self.type_value, onvalue="DEM", offvalue="")
        self.type_placeholder = tk.Label(self.middle_left_frame_2, text="") # this empty label is used for alignment
        self.type_4 = tk.Checkbutton(self.middle_right_frame_2, text="Color Infrared (3 Band)", var=self.type_value, onvalue="CIR", offvalue="")
        self.type_5 = tk.Checkbutton(self.middle_right_frame_2, text="Natural Color (3 Band)", var=self.type_value, onvalue="NC", offvalue="")
        self.type_6 = tk.Checkbutton(self.middle_right_frame_2, text="Natural Color/Color Infrared (4 Band)", var=self.type_value, onvalue="NC-CIR", offvalue="")
        self.type_7 = tk.Checkbutton(self.middle_right_frame_2, text="Black & White (1 Band)", var=self.type_value, onvalue="BW", offvalue="")
        self.type_list = [self.type_1, self.type_2, self.type_3, self.type_placeholder, self.type_4, self.type_5, self.type_6, self.type_7]
        # for loop to pack & configure checkbuttons
        for t in self.type_list:
            t.config(font=('Courier', 10))
            t.pack(fill="both")

        # Progress bar widget
        self.progress = Progressbar(self.middle_frame_3, orient='horizontal')
        self.progress.pack(fill='both')
        # Progress bar config
        self.progress.config(mode='determinate', value=0, maximum=100)

        # print messages from the downloader method
        self.display_message_1 = tk.StringVar()
        self.display_message_2 = tk.StringVar()
        self.error_message = tk.StringVar()
        self.display_message_1.set("Messages here provide download progress feedback.")
        self.message_area_1 = tk.Label(self.middle_frame_4, textvariable=self.display_message_1, font=('Courier', 10))
        self.message_area_2 = tk.Label(self.middle_frame_4, textvariable=self.display_message_2, font=('Courier', 10), fg='green')
        self.message_area_3 = tk.Label(self.middle_frame_4, textvariable=self.error_message, font=('Courier', 10), fg='red')
        self.message_area_list = [self.message_area_1, self.message_area_2, self.message_area_3]
        # for loop to pack message areas
        for a in self.message_area_list:
            a.pack(fill='both')

        self.folder_path = tk.StringVar()
        self.label_4 = tk.Label(self.top_frame, textvariable=self.folder_path)
        self.label_4.configure(font=('Courier', 10), pady=10)
        self.label_4.pack(fill='both')

        # pack buttons that run methods
        self.browse = tk.Button(self.top_frame, text="Browse", command=self.browse_button)
        self.browse.pack()
        self.getdata = tk.Button(self.bottom_frame, text="Get Data", command=self.start)
        self.getdata.pack(side='right', expand=1)
        self.stop_it = tk.Button(self.bottom_frame, text="Stop", command=self.stop)
        self.stop_it.pack(side='left', expand=1)

    # Allow user to select a directory and store it in global var called folder_path
    def browse_button(self):
        self.folder_path
        self.filename = filedialog.askdirectory()
        self.folder_path.set(self.filename)
        print('folder_path variable:', self.folder_path.get())
        return self.folder_path

    # fires the main method on its own separate thread
    def start(self):
        self.main_thread = threading.Thread(name='starter', target=self.get_data)
        self.main_thread.start()

    # method to set up separate thread and target for kill method
    # fired when the stop button is clicked
    def stop(self):
        self.kill_thread = threading.Thread(name='killer', target=self.kill(self.running))
        self.kill_thread.start()

    # this method changes the running variable from True to None and stops the main
    # downloader method from running / breaks the for loop when running = None
    def kill(self, running):
        response = messagebox.askokcancel(title="Stop Downloading", message="Are you sure you want to stop downloading?")
        # if ok button clicked to quit, set running var to None which will stop the for loop
        if response:
            print("stopping bulk downloader...")
            self.running = None

    # method to check if a valid uuid is provided
    def valid_uuid(self, val):
        try:
            UUID(str(val))
            return True
        except ValueError:
            return False

    # progress bar update method
    def p_bar(self, value):
        self.progress['value'] = value
        self.progress.update_idletasks()

    def get_data(self):
        self.display_message_1.set("Messages here provide download progress feedback.") # reset feedback message
        self.display_message_2.set("") # reset feedback message
        self.error_message.set("") # reset any error messages
        c = self.collection_id.get()
        t = self.type_value.get()
        self.count = 0
        base_url = "https://api.tnris.org/api/v1/resources/"
        id_query = "?collection_id="
        type_query = "&resource_type_abbreviation="
        # area_query = "&area_type="

        # first check to make sure the collection id string is a valid using valid_uuid method
        # then check if the folder_path directory to save the data exists
        # then assign data variable based on checkbox selections (build the url string requests needs to get data from rest endpoint)
        if self.valid_uuid(c):
            if os.path.exists(self.folder_path.get()):
                if c and not t:
                    # if no selections made, build url string to get all resources for that collection id
                    print('no selections made')
                    self.data = requests.get(base_url + id_query + c).json()
                elif c and t:
                    # if type selection made but not area, build the url string
                    print('type selection made. type = {}'.format(t))
                    '''
                    possible future enhancement here to add ability to handle multiple resource type filters
                    '''
                    self.data = requests.get(base_url + id_query + c + type_query + t).json()
            else:
                # retrun message to the user that there was a problem with the directory chosen to save downloaded data
                print("Error. Check the directory provided to save data.")
                self.error_message.set("Error. Check the directory provided to save data.")
                self.message_area_3.update_idletasks()
                return
        else:
            print("Error. Check the collection id provided.")
            self.error_message.set("Error. Check the collection id provided.")
            self.message_area_3.update_idletasks()
            return

        # run the downloader method
        if self.data:
            self.downloader(self.running, self.data, self.count)

    def downloader(self, running, data, count):
        # main method that iterates over api results and downloads collection resources
        api_num_count = self.data['count']
        api_str_count = str(self.data['count'])

        if self.data['count'] > 0:
            for obj in self.data['results']:
                if self.running:
                    try:
                        # count each file written
                        self.count += 1
                        print("{} | downloading resource id: {}".format(self.count, obj['resource'].rsplit('/', 1)[-1]))
                        # update progress_value variable by dividing new count number by total api object count
                        self.progress_value = round((self.count/api_num_count)*100)
                        # feed new progress value into p_bar function to update gui
                        self.p_bar(self.progress_value)
                        # show display message/text as progress percentage string
                        self.display_message_1.set("{}/{} resources downloaded".format(self.count, api_str_count))
                        self.display_message_2.set("download progress: " + str(self.progress_value) + "%")
                        # make sure message area/labels are updated
                        self.message_area_1.update_idletasks()
                        self.message_area_2.update_idletasks()
                        # assign next object['resource'] url to file variable
                        file = requests.get(obj["resource"], stream=True)
                        # write file variable to actual local zipfile saving to user provided directory and doing it in chunks
                        with open('{}/{}'.format(self.folder_path.get(), obj['resource'].rsplit('/', 1)[-1]), 'wb') as zipfile:
                            for chunk in file.iter_content(chunk_size=1024):
                                if chunk:
                                    zipfile.write(chunk)
                    # sepcific requests library exceptions to catch any errors getting data from the api
                    except requests.exceptions.HTTPError as http_error:
                        print ("http error:", http_error)
                        self.error_message.set("http error: ", http_error)
                        self.message_area_3.update_idletasks()
                    except requests.exceptions.ConnectionError as connection_error:
                        print ("error connecting:", connection_error)
                        self.error_message.set("error connecting: ", connection_error)
                        self.message_area_3.update_idletasks()
                    except requests.exceptions.Timeout as timeout_error:
                        print ("timeout error:", timeout_error)
                        self.error_message.set("timeout error: ", timeout_error)
                        self.message_area_3.update_idletasks()
                    # general catch all requests library exception to catch an error if it is outside the above exceptions
                    except requests.exceptions.RequestException as general_error:
                        print ("OOps, there was some error: ", general_error)
                        self.error_message.set("OOps, there was some error: ", general_error)
                        self.message_area_3.update_idletasks()
                else:
                    # if user stops program, display message
                    print("Bulk Downloader stopped.")
                    self.error_message.set("Bulk Downloader stopped.")
                    self.message_area_3.update_idletasks()
                    return
        else:
            # return a message to the user that there is an error with either the  collection id string or the filter applied
            print("Error. No resource results. Check your collection id or filters applied.")
            self.error_message.set("Error. No resource results. Check your collection id or filters applied.")
            self.message_area_3.update_idletasks()

        # if first page of resources downloaded successfully, run paginator method to see if there are additional pages
        self.paginator(self.running, self.count)

    def paginator(self, running, count):
        # check if next value present for pagination; if so, use it as data variable and re-run downloader method
        while self.data['next']:
            self.data = requests.get(self.data['next']).json()
            count = self.downloader(running, self.data, count)


# run the program
if __name__ == "__main__":
    window = tk.Tk()
    running = True
    data = ""
    count = 0
    progress_value = 0
    script = BulkDownloader(window, running, data, count, progress_value)
    window.mainloop()
