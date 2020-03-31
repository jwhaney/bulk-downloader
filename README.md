# bulk-downloader
__bulk download tnris datahub collection resources__

Steps:
1. Create a local project directory for this script and the requirements file. Example: create a new folder on your desktop or somewhere called tnris-bulk-downloader and put the files in there.
2. Optional - create a virtual environment for the bulk-downloader to isolate the requirements.
3. Open terminal and cd into your project folder - `cd tnris-bulk-downloader`
4. run `pip install requirements.txt`
5. run `python3 bulk-downloader.py`
6. paste the tnris datahub collection id you want to bulk download data for when the script prompts you for it.
  - to find the collection id you want, go to data.tnris.org and find the dataset
  - when you find it, look in your browser url window and copy the last part of the url after `collection/`
      - example datahub collection url: https://data.tnris.org/collection/a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2
      - in the url example above, copy `a8ef3bfc-1e26-4fba-9abe-1b86ecd594e2` to use in this script
7. hit enter and go get a beer cuz it might be a while...
