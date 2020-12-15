# bulk-downloader
### __bulk download tnris datahub collection resources__

### description
the bulk downloader utility uses the publicly available tnris api rest endpoint for datahub resources (https://api.tnris.org/api/v1/resources). the rest endpoint feeds amazon web services (aws) s3 url links for compressed data to the tnris datahub (https://data.tnris.org) web application. this utility allows bulk download of a datahub collection's resources, bypassing the need to click each area polygon in the download map.

<img src="/resources/bulk-downloader.png" width="500">

## recommendation
it is recommended, especially if you plan to download large collections/datasets such as lidar, that you save the data in a location that has plenty of disk/storage space. an external hard drive is ideal. however, if you'd like to store the data locally on your computer, just be sure you have enough disk/storage space before you run this utility. otherwise, you may encounter errors that the program does not anticipate.

additionally, this utility is dependent on a solid internet connection. if you experience issues, it could be due to your internet connection speed.

## setup

### setup option 1 - find and download the executable for your operating system

1. the `exe/` directory contains pre-built and compressed/zipped executables for each main operating system (linux, mac, windows).
2. download the .zip file that most closely applies to your operating system.
3. once you've downloaded the executable .zip, you will need to extract the project files from the zip file (should be in your *Downloads* folder or similar).
4. navigate inside the directory you just unzipped, then into __*dist/bulk_downloader/*__ which is where the executable file exists called __*bulk_downloader*__ .
    - there are a lot of files inside this directory, and depending on which executable you download, it might not be immediately obvious which file to use.
    - find the file called __*bulk_downloader*__ that has a file size of about __*1.7MB*__ .
5. double click the executable file to run the utility on your system.

**Important Note**: do not move the executable file from its native location in the project. this might either corrupt the application or make it not work at all. instead, you can create a shortcut if you like that links to the executable file in this project. that shortcut can reside on your desktop or wherever. here are some resources that might help with the process:

__create a shortcut on__ [Windows 10](https://www.minitool.com/news/create-desktop-shortcut-windows-10-004.html), [macos Catalina](https://www.igeeksblog.com/how-to-make-desktop-shortcuts-on-mac/), or [Linux/Ubuntu](https://itsfoss.com/ubuntu-desktop-shortcut/)


-------------------------------


### setup option 2 - setup local environment and run the utility from the terminal

1. hit the green *Clone or Download* button in this repo (upper right side). if you are already familiar with git and gitHub, then just clone the repo to local and skip to #4.
2. click *Download ZIP*. you will need to extract the downloaded .zip file to where you want your project to reside. the downloaded .zip file will be called __bulk-downloader-master.zip__.
3. __*optional*__ - create a python 3 virtual environment for the bulk-downloader to isolate the requirements/python packages.
4. open terminal and cd into your project source code folder - `cd bulk-downloader/src`
5. run `pip3 install -r requirements.txt`
    - if you've created a python 3 virtual environment (step #3) then run `pip install -r requirements.txt`
6. run `python3 bulk_downloader.py` to start the script utility.
    - if you've created a python 3 virtual environment (step #3) then run `python bulk_downloader.py`

__note__: if you encounter an error regarding tkinter (Tk) not being installed, such as

`ModuleNotFoundError: No module named 'tkinter'`

then follow the instructions at the url below.

https://tkdocs.com/tutorial/install.html

-------------------------------


## instructions

1. you should now see a graphical user interface (gui). paste the tnris datahub collection id you want to bulk download data for at the top.
    - to find the collection id you want, go to data.tnris.org and find the dataset
    - when you find it, look in your browser url window and copy the last part of the url after `collection/`
      - example datahub collection url: https://data.tnris.org/collection/a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2
      - in the url example above, copy `a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2` to use in this script
2. click the 'Browse' button to browse to a location on your computer or on an external drive to save the downloaded data.
3. __*optional*__ - use the resource type filter if you would like to narrow down the amount of files that will be downloaded per collection.
    - **resource type filter:** filters the collection by only the type of data that is checked. so if you check Hypsography, you will only receive the Hypsography resources for that collection. at this time, only one resource type filter can be applied at one time.
    - **note** - it is important to be familiar with what resource types are available for any one collection. some collections only have one resource type, such as vector datasets like address points or parcels. if you attempt to filter by a resource type that doesn't exist for that collection, you will receive a message telling you there was a problem.
        - you can find the resource type information by visiting the datahub collection and clicking an area type polygon in the download map which will then list the types of data available for download. the types will vary depending on the collection.
        - __*example*__: a lot of lidar collections/datasets have Digital Elevation Models, Lidar Point Clouds, & Hypsography resource types for each area. so, if you download an entire collection you will receive all three of those types for each area of the collection. if there are 17 areas for the collection, 17 x 3 resource types = 51 resources downloaded if no resource type filter applied.
4. click the **Get Data** button and let the script/utility do its thing.
    - depending on the number of resources and the size of those resources, the batch download process could take some time so please be patient.
    - it may be beneficial for large datasets like lidar, to download each resource type one by one (ie. Hypsography first, then DEMs, then LPCs.)
    - if you feel like there is an issue, or the utility is not working, you can **Stop** the bulk downloader at any time by hitting the **Stop** button and then confirming that you want to stop the bulk download process.
        - only do this if you truly want to stop the process because you cannot resume at the same point that you stopped. the program will have to restart at the beginning.


-------------------------------


### requirements

this project was built on __linux mint 19__ using __python 3.6.9__ and the __tkinter__ gui library

- altgraph==0.17
- certifi==2019.11.28
- chardet==3.0.4
- idna==2.9
- PyInstaller==3.6
- requests==2.23.0
- urllib3==1.25.8


-------------------------------


### executables

executable files were built on the native operating system using [PyInstaller](https://www.pyinstaller.org/) version 3.6. the specific operating system version that these executables were built on is listed in the executable .zip file name within the /exe directory.

__*if you do not see the correct version of your operating system listed in the pre-built executables provided in this code repository, please attempt to use the one most similar to your system, or you can build your own using the instructions below:*__

##### run these commands in the terminal/command prompt to build your own os specific executable files:
1. `git clone https://github.com/jwhaney/bulk-downloader.git`
2. *optional* - create a python virtual environment for this project
3. `cd bulk-downloader`
4. `pip install -r src/requirements.txt`
5. `pyinstaller src/bulk_downloader.py`
6. navigate to ./dist/bulk_downloader/bulk_downloader and double-click the file to run the utility


-------------------------------


### resources

here is a list of some resources that may help with the setup and use of this utility:

- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
- [Full Stack Python](https://www.fullstackpython.com/best-python-resources.html)
- [Official Python 3.6 Docs](https://docs.python.org/3.6/)
- [More official Python documentation](https://www.python.org/doc/)
