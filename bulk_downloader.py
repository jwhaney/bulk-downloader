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
    # label.grid(column=0, row=0)

# collection id entry
collection_id = tk.Entry(top_frame, width=45, font=('Courier', 11))
collection_id.pack()
# collection_id.grid(column=0, row=0)
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
    # type.grid(column=0, row=0)

# area type check box variables
# area_value = tk.BooleanVar()
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
    # area.grid(column=0, row=0)

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
# def kill():
#     display_message.set("killing process...")
#     print("killing process...")
#     time.sleep(2)
#     window.destroy()

# function to make requests to api.tnris.org resources endpoint to download data
def bulk_download():
    # variables
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
    # if no selections made, build url string to get all resources for that collection id
    if not t and not a:
        print('no selections made')
        data = requests.get(base_url + id_query + c).json()
    # if both type and area selections made, build the url string
    elif t and a:
        print('both area and type selections made. type = {} and area = {}'.format(t,a))
        # need to handle here if there area multiple selections made for both type and area

        # if both area and type selected then combine all of it into data request
        data = requests.get(base_url + id_query + c + type_abbr_query + t + area_query + a).json()
    # if type selection made but not area, build the url string
    elif t and not a:
        print('type selections made. type = {}'.format(t))
        # need to handle here if multiple type selections made but no area selections

        data = requests.get(base_url + id_query + c + type_abbr_query + t).json()
    # if area selection made but not type, build the url string
    elif a and not t:
        print('area selections made. area = {}'.format(a))
        # need to handle here if multiple area selections made but no type selections

        data = requests.get(base_url + id_query + c + area_query + a).json()

    # api data variables - string and integer
    api_str_count = str(data['count'])
    api_num_count = data['count']

    print(api_str_count + " number of resources found!!!!!")

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
                progress_value = round((count/api_num_count)*100,1)
                print(str(progress_value) + "%")
                # feed new progress value into p_bar function to update gui
                p_bar(progress_value)
                # show display message as progress percentage string
                display_message.set(str(progress_value) + "%")
            except requests.ConnectionError:
                print("requests connection error")
                display_message.set("requests connection error")
            except requests.ConnectTimeout:
                print("requests timeout error")
                display_message.set("requests timeout error")
    else:
        display_message.set("There was an error with the DataHub collection id string or there were no resources for that collection id. Please try again.")

    print("Script process completed. {} out of {} resource(s) successfully downloaded.".format(count, api_str_count))
    display_message.set("Script process completed. {} out of {} resource(s) successfully downloaded.".format(count, api_str_count))


tk.Button(bottom_frame_left, text="Start", command=bulk_download, bg="#009933", fg="white", activebackground="green", activeforeground="white").pack()
# tk.Button(bottom_frame_right, text="Stop", command=window.quit, bg="#ff4d4d", fg="white", activebackground="red", activeforeground="white").pack()

window.mainloop()
