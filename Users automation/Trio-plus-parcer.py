
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
import csv
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me',maxResults=300,q="trioplus.co.uk_akt7mh@collect-reviews.com").execute()
#    print (results)
    temp1 = (list(results.values()))
    print(temp1)
    myidstack=temp1[0]
    print(myidstack)
    myids=list(myidstack)
    print(myids, len(myids))
#main loop
##    exampleFile = open('trio-order-auto.csv')
##    exampleReader = csv.reader(exampleFile)
##    exampleData = list(exampleReader)
##    lastdatewritten=exampleData[0][2]
##    print (lastdatewritten)
##    exampleFile.close()
    outputFile = open('trio-order-auto.csv', 'w', newline='')
    for myfirstidnum in range(len(myids)):
        myfirstid=list(myids[myfirstidnum].values())
        print(myfirstid[0])
        myfirstidstr=str(myfirstid[0])

        message = service.users().messages().get(userId='me', id=myfirstidstr,format='raw').execute()
     
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        
        msg_strdec=msg_str.decode()
        customerFindA=msg_strdec.find('strong')
        customerFindB=msg_strdec.find('strong',customerFindA+6)
        print(customerFindA,customerFindB)
        customerFindtxt=msg_strdec[customerFindA+7:customerFindB-2]
        emailFindA=msg_strdec.find('mailto:',customerFindB)
        emailFindB=msg_strdec.find('">',emailFindA)
        emailFindtxt=msg_strdec[emailFindA+7:emailFindB]
        orderFindA=msg_strdec.find('orderId=',emailFindB)
        orderFindB=msg_strdec.find('"',orderFindA)
        orderFindtxt=msg_strdec[orderFindA+8:orderFindB]
##      if orderFindtxt==lastdatewritten:
##            break
        print(customerFindtxt,' ',emailFindtxt,' ',orderFindtxt)

        
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow([orderFindtxt,emailFindtxt,customerFindtxt,'2021-06-06'])
    outputFile.close()

if __name__ == '__main__':
    main()

