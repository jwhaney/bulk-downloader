import requests

# variables
base_url = "https://api.tnris.org/api/v1/resources/"
base_query = "?collection_id="
count = 0

# prompt user for a tnris collection id
collection_id_string = input("Enter TNRIS collection id: ")

# get data from api.tnris.org rest endpoint for datahub resources
data = requests.get(base_url + base_query + collection_id_string).json()

# show user how many collection resources returned from query
print(str(data['count']) + " resources found for tnris collection id {}.".format(collection_id_string))

# loop through all object resources for a collection id and write them to .zip file
# file name used is same as from s3 url
for obj in data['results']:
    try:
        print("downloading resource id: {}".format(obj["resource_id"]))
        file = requests.get(obj["resource"])
        open('data/{}'.format(obj['resource'].rsplit('/', 1)[-1]), 'wb').write(file.content)
        count += 1
        print("file download success!")
    except requests.ConnectionError:
        print("requests connection error")
    except requests.ConnectTimeout:
        print("requests timeout error")

print("script process complete. {} out of {} resource(s) successfully downloaded.".format(count, data['count']))
