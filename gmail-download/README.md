gmail-download
=====================

<code>gmail.py</code> - This script came about after working on a client project where preview links were needed from actual deployed emails for client to review. After spending quite a bit of time manually creating previews, I decided I needed to automate the process. Hence this quickly cobbled Python script, extended from the sample code from Google's Python QuickStart guide for the Gmail API (https://developers.google.com/gmail/api/quickstart/python). This script will download the HTML version of emails from a specific sender, using OAuth connect to your Gmail account. Query details for the emails can be provided as a parameter through the command line (see below). Note: This script is only set with scope persmission to read emails.

## Requirements:
- Python 3.x - make sure you have the Google API client modules installed. Script has not been tested on Python 2.x
  - Run: <code>pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib</code>
- credentials.json - placed in the same folder as the script
  - This script requires a Google Cloud Console project with Gmail API library enabled. You will need to create an OAuth Client ID in your Cloud project and download the JSON file. 

## Example of commands:
- <code>python gmail.<span>py</span> from:someone<span></span>@test.com after:2020/06/29 before:2020/08/01</code>
  - Looks for and downloads emails from someone<span></span>@test.com between dates June 29 and Aug 1st
- <code>python gmail.<span>py</span> from:someone<span></span>@test.com is:unread</code>
  - Looks for and downloads unread emails from someone<span></span>@test.com

By default, if the script is run without additional parameters, it looks for emails from *someone<span></span>@test.com*:
- <code>python <span>gmail.py</span></code>

Note: when you intially run the script and authenticate to Gmail, Google will warn that the app is not verified. Since this is for dev purposes only, click the "Advanced" link (if you're on Firefox) and choose to continue logging in.

## TBD:
- Add verbose information on number of emails downloaded, maybe with dates
- Indicate if there are more that can be downloaded and prompt user to continue and retrieve next batch or quit the application