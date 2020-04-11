
#######################################################################################
# Display formatting
def print_spacer():
    print("---------------------------------------------------------------")
    return

def print_message(str_description, str_info):
    print()
    print_spacer()
    print(str_description, str_info)
    print()
    return
#######################################################################################
# Automatically find the previous data file
def find_last_local_data_file():
    i=0
    while i<7:
        # Get a time stamp i days from now
        date_i_days_ago = datetime.now() - timedelta(days=i)
        # Format the time stamp
        day_str = date_i_days_ago.strftime("%Y.%m.%d")
        # This should be the name of the data file created i days ago (if it exists)
        filename = path + "cor." + day_str+".csv"
        # Check if the data file created i days ago exists
        file_found =  glob.glob(filename)
        if file_found:
            print_message("Last local data file found:" , file_found[0])
            i=7
        i=i+1
    return filename