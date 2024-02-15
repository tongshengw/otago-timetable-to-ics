from datetime import datetime
import ics
import re

def parse (line, line1, objdate):
    # details = line.split('\t')
    # print (details)
    # date, event_type_title = details[0], details[1].split(' - ')
    # date = date.strip()
    # course_code = line1.strip()
    # time_range_type = event_type_title[0].split(' ')
    # time_range = time_range_type[0]
    # event_type = time_range_type[1]
    # start_end_time = time_range.split('-')
    # start_time, end_time = start_end_time[0], start_end_time [1]
    # title = event_type_title[1]

#10:00-11:00 Other Teaching - The Chemical Basis of Biology and Human Health
    details = line.split(' ', 1)
    time_range = details[0].split('-')
    start_time, end_time = time_range[0], time_range[1]
    type_title = details[1].split('-')
    type, title = type_title[0].strip(), type_title[1].strip()
    course_code = line1.strip()

    events.append({"date":objdate.strftime('%d %B %Y'), "start_time": start_time, "end_time": end_time, "type": type, "course_name": title, "course_code": course_code})




# Step 1: Parse the Text File
def parse_text_to_events_array(file_path):
    global events
    events = []
    current_date = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines.append("")
        # print (lines)
    
    i=0
    while i < len(lines)-1:
        line1 = lines[i].strip()
        line2 = lines[i+1].strip()
        line3 = lines[i+2].strip()

        # Match lines that start with a date pattern
        if re.match(r'\w+day', line1):
            date_str = re.search(r'\d+\s+\w+\s+\d+', line2).group()
            if date_str:
                current_date = datetime.strptime(date_str.strip(), '%d %B %Y')
                
                pureline = line2.split('\t')
                parse(pureline[1], line3, current_date)
                i+=3
            else:
                print('error')
                exit()

        elif current_date and line1:  
            parse (line1, line2, current_date)
            i+=2


    # print('\n events')
    print (events)
    return events

# Step 2: Generate the .ics File
def create_ics_file(events, output_file_name, type):
    c = ics.Calendar()
    
    for event in events:
        if event["type"] == type:
            e = ics.Event()
            e.name = f'{event["course_code"]} ({event["type"]})'
            e.begin = datetime.strptime(f'{event["date"]} {event["start_time"]}', '%d %B %Y %H:%M')
            e.end = datetime.strptime(f'{event["date"]} {event["end_time"]}', '%d %B %Y %H:%M')
            e.description = f'{event["course_name"]}, {event["type"]} ({event["course_code"]})'
            c.events.add(e)
    
    with open(output_file_name, 'w') as file:
        file.writelines(c)

# Example usage
file_path = '2024sem1.txt'  # Update this to your actual text file path
events = parse_text_to_events_array(file_path)

type_list = []

for event in events:
    if event['type'] not in type_list:
        type_list.append(event["type"])

for type in type_list:
    create_ics_file(events, f'{type}2024.ics', type)