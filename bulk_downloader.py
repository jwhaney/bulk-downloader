import requests
import tkinter as tk
from tkinter.ttk import Progressbar
# import tkinter.ttk as ttk
import time, sys

# master/parent window contains all gui elements
window = tk.Tk()
window.title("TNRIS DataHub Bulk Download Utility")

# frame variables - parent is window
top_frame = tk.Frame(window, borderwidth=20)
middle_frame_1 = tk.Frame(window, borderwidth=20, bg="red")
middle_frame_2 = tk.Frame(window, borderwidth=20, bg="green")
middle_frame_3 = tk.Frame(window, borderwidth=20)
middle_frame_4 = tk.Frame(window, borderwidth=20)
bottom_frame_master = tk.Frame(window, borderwidth=20)
bottom_frame_left = tk.Frame(bottom_frame_master, bg='yellow')
bottom_frame_right = tk.Frame(bottom_frame_master, bg='blue')
frame_list = [top_frame, middle_frame_1, middle_frame_2, middle_frame_3, middle_frame_4, bottom_frame_master, bottom_frame_left, bottom_frame_right]
# for loop to pack all frames
for frame in frame_list:
    frame.pack(fill='both')

# label variables
label_1 = tk.Label(top_frame, text="Enter a TNRIS DataHub Collection ID: ")
label_2 = tk.Label(middle_frame_1, text="**Optional: Select the resource type(s) you want to download from the Collection ID entered.")
label_3 = tk.Label(middle_frame_1, text="If no selection made, all resources for the collection will be downloaded.")
label_4 = tk.Label(middle_frame_2, text="**Optional: Select a resource area type.")
label_5 = tk.Label(middle_frame_2, text="If no selection made, the largest area type for the provided collection will be chosen.")
# label_6 = tk.Label()
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
type_value = tk.BooleanVar()
# type_value = tk.StringVar()
# type_value.set(False)
type_1 = tk.Checkbutton(middle_frame_1, text="Lidar Point Cloud")
type_2 = tk.Checkbutton(middle_frame_1, text="Hypsography")
type_3 = tk.Checkbutton(middle_frame_1, text="Digital Elevation Model")
type_4 = tk.Checkbutton(middle_frame_1, text="Land Cover")
type_5 = tk.Checkbutton(middle_frame_1, text="Vector")
type_6 = tk.Checkbutton(middle_frame_1, text="Natural Color/Color Infrared (4 Band)")
type_list = [type_1, type_2, type_3, type_4, type_5, type_6]
# for loop to pack all check boxes
for type in type_list:
    type.configure(font=('Courier', 11))
    type.pack(fill='both')

# area type check box variables
area_value = tk.BooleanVar()
# area_value = tk.StringVar()
# area_value.set(False)
area_1 = tk.Checkbutton(middle_frame_2, text="state")
area_2 = tk.Checkbutton(middle_frame_2, text="county")
area_3 = tk.Checkbutton(middle_frame_2, text="quad")
area_4 = tk.Checkbutton(middle_frame_2, text="qquad")
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
display_message = tk.StringVar()
display_message.set("Messages here provide download progress feedback.")
message_area = tk.Label(middle_frame_4, textvariable=display_message, font=('Courier', 10))
message_area.pack(fill='both')

# kill function
def kill():
    display_message.set("killing process...")
    print("killing process...")
    time.sleep(2)
    window.destroy()

# function to make requests to api.tnris.org resources endpoint to download data
def bulk_download():
    # variables
    base_url = "https://api.tnris.org/api/v1/resources/"
    id_query = "?collection_id="
    type_query = "&resource_type_name="
    type_abbr_query = "&resource_type_abbreviation="
    area_query = "&area_type="
    count = 0
    progress_value = 0
    c = collection_id.get()

    # get data from api.tnris.org rest endpoint for datahub resources
    data = requests.get(base_url + id_query + collection_id.get()).json()
    # api data variables - string and integer
    api_str_count = str(data['count'])
    api_num_count = data['count']

    # progress bar function
    def p_bar(value):
        progress['value'] = value
        middle_frame_3.update_idletasks()

    # loop through all object resources for a collection id and save them to file using same name as s3 .zip name
    # also update progress bar feedback for user to see progress
    if data['count'] > 0:
        # show user how many collection resources returned from query
        print('should see resource count here')
        print(api_str_count + " resources found for tnris collection id " + c)
        display_message.set(api_str_count + " resources found for tnris collection id " + c)
        print('sleeping for 2 secs')
        time.sleep(2)
        # set message to tell user download progress started
        display_message.set("resource download(s) in progress...")

        for obj in data['results']:
            try:
                print("downloading resource id: {}".format(obj['resource'].rsplit('/', 1)[-1]))
                # assign next object['resource'] url to file variable
                file = requests.get(obj["resource"], stream=True)
                # write file variable to actual local file to this projects data directory
                open('data/{}'.format(obj['resource'].rsplit('/', 1)[-1]), 'wb').write(file.content)
                count += 1
                # update progress_value variable by dividing new count number by total api object count
                progress_value = round((count/api_num_count)*100,0)
                print(round((count/api_num_count)*100,1))
                # feed new progress value into p_bar function to update gui
                p_bar(progress_value)
            except requests.ConnectionError:
                print("requests connection error")
            except requests.ConnectTimeout:
                print("requests timeout error")
    else:
        display_message.set("There was an error with the DataHub collection id string or there were no resources for that collection id. Please try again.")

    print("Script process completed. {} out of {} resource(s) successfully downloaded.".format(count, api_str_count))
    display_message.set("Script process completed. {} out of {} resource(s) successfully downloaded.".format(count, api_str_count))


tk.Button(bottom_frame_left, text="Start", command=bulk_download, bg="#009933", fg="white", activebackground="green", activeforeground="white").pack()
tk.Button(bottom_frame_right, text="Stop", command=window.quit, bg="#ff4d4d", fg="white", activebackground="red", activeforeground="white").pack()

window.mainloop()
