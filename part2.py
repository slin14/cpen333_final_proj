# Group #: 32
# Student names: Joshua Ho, Sophie Lin
 
import threading
import queue
import time, random

def consumerWorker (queue):
    """target worker for a consumer thread"""
    # to implement  

    # inner function to add a random delay for when an item is consumed
    def waitForItemToBeConsumed() -> None:
        time.sleep(round(random.uniform(minDelayConsumer, maxDelayConsumer), 2)) # wait for a random delay

    # consume {consumeItems} number of items
    for _ in range(consumeItems):
        waitForItemToBeConsumed() # wait for a random delay
        item = buffer.get()       # consume an item
        print(f"DEBUG: {item} consumed")

  
def producerWorker(queue):
    """target worker for a producer thread"""
    # to implement

    # inner function to add a random delay for when an item is produced
    def waitForItemToBeProduced() -> int:
        time.sleep(round(random.uniform(minDelayProducer, maxDelayProducer), 2)) #wait for a random delay
        return random.randint(minItemProduced, maxItemProduced)  #produce an item

    for _ in range(produceItems): # produce a few items for testing
        item = waitForItemToBeProduced()  #wait for an item to be produced, then produce an item
        print(f"DEBUG: {item} produced")
        buffer.put(item) # store the produced item into the buffer


if __name__ == "__main__":
    buffer = queue.Queue()
    # to implement

    # parameters for number of producer/consumer threads, and number of items each thread produces/consumes
    producerThreads = 4    # number of producer threads
    consumerThreads = 5    # number of consumer threads
    produceItems = 4       # a reasonably small # of items that each producer thread produces
    consumeItems = 3       # a reasonably small # of items that each consumer thread consumes
    
    # random delay settings for when an item is produced and consumed
    minDelayProducer = 0.1 # mininum delay in seconds
    maxDelayProducer = 0.3 # maximum delay in seconds
    minDelayConsumer = 0.1 # minimum delay in seconds
    maxDelayConsumer = 0.3 # maximum delay in seconds

    # randomness for the value of items produced
    minItemProduced = 1    # minimum value of item produced
    maxItemProduced = 99   # maximum value of item produced

    # implementation
    threads = [] # list containing all the threads 

    # create and start producer threads
    for i in range(producerThreads):
        p = threading.Thread(target=producerWorker, args=(buffer,))
        p.start()
        threads.append(p)

    # create and start consumer threads
    for i in range(consumerThreads):
        p = threading.Thread(target=consumerWorker, args=(buffer,))
        p.start()
        threads.append(p)

    # call join() on all the threads 
    for thread in threads:
        thread.join()

    ## testing 1 producer and 1 consumer thread
    #p1 = threading.Thread(target=producerWorker, args=(buffer,))
    #p1.start()

    #p2 = threading.Thread(target=consumerWorker, args=(buffer,))
    #p2.start()

    #p1.join()
    #p2.join()
