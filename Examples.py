#examples:

# get the given log in json format
import log_transformer

logs_in_json = log_transformer.transform_log('D:\GeneralLog1350002-191014.log')


# to get last n events 
import log_transformer

last_5_errors = log_transformer.get_last_few_events('D:\GeneralLog1350002-191014.log','error',5)
last_5_info = log_transformer.get_last_few_events('D:\GeneralLog1350002-191014.log','information',5)

# to get log as a link
import log_transformer
logs_asjson_link = log_transformer.generate_transform_log_link('D:\GeneralLog1350002-191014.log')
print(logs_asjson_link)

#to get last n events as link
import log_transformer
last_5_Events_as_link = log_transformer.generate_last_few_events_as_link('D:\GeneralLog1350002-191014.log','error',5)
print(last_5_Events_as_link)
