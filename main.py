import threading
from queue import Queue
from bot import Bot
from url import *
from creator import *

folder = 'Fit'
url = 'http://www.fit.ba/'
domain = get_url(url)
waiting_files = folder + '/waitinglist.txt'
links_files = folder + '/links.txt'
number_of_cores = 8
waiting_list = Queue()
Bot(folder, url, domain)

# Because we have lot cores on our processors, we can make more bots to work at the same time. With this function we will make more bots.
# Bots will find their jobs automaticly and when they are finished, tehy will shutdwn
# _ will let compiler create variable and type for us
def create_bots():
    for _ in range(number_of_cores):
        # All threads can work only one job which is called work
        t = threading.Thread(target=work)
        # When is run as deamon, it will die a the end of work
        t.daemon = True
        t.start()


# Do the next job in the waiting list
def work():
    while True:
        url = waiting_list.get()
        # Threading module that will give us name of thread which is wokring on file
        Bot.crawl_page(threading.current_thread().name, url)
        waiting_list.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(waiting_files):
        waiting_list.put(link)
    waiting_list.join()
    crawl()


# With this function we will check are there any links in waiting list and that we need to crawl them
def crawl():
    queued_links = file_to_set(links_files)
    if len(queued_links) > 0:
       create_jobs()


create_bots()
crawl()