import requests
# from tkinter import *
import tkinter as tk

# master/parent window contains all gui elements
window = tk.Tk()
window.title("TNRIS DataHub Bulk Download Utility")
window.geometry()

# frame variables - parent is window
top_frame = tk.Frame(window, borderwidth=20)
middle_frame_1 = tk.Frame(window, borderwidth=20)
middle_frame_2 = tk.Frame(window, borderwidth=20)
bottom_frame = tk.Frame(window, borderwidth=20)
frame_list = [top_frame, middle_frame_1, middle_frame_2, bottom_frame]
# for loop to pack all frames
for frame in frame_list:
    frame.pack()

# label variables
label_1 = tk.Label(top_frame, text="Enter Collection ID: ")
label_2 = tk.Label(middle_frame_1, text="Select the resource types you want to download")
label_3 = tk.Label(middle_frame_1, text="(You must select at least one)")
# label_4 = tk.Label(bottom_frame, text="Bulk Download Utility Messages: ")
label_list = [label_1, label_2, label_3]
# for loop to pack all labels
for label in label_list:
    label.pack()

# collection id entry
collection_id = tk.Entry(top_frame, width=40)
collection_id.pack()
collection_id.focus()

# print messages from the bulk_download function
# display_message = tk.StringVar()
# display_message.set("Messages appear here to provide feedback and show the progress of your download.")
# message_area = tk.Label(bottom_frame, textvariable=display_message)
# message_area.pack()

# check box variables
# type_1 = tk.Checkbutton(middle_frame_1, text="Lidar Point Cloud")
# type_2 = tk.Checkbutton(middle_frame_1, text="Hypsography")
# type_3 = tk.Checkbutton(middle_frame_1, text="Digital Elevation Model")
# type_4 = tk.Checkbutton(middle_frame_1, text="Land Cover")
# type_5 = tk.Checkbutton(middle_frame_1, text="Vector")
# type_6 = tk.Checkbutton(middle_frame_1, text="Natural Color/Color Infrared (4 Band)")
# box_list = [type_1, type_2, type_3, type_4, type_5, type_6]
# for loop to pack all check boxes
# for box in box_list:
#     box.pack()

# list box variables
list_box = tk.Listbox(middle_frame_1)
list_box.insert(1, "Lidar Point Cloud (LPC)")
list_box.insert(2, "Hypsography (HYPSO)")
list_box.insert(3, "Digital Elevation Model (DEM)")
list_box.insert(4, "Land Cover")
list_box.insert(5, "Vector")
list_box.insert(6, "Natural Color/Color Infrared (4 Band) Imagery")
list_box.pack()


# function to make requests to api.tnris.org resources endpoint to download data
def bulk_download():
    # variables
    base_url = "https://api.tnris.org/api/v1/resources/"
    id_query = "?collection_id="
    type_query = "&resource_type_name="
    type_abbr_query = "&resource_type_abbreviation="
    area_query = "&area_type="
    count = 0

    # get data from api.tnris.org rest endpoint for datahub resources
    data = requests.get(base_url + id_query + collection_id.get()).json()

    # loop through all object resources for a collection id and save them to file using same name as s3 .zip name
    if data['count'] > 0:
        # show user how many collection resources returned from query
        # print(str(data['count']) + " resources found for tnris collection id {}.".format(collection_id.get()))
        api_count = str(data['count'])
        print(api_count + " resources found for tnris collection id")

        for obj in data['results']:
            try:
                # check if resource type check boxes are checked first
                # for box in box_list:
                #     if box.state('selected'):
                #         print(box.text())
                print("downloading resource id: {}".format(obj["resource_id"]))
                # print("resource download in progress...")
                file = requests.get(obj["resource"])
                open('data/{}'.format(obj['resource'].rsplit('/', 1)[-1]), 'wb').write(file.content)
                count += 1
                print("file download success!")
                # display_message.set("file download success")
            except requests.ConnectionError:
                print("requests connection error")
            except requests.ConnectTimeout:
                print("requests timeout error")
    else:
        print("There was an error with the DataHub collection id string or there were no resources for the collection id. Please try again.")

    print("script process complete. {} out of {} resource(s) successfully downloaded.".format(count, api_count))


btn_1 = tk.Button(bottom_frame, text="Get Data!", command=bulk_download, bg="green", fg="white", activebackground="#009933", activeforeground="white")
btn_1.pack()

window.mainloop()
