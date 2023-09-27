import logging

# Create a logger
logger = logging.getLogger(__name__)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file handler to write log messages to a file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)  # Set the log level for the file handler
file_handler.setFormatter(formatter)

# Create a console handler to display log messages in the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the log level for the console handler
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Set the log level for the logger (you can adjust this as needed)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
