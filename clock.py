from datetime import datetime
import time
import threading

# Waits for the user to press Enter.
# 'stop_event' is our parameter name.
def wait_for_enter(stop_event):

    # Wait for Enter.
    input()

    # Tell the clock to stop.
    stop_event.set()

# Displays the live time and date.
def display_date_time(stop_event):

    # Create a separate Thread to wait for Enter.
    enter_thread = threading.Thread(

                # Tell the Thread to run function: wait_for_enter.
                target=wait_for_enter,

                # Pass stop_event as the argument to function: wait_for_enter.
                args=(stop_event,)
    )

    # Start the Thread, which would now run the function: wait_for_enter. 
    enter_thread.start()

    # Keep looping/running the clock until function wait_for_enter sets the stop signal,
    # which is controlled by the Thread.
    while not stop_event.is_set():

        # Get the current date and time.
        current_datetime = datetime.now()
        print(
            current_datetime.strftime("%d %B %Y       %H:%M:%S"),
            end="\r"
        )

        # Wait one second before updating again.
        time.sleep(1)

    
