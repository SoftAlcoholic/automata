from config import *
import xmlrpc.client
import xml.etree.ElementTree as ET

# Set the URL of the XML-RPC endpoint
url = "http://192.168.0.39/pagab/w/xmlrpc.php"

# Set the username and password for authentication
username = WORDPRESS_USER
password = WORDPRESS_TKN

# Create a server object using the XML-RPC endpoint URL
server = xmlrpc.client.ServerProxy(url)

# Set the post content
post_content = "This is the content of my new post."

# Set the post title
post_title = "My New Post Title"

# Set the post category
post_category = "Uncategorized"

# Set the post status
post_status = "publish"

# Create a dictionary with the post data
post_data = {
    "post_title": post_title,
    "post_content": post_content,
    "post_category": [post_category],
    "post_status": post_status
}

# Call the wp_insert_post() function to create the post
try:
    post_id = server.wp.newPost(0, post_data, username, password)
    xml_data = server.system.methodHelp('wp.newPost')
    root = ET.fromstring(xml_data)
    print(ET.dump(root))
    print("New post created with ID:", post_id)
except xmlrpc.client.ProtocolError as error:
    print("Error:", error.errmsg)
    print("Response:", error.response) # print out the response from the server
except xmlrpc.client.Fault as error:
    print("Error:", error.faultString)
    print("Response:", error.faultCode) # print out the fault code from the server
except Exception as error:
    print("Error:", error)
