"""Act as a server bound to port 5353. When data is received:
- Check validity. Valid input is a JSON object that looks like:
    - {
        'check_data': [{json}, {json}, {json}],
        'check_name': 'check_string',
        'check_value': value(any)}
    - Or, if ending the program:
        {
        'end': true}
    - All json objects in check_data must have one attribute name matching the input check_name.
    - All values connected to check_name must be the same value type as check_value.
- get a count of how many objects whose values connected to check_name are identical to check_value
- find percentage of these objects out of total array
- Output back a json object containing:
    - boolean 'valid': true when valid input
    - int 'count': null when valid is false
    - float 'percentage': null when valid is false
    - string 'error_msg': null when valid is true"""

import json
import zmq

def get_count(check_list: list[dict], check_name: str, check_value) -> dict["valid":bool,
                                                                           "count":int,
                                                                           "percentage":float,
                                                                           "error_msg":str]:
    """Return error message, or count and percentage of dicts containing check_value
    at check_name."""
    count = 0
    for check_dict in check_list:
        if not isinstance(check_dict, dict):
            return {
                "valid": False,
                "count": None,
                "percentage": None,
                "error_msg": f"ERROR: List item {check_dict} is not a dictionary."
            }
        elif check_name not in check_dict:
            return {
                "valid": False,
                "count": None,
                "percentage": None,
                "error_msg": f"ERROR: check_name {check_name} not present in all objects."
            }
        elif type(check_dict[check_name]) != type(check_value):
            return {
                "valid": False,
                "count": None,
                "percentage": None,
                "error_msg": f"ERROR: value type {check_dict[check_name]} at name {check_name} in {check_dict} does not match type of check_value: {type(check_value)}."
            }
        elif check_dict[check_name] == check_value:
            count += 1
    return {
        "valid": True,
        "count": count,
        "percentage": count / len(check_list) * 100,
        "error_msg": None
    }

# Set up server at socket 5353
context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5353")

stay_alive = True
while stay_alive:
    out_dict: dict["valid":bool,
                    "count":int,
                    "percentage":float,
                    "error_msg":str] = {}
    # get input
    input_msg = socket.recv_json()
    in_dict:dict = json.loads(input_msg)
    # Check if time to end
    if "end" in in_dict:
        stay_alive = False
        out_dict = {
            "valid": False,
            "count": None,
            "percentage": None,
            "error_msg": "Program ended."
        }
    # Input validation: Missing input
    elif not "check_data" in in_dict or not "check_name" in in_dict or not "check_value" in in_dict:
        out_dict = {
            "valid": False,
            "count": None,
            "percentage": None,
            "error_msg": "ERROR: Missing input."
        }
    # Input validation: invalid check_data
    elif not isinstance(in_dict["check_data"], list):
        out_dict = {
                    "valid": False,
                    "count": None,
                    "percentage": None,
                    "error_msg": "ERROR: invalid check_data. must be list."
                }
    # Input validation: invalid check_name
    elif not isinstance(in_dict["check_name"], str):
        out_dict = {
                    "valid": False,
                    "count": None,
                    "percentage": None,
                    "error_msg": "ERROR: invalid check_name. must be string."
                }
    else:
        #Get output
        out_dict = get_count(in_dict["check_data"], in_dict["check_name"], in_dict["check_value"])
    #send back output
    out_json = json.dumps(out_dict)
    socket.send_json(out_json)
