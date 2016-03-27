from urllib.request import urlopen
from parser import link_parser
from url import *
from creator import *


class Bot:
    # Class variables
    folder = ''
    url = ''
    domain = ''
    queue_file = ''
    crawled_file = ''
    # Sets are used for faster operations because their values will be in ram
    queue = set()
    crawled = set()

    # Initialazing and givin objects its values passed from user and creatin files
    def __init__(self, folder, url, domain):
        Bot.folder = folder
        Bot.url = url
        Bot.domain = domain
        Bot.queue_file = Bot.folder + '/waitinglist.txt'
        Bot.crawled_file = Bot.folder + '/links.txt'
        self.boot()
        # Creating first line in crawled pages so that any other instance can see it, skipp it and continue to workd on another threads
        self.crawl_page('First Bot', Bot.url)

    # Function for the first bot, needs to create project directory and files
    @staticmethod
    def boot():
        create_directory(Bot.folder)
        create_data_files(Bot.folder, Bot.url)
        Bot.queue = file_to_set(Bot.queue_file)
        Bot.crawled = file_to_set(Bot.crawled_file)

    # If we make another bot we will need to provide him with updated informations
    @staticmethod
    def crawl_page(thread_name, url):
        if url not in Bot.crawled:
            print(thread_name + ' is now web crawling: ' + url)
            # Show how much info is in waiting queue and how much is crawled. We will convert that info into string
            print('Remaining files in waiting list: ' + str(len(Bot.queue)) + ' *** Files that are crawled and saved:  ' + str(len(Bot.crawled)))
            # When we get links we need them to be added to queue
            Bot.add_links_to_queue(Bot.gather_links(url))
            # When page is crawled we need to remove it and add it to crawled pages
            Bot.queue.remove(url)
            Bot.crawled.add(url)
            # Now we will take everything processes from ram and put it in files on disk
            Bot.update_files()

    # Because python gives us html in binary form we need to convert it to strings
    @staticmethod
    def gather_links(url):
        html_string = ''
        try:
            # Connects us to a site
            response = urlopen(url)
            # Get only the html file, nothing else
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                # Take html bytes and convert them to readable format
                html_string = html_bytes.decode("utf-8")
            finder = link_parser(Bot.url, url)
            finder.feed(html_string)
        except Exception as error:
            print(str(error))
            # We must return set so we will provide it with empty set
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            # First we need to check are they already in queue and second we need to check are they allread crawled
            if (url in Bot.queue) or (url in Bot.crawled):
                continue

            # Third is to add our domain. If we forget about this, bot will crawl entire internet :P
            if Bot.domain != get_url(url):
                continue
            Bot.queue.add(url)

    @staticmethod
    def update_files():
        # Now save to file from set that we have
        set_to_file(Bot.queue, Bot.queue_file)
        set_to_file(Bot.crawled, Bot.crawled_file)

