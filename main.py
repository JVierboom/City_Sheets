# ------------------------------- core imports ------------------------------- #
import sys
import os
import datetime

# ----------------------------- 3rd-party imports ---------------------------- #

# ------------------------------- local imports ------------------------------ #
sys.path.append(".")

from city import City

# --------------------------- variable declaration --------------------------- #

debug_enabled = True
sheet_string = ""
city_size = 0

# ------------------------------ debug function ------------------------------ #


def log(debug_message: str):
    if debug_enabled:
        timestamp = datetime.datetime.now()
        file = open(f'./output/logs/city_sheet_{timestamp.strftime("%d-%m-%Y")}.log', 'a')
        file.write(f'[{timestamp.strftime("%H:%M:%S")}] - {debug_message}' + os.linesep)
        file.close()

# ------------------------------- main program ------------------------------- #

log("# STARTING GENERATOR #")

# get user input for how large of a city they want
while True:
    try:

        city_size = int(input((
            "Please select one of the following city sizes:" + os.linesep + \
            "1: Outpost, 2: Thorp, 3: Hamlet, 4: Village, 5: Small town, " + os.linesep + \
            "6: Large town, 7: Small city, 8: Large city, 9: Metropolis, 10: Capital" + os.linesep + \
            "> "
        )))

        if city_size < 1:
            print("Oopsy woopsy, you did a fucky wucky uwu. ENTER A NUMBER > 1 NEXT TIME DUMBASS.")
        elif city_size > 10:
            print("Oopsy woopsy, you did a fucky wucky uwu. ENTER A NUMBER < 10 NEXT TIME DUMBASS.")
        else:
            print("Generating sheet...")
            log("# USER INPUT RECIEVED #")
            break

    except:

        print("Oopsy woopsy, you did a fucky wucky uwu. ENTER A PROPER NUMBER NEXT TIME DUMBASS.")

# create city from user input and propogate city data
city = City(city_size, debug_enabled)
city.propogate_data()

# get template for city sheet and stringify it
log("# READING SHEET TEMPLATE #")
sheet_template = open('./assets/sheet_template.txt', 'r')

# fill lines with data
log("# RECONSTRUCTING TEMPLATE #")
last_stat_scanned = ""
while True:

    log("Grabbing new line")
    # grab new line and break if reached EOF
    line = sheet_template.readline()
    if not line:
        break

    log("Tokenizing line")
    # tokenize line and match cases
    line_parts = line.strip().split(":")

    log("Matching first token as line ID")
    match line_parts[0]:
        case "City Name":
            sheet_string += line.strip() + " " + "Generic City" + os.linesep
            log("City name set")

        case "City Type":
            sheet_string += line.strip() + " " + city.get_type() + os.linesep
            log("City type set")

        case "City Population":
            sheet_string += line.strip() + " " + str(city.get_population()) + os.linesep
            log("City population set")

        case "Specialisation":
            specialities = city.get_specialities()
            sheet_string += line.strip() + " #1 " + specialities[0] + " || #2 " + specialities[1] + os.linesep

        case _:
            # stat handling
            line_stat = city.get_stat(line_parts[0])
            if line_stat != None:
                last_stat_scanned = line_parts[0]
                sheet_string += line.strip() + " " + str(line_stat) + os.linesep
                log("City stat " + line_parts[0] + " set")
            else:
                try:
                    # stat location handling
                    if line_parts[0][0] == "-":
                        location_data = city.get_locations(last_stat_scanned)
                        if location_data != None:
                            sheet_string += " " + line_parts[0].strip().format(location_data[0], location_data[1], location_data[2], location_data[3], location_data[4]) + os.linesep
                            log("City stat locations set")
                    else:
                        sheet_string += line.strip() + os.linesep

                except:
                    # default
                    sheet_string += line.strip() + os.linesep

# kill the template file stream
sheet_template.close()

# construct and save new sheet file
log("# CREATING NEW SHEET AND DIRECTORY #")
timestamp = datetime.datetime.now()

# make directory
sheet_directory = f'./output/{timestamp.strftime("%d-%m-%Y")}'
if not os.path.exists(sheet_directory):
    os.makedirs(sheet_directory, exist_ok=True)

# make and write file
log("# WRITING DATA TO FILE #")
new_sheet = open(sheet_directory + "/" + timestamp.strftime("%H-%M-%S") + ".txt", "w")
new_sheet.write(sheet_string)
new_sheet.close()

print(f'Sheet output to {timestamp.strftime("%H-%M-%S")}.txt in the folder {sheet_directory}')
log(f'# Sheet output to {timestamp.strftime("%H-%M-%S")}.txt in the folder {sheet_directory} #' + os.linesep + os.linesep)
