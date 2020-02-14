from class_storage import SharepointConnector

url = "http://sharepoint/"
domain = "hsi"
username = "jjacinto"
password = "?kouLunakomo87"
connection = SharepointConnector(url, domain, username, password)

pageRequest = connection.request_page("operations/solar/Shared%20Documents/Forms/AllItems.aspx")
connection.request
import pdb; pdb.set_trace()
