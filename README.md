# TNT
A powerful and easy-to-use tool that performs DDoS attacks on websites.

usage : python3 tnt.py [-s] [-p] [-t]
-h : help
-s : server IP
-p : port (default 80)
-t : turbo (default 135)

Improvements and Features

    Class Structure: Refactored the code into a TNT class for better organization and encapsulation of functionality.
    Enhanced Error Handling: Implemented specific exception handling to provide clearer error messages and improve debugging.
    Socket Management: Utilized context managers (with statements) for socket connections to ensure proper resource management and prevent leaks.
    Dynamic User Agents: Randomized user-agent strings to simulate different clients, enhancing the realism of requests.
    Command-Line Interface: Improved command-line argument parsing with clear usage instructions and default values for parameters.
    Header File Handling: Added error handling for reading the headers file, ensuring graceful exits if the file is missing.
    Thread Management: Implemented daemon threads to prevent blocking the main program from exiting and to manage concurrent requests effectively.
    Memory Management: Included logic to prevent memory crashes by limiting the number of queued items.
    User -Friendly Output: Enhanced console output with color-coded messages for better visibility and user experience.

Feel free to modify or expand upon these points to better fit your project's style and goals!
