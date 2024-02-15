from datetime import datetime
import ics
import re
import sys
import pytz

global timezone
timezone = pytz.timezone("Pacific/Auckland")

def parse (line, line1, objdate):

    details = line.split(' ', 1)
    # print(objdate.strftime('%d %B %Y'))
    # print(details)
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
        lines.append("lastline")
        # print (lines)
    
    #loops through all lines. needs one extra blank line in order to catch last event.
    i=0
    while i < len(lines)-1:
        line1 = lines[i].strip()
        line2 = lines[i+1].strip()
        line3 = lines[i+2].strip()

        # if line1 contains a day of the week, parse line2 and line3. if not, parse line1 and line2
        if re.match(r'\w+day', line1):
            date_str = re.search(r'\d+\s+\w+\s+\d+', line2).group()
            print(date_str + 'end')
            if date_str and line2 != "" and line3 != "":
                current_date = datetime.strptime(date_str.strip(), '%d %B %Y')
                print(line2)
                pureline = line2.split('\t')
                parse(pureline[1].strip(), line3, current_date)
                i+=3
            else:
                print('error')
                sys.exit(2)

        elif current_date and line1 != "" and line2 != "":
            parse (line1, line2, current_date)
            i+=2


    # print('\n events')
    # print (events)
    return events

# Step 2: Generate the .ics File
def create_ics_file(events, output_file_name, type):
    c = ics.Calendar()
    
    for event in events:
        if event["type"] == type:
            e = ics.Event()
            e.name = f'{event["course_code"]} ({event["type"]})'
            e.begin = timezone.localize(datetime.strptime(f'{event["date"]} {event["start_time"]}', '%d %B %Y %H:%M'))
            e.end = timezone.localize(datetime.strptime(f'{event["date"]} {event["end_time"]}', '%d %B %Y %H:%M'))
            e.description = f'{event["course_name"]}, {event["type"]} ({event["course_code"]})'
            c.events.add(e)
    
    with open(output_file_name, 'w') as file:
        file.writelines(c)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py [input.txt]")
        sys.exit(1)
    file_path = sys.argv[1]
    events = parse_text_to_events_array(file_path)

    type_list = []

    for event in events:
        if event['type'] not in type_list:
            type_list.append(event["type"])

    for type in type_list:
        create_ics_file(events, f'{type}.ics', type)
        # print(f'made {type}.ics')
    

main()