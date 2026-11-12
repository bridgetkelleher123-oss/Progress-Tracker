"""Example client, showing results of input, demonstrating all errors and valid input results."""

import multiprocessing as mp
import subprocess as sp
import json
import zmq

#Create data sets to test
TEST_DATA_BOOL_VALID = [
    {"completed": True},
    {"completed": True},
    {"completed": True},
    {"completed": False},
    {"completed": False}
]
TEST_DATA_BOOL_INVALID = [
    {"completed": True},
    {"completed": True},
    {"completed": "True"},
    {"completed": False},
    {"completed": False}
]
TEST_DATA_STRING_VALID = [
    {"check_string": "pass"},
    {"check_string": "pass"},
    {"check_string": "pass"},
    {"check_string": "fail"},
    {"check_string": "fail"}
]
TEST_DATA_STRING_INVALID = [
    {"check_string": "pass"},
    {"check_string": "pass"},
    {"check_string": 1},
    {"check_string": "fail"},
    {"check_string": "fail"}
]
TEST_DATA_NAME_INVALID = [
    {"completed": True},
    {"completed": True},
    {"check_string": "pass"},
    {"completed": False},
    {"completed": False}
]
TEST_DATA_LISTITEM_INVALID = [
    {"completed": True},
        {"completed": True},
        True,
        {"completed": False},
        {"completed": False}
]

# Set up socket
context = zmq.Context()

print("Connecting to server...")

MESSAGE = "This is a message from CS361"

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5353")

#Create function to display output
def show_validity (display_dict: dict):
    """Send dict to tracker, print results of output."""
    in_json = json.dumps(display_dict)
    socket.send_json(in_json)
    output_json = socket.recv_json()
    output_dict = json.loads(output_json)
    if output_dict["valid"]:
        print(f"Input valid. Count: {output_dict["count"]}. Percentage: {output_dict["percentage"]}%.")
    else:
        print(output_dict["error_msg"])

def run_p_tracker():
    sp.run(["python3", "./progress_tracker.py"])

pt = mp.Process(target=run_p_tracker)
pt.start()

###################################################################################################
###################################################################################################
# Test demo datasets
###################################################################################################
###################################################################################################

###################################################################################################
# Invalid Data
###################################################################################################
print("~" * 50)
print("~" * 50)
print("DEMO ERROR MESSAGES")
print("~" * 50)
print("~" * 50)
print("\n")

print("-" * 50)
print("Demo invalid value types (2 examples)")
print("-" * 50)
print("example 1 data:")
in_dict = {
    "check_data": TEST_DATA_BOOL_INVALID,
    "check_name": "completed",
    "check_value": True
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("-" * 50)
print("example 2 data:")
in_dict = {
    "check_data": TEST_DATA_STRING_INVALID,
    "check_name": "check_string",
    "check_value": "pass"
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("-" * 50)
print("Demo invalid name")
print("-" * 50)
print("Example data:")
in_dict = {
    "check_data": TEST_DATA_NAME_INVALID,
    "check_name": "completed",
    "check_value": True
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("-" * 50)
print("Demo missing input")
print("-" * 50)
print("example data (missing check_value):")
in_dict = {
    "check_data": TEST_DATA_BOOL_VALID,
    "check_name": "completed"
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("-" * 50)
print("Demo bad list item, not dict:")
print("-" * 50)
in_dict = {
    "check_data": TEST_DATA_LISTITEM_INVALID,
    "check_name": "completed",
    "check_value": True
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("-" * 50)
print("Demo invalid check_data.")
print("-" * 50)
print("example data:")
in_dict = {
    "check_data": "Not a list",
    "check_name": "completed",
    "check_value": True
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("-" * 50)
print("Demo invalid check_name.")
print("-" * 50)
in_dict = {
    "check_data": TEST_DATA_BOOL_VALID,
    "check_name": True,
    "check_value": True
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

###################################################################################################
# Valid Data
###################################################################################################

print("~" * 50)
print("~" * 50)
print("DEMO VALID INPUT (2 examples)")
print("~" * 50)
print("~" * 50)
print("\n")

print("-" * 50)
print("example bool data: (should return count 3, percentage 60%)")
in_dict = {
    "check_data": TEST_DATA_BOOL_VALID,
    "check_name": "completed",
    "check_value": True
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("-" * 50)
print("example string data: (should return count 3, percentage 60%)")
in_dict = {
    "check_data": TEST_DATA_STRING_VALID,
    "check_name": "check_string",
    "check_value": "pass"
}
pprint(in_dict)
show_validity(in_dict)
print("\n")

print("~" * 50)
print("~" * 50)
print("END PROGRESS_TRACKER")
print("~" * 50)
print("~" * 50)
print("\n")

in_dict = {
    "end": True
}
pprint(in_dict)
show_validity(in_dict)

pt.join()
print("Test concluded.")
