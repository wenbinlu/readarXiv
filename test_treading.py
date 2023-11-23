import threading
import queue

# This function will run in a separate thread to get user input
def get_input(input_queue):
    while True:
        # Get input from user
        user_input = input("Enter anything: ")
        # Put the user input into the queue
        input_queue.put(user_input)

# Create a queue to hold the input
input_queue = queue.Queue()

# Set up the thread to run the get_input function
input_thread = threading.Thread(target=get_input, args=(input_queue,))
# Set the thread as a daemon so it will close when the main program closes
input_thread.daemon = True
# Start the thread
input_thread.start()

# Set the time limit for input
time_limit = 10

try:
    # Try to get something off the queue within the time limit
    user_input = input_queue.get(timeout=time_limit)
    if user_input is not None:
        
except queue.Empty:
    # If nothing was added to the queue, move on
    print(f"No input received within {time_limit} sec. Move on...")

