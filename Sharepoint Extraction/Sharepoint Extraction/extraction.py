from class_storage import SharepointConnector

connection = SharepointConnector("http://sharepoint/",
                                 "hsi.int",
                                 "jjacinto",
                                 "?kouLunakomo87")

base_directory = "default.aspx"
print(connection.request_page(base_directory))

