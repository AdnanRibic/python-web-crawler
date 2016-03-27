import os


# If program is not executed completly, this code will check does that project allready exist. If it does it will not overwrite it,
#if it does not exist, than it will create new project every time we execute it
def create_directory(directory):
    if not os.path.exists(directory):
        print('New sequence started. Now we are creating new directory to put al files in. Directory is called:  ' + directory)
        os.makedirs(directory)

#This function is for creating new files. We provide path and data, and then close it to free up memory.
def write_file(path, data):
    # w stand for write
    with open(path, 'w') as file:
        file.write(data)
        # Free up memory
        file.close()

#Adding data to files that we will create
def add_to_file(path, data):
    # a stand for append
    with open(path, 'a') as file:
        # Whenever we add new files, we will provide them with new row
        file.write(data + '\n')


#Clear all data from file
def empty_file(path):
    # Writing over existing file
    with open(path, 'w'):
        # Pass is equal for do nothing. With this command we will write nothing over existing file
        pass


# Creating set list and putting objects inside it. Set list does not allow any duplicates, every item must bu unique,
# so when we crawl one page, get all link, transfer to next, the same links wont appear twice
def file_to_set(file_name):
    results = set()
    # Rt is read text files
    with open(file_name, 'rt') as file:
        for line in file:
            # Every time we are adding and converting lines, it will add \n, so we need to delete it
            results.add(line.replace('\n', ''))
    return results


# Iterate and add items to a file
def set_to_file(links, file):
    empty_file(file)
    for link in sorted(links):
        add_to_file(file, link)


# Now I am creating two things. Cue and crawl. Cueue is like waiting list and crawl is list of files that are allready crawled. Ofcourse this
# applys only if they are not created.
def create_data_files(project_name, base_url):
    queue = project_name + '/waitinglist.txt'
    crawled = project_name + '/links.txt'
    # If queue does not exist, create it like textual file
    if not os.path.isfile(queue):
        # Creactin queue file and providing it with some data, in this case, our page url so that file is not empty
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        # The same thing but instead providing it with base url, we are giving it empty string. If we do the same thing as before,
        # then program will always think that it crawled that site and we will not get any results
        write_file(crawled, '')