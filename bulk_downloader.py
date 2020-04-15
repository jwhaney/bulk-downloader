import requests
import tkinter as tk
from tkinter.ttk import Progressbar
import time, sys

# master/parent window contains all gui elements
window = tk.Tk()
window.title("TNRIS DataHub Bulk Download Utility")

# frame variables - parent is window
top_frame = tk.Frame(window, borderwidth=20)
middle_frame_1 = tk.Frame(window, borderwidth=20)
middle_frame_2 = tk.Frame(window, borderwidth=20)
middle_frame_3 = tk.Frame(window, borderwidth=20)
middle_frame_4 = tk.Frame(window, borderwidth=20)
bottom_frame = tk.Frame(window, borderwidth=20)
frame_list = [top_frame, middle_frame_1, middle_frame_2, middle_frame_3, middle_frame_4, bottom_frame]
# for loop to pack all frames
for frame in frame_list:
    frame.pack(fill='both')

# label variables
label_1 = tk.Label(top_frame, text="Enter a TNRIS DataHub Collection ID: ")
label_2 = tk.Label(middle_frame_1, text="**Optional: Select the resource type you want to download from the Collection ID entered.")
label_3 = tk.Label(middle_frame_1, text="If no selection is made, all resources for the collection will be downloaded.")
label_4 = tk.Label(middle_frame_2, text="**Optional: Select a resource area type.")
label_5 = tk.Label(middle_frame_2, text="If no selection is made, the default area type for the provided collection will be chosen.")
label_list = [label_1, label_2, label_3, label_4, label_5]
# for loop to pack all labels
for label in label_list:
    label.configure(font=('Courier', 11, 'bold'))
    label.pack(fill='both')

# collection id entry
collection_id = tk.Entry(top_frame, width=45, font=('Courier', 11))
collection_id.pack()
collection_id.focus()

# resource types check box variables
type_value = tk.StringVar()
type_value.set("")
type_1 = tk.Checkbutton(middle_frame_1, text="Lidar Point Cloud", var=type_value, onvalue="LPC", offvalue="")
type_2 = tk.Checkbutton(middle_frame_1, text="Hypsography", var=type_value, onvalue="HYPSO", offvalue="")
type_3 = tk.Checkbutton(middle_frame_1, text="Digital Elevation Model", var=type_value, onvalue="DEM", offvalue="")
type_4 = tk.Checkbutton(middle_frame_1, text="Land Cover", var=type_value, onvalue="LC", offvalue="")
type_5 = tk.Checkbutton(middle_frame_1, text="Vector", var=type_value, onvalue="VECTOR", offvalue="")
type_6 = tk.Checkbutton(middle_frame_1, text="Color Infrared (3 Band)", var=type_value, onvalue="CIR", offvalue="")
type_7 = tk.Checkbutton(middle_frame_1, text="Natural Color (3 Band)", var=type_value, onvalue="NC", offvalue="")
type_8 = tk.Checkbutton(middle_frame_1, text="Natural Color/Color Infrared (4 Band)", var=type_value, onvalue="NC-CIR", offvalue="")
type_9 = tk.Checkbutton(middle_frame_1, text="Black & White (1 Band)", var=type_value, onvalue="BW", offvalue="")
type_10 = tk.Checkbutton(middle_frame_1, text="Map", var=type_value, onvalue="MAP", offvalue="")
type_list = [type_1, type_2, type_3, type_4, type_5, type_6, type_7, type_8, type_9, type_10]
# for loop to pack all check boxes
for type in type_list:
    type.configure(font=('Courier', 11))
    type.pack(fill='both')

# area type check box variables
area_value = tk.StringVar()
area_value.set("")
area_1 = tk.Checkbutton(middle_frame_2, text="state", var=area_value, onvalue="state", offvalue="")
area_2 = tk.Checkbutton(middle_frame_2, text="county", var=area_value, onvalue="county", offvalue="")
area_3 = tk.Checkbutton(middle_frame_2, text="quad", var=area_value, onvalue="quad", offvalue="")
area_4 = tk.Checkbutton(middle_frame_2, text="qquad", var=area_value, onvalue="qquad", offvalue="")
area_list = [area_1, area_2, area_3, area_4]
# for loop to pack all check boxes
for area in area_list:
    area.configure(font=('Courier', 11))
    area.pack(fill='both')

# Progress bar widget
progress = Progressbar(middle_frame_3, orient='horizontal')
progress.pack(fill='both', pady=10)
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
message_area_1.pack(fill='both')
message_area_2.pack(fill='both')
message_area_3.pack(fill='both')

# function to make requests to api.tnris.org resources endpoint to download data
def bulk_download():
    # variables
    error_message.set("")
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
    a = area_value.get()

    # assign data variable based on checkbox selections (build the url string requests needs to get data from rest endpoint)
    if not t and not a:
        # if no selections made, build url string to get all resources for that collection id
        print('no selections made')
        data = requests.get(base_url + id_query + c).json()
    elif t and a:
        # if both type and area selections made, build the url string
        print('both area and type selections made. type = {} and area = {}'.format(t,a))
        '''
        future enhancement to add and handle multiple selections for both type and area
        '''
        data = requests.get(base_url + id_query + c + type_abbr_query + t + area_query + a).json()
    elif t and not a:
        # if type selection made but not area, build the url string
        print('type selections made. type = {}'.format(t))
        '''
        future enhancement to add and handle multiple selections for type only
        '''
        data = requests.get(base_url + id_query + c + type_abbr_query + t).json()
    elif a and not t:
        # if area selection made but not type, build the url string
        print('area selections made. area = {}'.format(a))
        '''
        future enhancement to add and handle multiple selections for area only
        '''
        data = requests.get(base_url + id_query + c + area_query + a).json()

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
                open('data/{}'.format(obj['resource'].rsplit('/', 1)[-1]), 'wb').write(file.content)
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
        print("ERROR. No resource results. Please double check your collection id string or any filters applied.")
        error_message.set("ERROR. No resource results. Please double check your collection id string or any filters applied.")
        # make sure message is updated
        middle_frame_4.update_idletasks()

get_data = tk.Button(bottom_frame, text="Get Data", command=bulk_download, bg="#009933", fg="white", activebackground="green", activeforeground="white")
get_data.pack(pady=20)

window.mainloop()
