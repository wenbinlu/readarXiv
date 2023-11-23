import time
import threading
import queue
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

audio_savename = sys.argv[1]
# Set the time limit for input
time_limit = 30


# This function will run in a separate thread to get user input
def get_input(input_queue):
    # Get input from user
    user_input = input()
    # Put the user input into the queue
    input_queue.put(user_input)


mixer.init()
mixer.music.load(audio_savename)
mixer.music.play()

# Create a queue to hold the input                 
input_queue = queue.Queue()

# Set up the thread to run the get_input function
input_thread = threading.Thread(target=get_input, args=(input_queue,))
# Set the thread as a daemon so it will close when the main program closes
input_thread.daemon = True
input_thread.start()

try:
    # Try to get something off the queue within the time limit
    user_input = input_queue.get(timeout=time_limit)
    print('Y')
except queue.Empty:
    # If nothing was added to the queue, move on
    print(f"No input received within {time_limit} sec. Move on...")
# clear the queue
with input_queue.mutex:
    input_queue.queue.clear()

while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)
mixer.music.stop()
