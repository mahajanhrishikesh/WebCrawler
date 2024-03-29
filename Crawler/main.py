import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'wikipedia'
HOMEPAGE = 'https://en.wikipedia.org/wiki/Main_Page'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 2		#use as you will
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


#Create worker threads(will die when main exits)
def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target = work)  #work will be job of the thread
		t.daemon = True
		t.start()

# Do the next job in the queue
def work():
	while True:
		url = queue.get()
		Spider.crawl_page(threading.current_thread().name, url)	#asks for thread number and url it is doing
		queue.task_done()

#each queue link is a new job 
def create_jobs():
	for link in file_to_set(QUEUE_FILE):
		queue.put(link)
	queue.join()
	crawl()	


#check if there are items in the todo list and then crawl them
def crawl():
	queued_links = file_to_set(QUEUE_FILE)
	if len(queued_links) > 0:
		print(str(len(queued_links))+ ' links in the queue.')
		create_jobs()
		
create_workers()
crawl()
		