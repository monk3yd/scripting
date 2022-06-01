'''
Project: Script adds a case into G&P database(gsheets)
Input:
    A. New client data
    B. Existing (old) client id
    
Blackbox:
    if new client:
        add client to cartera
        add first case of new client
    
    if old client:
        if updates in client data:
            update
        add new case of old client
'''


def main():
    # Input for client
    # Check if client already exists
    # if True
        # Print existing user data
        # Check if data have changed
        # if False
            # Add new case with existing client data
            # return

        # Update data
        # Add new case with updated client data
        # return
    # else
        # Add client to database
        # Add new case with new client data
        # return


    # Get new client parameters
    # Connect to Google's API
    pass


if __name__ == "__main":
    main()
