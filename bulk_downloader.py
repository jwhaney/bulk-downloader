import requests

base = "https://api.tnris.org/api/v1/resources"
query_base = "?collection_id="

collection = input("Enter TNRIS collection id: ")

data = requests.get(base + query_base + collection).json()

print(str(data['count']) + " resources found for tnris collection id {}.".format(collection))

for obj in data['results']:
    print("downloading resource id {}".format(obj["resource_id"]))
    file = requests.get(obj["resource"])
    open('{}.zip'.format(obj["resource_id"]), 'wb').write(file.content)
    print("finished downloading file")
