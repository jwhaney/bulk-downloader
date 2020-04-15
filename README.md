# bulk-downloader
### __bulk download tnris datahub collection resources__

#### Description:
The bulk downloader utility uses the TNRIS API Resource REST endpoints (https://api.tnris.org/api/v1/resources) which feeds data to the TNRIS DataHub (https://data.tnris.org) application. This utility allows bulk download of a collection's resources bypassing the need to click each area type (county, quad, qquad) polygon in the DataHub collection download map.

#### Instructions:
1. Hit the green 'Clone or Download' button in this repo (upper right side)
2. Click Download ZIP
3. Create a local project directory to extract the repo files. Example: create a new folder on your desktop or somewhere called tnris-bulk-downloader and unzip the files in there.
4. *Optional* - create a virtual environment for the bulk-downloader to isolate the requirements.
5. Open terminal and cd into your project folder - `cd tnris-bulk-downloader`
6. Run `pip install -r requirements.txt`
7. Run `python3 bulk_downloader.py`
8. You should now see a graphical user interface (gui). Paste the tnris datahub collection id you want to bulk download data for at the top.
    - to find the collection id you want, go to data.tnris.org and find the dataset
    - when you find it, look in your browser url window and copy the last part of the url after `collection/`
      - example datahub collection url: https://data.tnris.org/collection/a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2
      - in the url example above, copy `a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2` to use in this script
9. *Optional* - use the resource type or area filter if you like to narrow down the amount of files that will be downloaded per collection. at this time, only one resource type filter and one area filter can be applied at one time.
    - **Resource Type Filter:** filters the collection by only the type of data that is checked. So if you check Hypsography, you will only receive the Hypsography resources for that collection.
    - **Area Type Filter:** filters the collection by the area type, if there are more than one available. A lot of collections only have one area type so you should be familiar with the collection
      before you use this filter or else you will receive an error.
    - **Note** - it is important to be familiar with what resource and area types are available for any one collection.
      - you can find the resource type information by visiting the datahub collection and clicking an area type in the download map which will then list the types of data available for download. the types will vary depending on the collection.
      - *Example*: most all lidar collections have Digital Elevation Models, Lidar Point Clouds, & Hypsography resource types for each area. So, if you download an entire collection
        you will receive all three of those files for each area of the collection.
10. Hit enter and let the script do its thing.
    - depending on the number of resources and the size of those resources, the batch download process could take some time so please be patient.
    - **Important**: all data will be downloaded into the */data* directory of this project.
