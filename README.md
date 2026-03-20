# Taking-a-file-and-uploading-it-from-one-to-another-database


This automation is built with Selenium and the pyairtable library (mainly). The main idea is to take a file from a database, create a phone book (plus sme other things inside the other database we’re using). For these purposes, we are going to upload our Airtable, because Airtable APi key is easier to set up rather then Googe drive, which needs OAuth2 verification, and it is easier to work with Airtable in a general sense. We’ll need only one function where we’ll do everything since the script isn’t that complex.

How are we going to determine which files to download and which not in our Airtable? We’ll use a checkbox. If the checkbox is not checked, this means the files must be downloaded. When the file is downloaded, we check the checkbox.

First step, we import the libraries we’ll need. Second step, we create 4 constant variables for our URL and Airtable credentials.

In our fetch_and_upload function, we start our Chrome (using headless chrome options so we don’t open the browser window on our computer)-> create a api and a table to be able to get the records we want by formula -> we loop through the records we found and open the Second Database url where we’ll be uploading the files with driver -> we wait for 2 second for the full content of the page to load -> then we want to get all the files from our Attachments Collumn in Airtable -> then we loop through it incase there are multiple files in one field -> so we know that when we fetch a file from Airtable via API it come swith multiple json properties ->  then we extract the downloads url and the original filename -> then we simply sends an HTTP GET request to that URL, just like when your browser visits a webpage -> In this case the URL is the Airtable file link, so instead of getting HTML back you get the raw file content (bytes), with this line we hold them into a veriable response = requests.get(url) -> to upload a file, we need to have it locally on our machine somewhere, but we don’t need it actually in the long-term after we upload where we want, so we will store it in a temporary address in our OS temp folder and delete it later -> for this we need to create a file in our OS temp folder -> then we pour the downloaded bytes into that file with the .write method from the file library -> then we save the full path of the file into a veriable, cause ones we exit the with block the file closes and tmp is not longer accessable -> then we check our checkbox -> (really import is to delete the file after our script execute - os.remove(tmp_path)

For uploading the files into the database we are using, we’ll follow this path (sorry for not providing a screen recording from the actual platform):

Path -> Sign In first -> Phone book -> new book -> County -US ; name - file_name -> import phones -> exel csv -> uploading -> next -> next -> finish

The main structure of the whole selenium automation is this. First step, we log in to the platform once (not every time we proceed with the file, cause there is no point since the browser saves the session). Then we use a simple Wait till an element appears all the way to the end. When we finish with the last step, we check the checkbox for that file in Airtable, remove the file from our temp OS folder, and reload the platform dashboard. We wrap everything in a try/except cause if one file fails to not break our entire automation, but just continues to the next file

Tricks used:

- inputting the credentials for the login page so we don’t have to log in every time
- saving the file into a temp folder in our OS and then deleting it
- reopens the browser dashboard at the end of the script, so we use the session ID from the browser
- using an error handling to prevent the whole script from crashing, instead, skip to the next file
- using a checkbox to determine which file to take instead of the date created
