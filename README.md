# bulk-downloader
### __bulk download tnris datahub collection resources__

#### description:
The bulk downloader utility uses the TNRIS API REST endpoint for DataHub resources (https://api.tnris.org/api/v1/resources) which feeds AWS S3 url links for data to the TNRIS DataHub (https://data.tnris.org) application. This utility allows bulk download of a collection's resources, bypassing the need to click each area type (county, quad, qquad) polygon in the download map.

<img src="/resources/bulk-downloader-linux.png" width="500">

### instructions
#### option 1 - setup local environment and run the utility from the terminal

1. hit the green *Clone or Download* button in this repo (upper right side). if you are already familiar with git and gitHub, then just clone the repo to local and skip to #4.
2. click *Download ZIP*. you will need to extract the downloaded .zip file to where you want your project to reside. the downloaded .zip file will be called __bulk-downloader-master.zip__.
3. __*optional*__ - create a virtual environment for the bulk-downloader to isolate the requirements.
4. open terminal and cd into your project folder - `cd tnris-bulk-downloader`
5. run `pip install -r requirements.txt`
6. run `python3 bulk_downloader.py`
7. you should now see a graphical user interface (gui). paste the tnris datahub collection id you want to bulk download data for at the top.
    - to find the collection id you want, go to data.tnris.org and find the dataset
    - when you find it, look in your browser url window and copy the last part of the url after `collection/`
      - example datahub collection url: https://data.tnris.org/collection/a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2
      - in the url example above, copy `a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2` to use in this script
8. click the 'Browse' button to browse to a location on your computer or on an external drive to save the downloaded data.
9. __*optional*__ - use the resource type filter if you would like to narrow down the amount of files that will be downloaded per collection. at this time, only one resource type filter can be applied at one time.
    - **resource type filter:** filters the collection by only the type of data that is checked. so if you check Hypsography, you will only receive the Hypsography resources for that collection.
    - **note** - it is important to be familiar with what resource types are available for any one collection. some collections only have one resource type, such as vector datasets like address points or parcels. if you attempt to filter by a resource type that doesn't exist for that collection, you will receive a message telling you there was a problem.
      - you can find the resource type information by visiting the datahub collection and clicking an area type polygon in the download map which will then list the types of data available for download. the types will vary depending on the collection.
      - __*example*__: most all lidar collections have Digital Elevation Models, Lidar Point Clouds, & Hypsography resource types for each area. so, if you download an entire collection you will receive all three of those types for each area of the collection.
10. click the **Get Data** button and let the script do its thing.
    - depending on the number of resources and the size of those resources, the batch download process could take some time so please be patient.
    - it may be beneficial for large datasets like lidar, to download each resource type one by one (ie. Hypsography first, then DEMs, then LPCs.)
