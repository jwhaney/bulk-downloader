# bulk-downloader
__bulk download tnris datahub collection resources__

Steps:
1. Hit the green 'Clone or Download' button in this repo (upper right side)
2. Click Download ZIP
3. Create a local project directory to extract the repo files. Example: create a new folder on your desktop or somewhere called tnris-bulk-downloader and unzip the files in there.
4. Optional - create a virtual environment for the bulk-downloader to isolate the requirements.
5. Open terminal and cd into your project folder - `cd tnris-bulk-downloader`
6. run `pip install requirements.txt`
7. run `python3 bulk-downloader.py`
8. paste the tnris datahub collection id you want to bulk download data for when the script prompts you for it.
    - to find the collection id you want, go to data.tnris.org and find the dataset
    - when you find it, look in your browser url window and copy the last part of the url after `collection/`
      - example datahub collection url: https://data.tnris.org/collection/a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2
      - in the url example above, copy `a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2` to use in this script
9. hit enter and go get a beer cuz it might be a while...
