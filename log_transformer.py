import json
from datetime import datetime
import sys
import requests

def transform_log(LogFilePath):
    """
    transform a log in KT LOGGER format to a json format based on events ordered ascending
    LogFilePath : full path of the Log file to be parsed
    """
    data = open(LogFilePath,'r').readlines()
    start_ = datetime.now()
    transform_stats={'exceptions':[],'start':None,'end':None, 'time_taken':None}
    tree={'information':[],'trace':[],'warning':[],'error':[],'all':[],}
    for lines in data:
        try:
            if(lines.split('\t')[0] in ['<information>','<error>','<trace>','<warning>']):
                type_of_line = lines.split('\t')[0].strip('<').strip('>')
                tree[type_of_line].append(lines)
                tree['all'].append(lines)
            else:
                tree['all'].append(lines)
        except:
            transform_stats['exceptions'].append(str(sys.exc_info()))
    end_ = datetime.now()
    transform_stats['start']=str(start_)
    transform_stats['end']=str(end_)
    transform_stats['time_taken']=str((end_-start_).total_seconds())
    return {"stats":transform_stats, "data":tree}

def get_last_few_events(LogFilePath , event , count):
    """
    Get last few events from the given KT LOG 
    LogFilePath : path of the Logfile to parse
    event : Event to filter
    count: int - last n occurences of the event
    Eg. get_last_few_events("d:\\ge_log.log','error',5)
    """
    log_json = transform_log(LogFilePath)
    if(log_json['stats']['exceptions'].__len__()==0):
        try:
            return log_json['data'][event][-count::]
        except IndexError:
            return []


def generate_transform_log_link(LogFilePath):
    """
    Generate a link that serves the Log file a json
    LogFilePath Path of the log file to be parsed
    returns the link generated for the data
    WARNING: served data response may be too large for certain programs to handle!
    """
    try:
        log_json = transform_log(LogFilePath)
        rs = requests.post(url = json.load(open('config.json'))['data_host'], json = log_json)
        return rs.content
    except:
        return None

def generate_last_few_events_as_link(LogFilePath , event , count):
    """
    Generate last few events and server the data using a generated url
    LogFilePath : path of the Logfile to parse
    event : Event to filter
    count: int - last n occurences of the event
    Ex: generate_last_few_events_as_link("d:\\ge_log.log','error',5)

    returns str: link generated
    WARNING: served data response may be too large for certain programs to handle!
    """
    events = get_last_few_events(LogFilePath , event , count)
    try:        
        rs = requests.post(url = json.load(open('config.json'))['data_host'], json = events)
        return rs.content
    except:
        return None