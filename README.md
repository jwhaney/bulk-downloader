# bulk-downloader
### __bulk download tnris datahub collection resources__

#### Description:
The bulk downloader utility uses the TNRIS API REST endpoint for DataHub resources (https://api.tnris.org/api/v1/resources) which feeds AWS S3 url links for data to the TNRIS DataHub (https://data.tnris.org) application. This utility allows bulk download of a collection's resources, bypassing the need to click each area type (county, quad, qquad) polygon in the download map.

![TNRIS DataHub Bulk Downloader Utility](/resources/bulk-downloader-linux.png)

#### Instructions:
1. Hit the green 'Clone or Download' button in this repo (upper right side)
2. Click Download ZIP
3. Create a local project directory to extract the repo files. Example: create a new folder on your desktop or somewhere called tnris-bulk-downloader and unzip the files in there.
4. *Optional* - create a virtual environment for the bulk-downloader to isolate the requirements.
5. Open terminal and cd into your project folder - `cd tnris-bulk-downloader`
6. Run `pip install -r requirements.txt`
7. Run `python3 bulk_downloader.py`
8. You should now see a graphical user interface (gui). Paste the tnris datahub collection id you want to bulk download data for at the top.
    - To find the collection id you want, go to data.tnris.org and find the dataset
    - When you find it, look in your browser url window and copy the last part of the url after `collection/`
      - example datahub collection url: https://data.tnris.org/collection/a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2
      - In the url example above, copy `a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2` to use in this script
9. Click the 'Browse' button to browse to a location on your computer or on an external drive to save the downloaded data.
10. *Optional* - Use the resource type filter if you would like to narrow down the amount of files that will be downloaded per collection. At this time, only one resource type filter can be applied at one time.
    - **Resource Type Filter:** Filters the collection by only the type of data that is checked. So if you check Hypsography, you will only receive the Hypsography resources for that collection.
    - **Note** - It is important to be familiar with what resource types are available for any one collection. Some collections only have one resource type, such as vector datasets like address points or parcels. If you attempt to filter by a resource type that doesn't exist for that collection, you will receive a message telling you there was a problem.
      - You can find the resource type information by visiting the DataHub collection and clicking an area type polygon in the download map which will then list the types of data available for download. The types will vary depending on the collection.
      - *Example*: Most all lidar collections have Digital Elevation Models, Lidar Point Clouds, & Hypsography resource types for each area. So, if you download an entire collection
        you will receive all three of those types for each area of the collection.
11. Click the 'Get Data' button and let the script do its thing.
    - Depending on the number of resources and the size of those resources, the batch download process could take some time so please be patient.
    - It may be beneficial for large datasets like lidar, to download each resource type one by one (ie. Hypsography first, then DEMs, then LPCs.)
