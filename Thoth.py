import json
import random
import datetime
import os
import uuid
import pytz  # Import pytz for time zone support

# List of time zones for user selection
TIME_ZONES = [
    ("Pacific/Midway", "UTC-11:00"),  # Midway Island, Samoa (SST)
    ("Pacific/Honolulu", "UTC-10:00"),  # Hawaii (HST)
    ("Pacific/Marquesas", "UTC-09:30"),  # Marquesas Islands (MART)
    ("America/Anchorage", "UTC-09:00"),  # Alaska (AKST)
    ("America/Los_Angeles", "UTC-08:00"),  # Pacific Time (US & Canada) (PST)
    ("America/Denver", "UTC-07:00"),  # Mountain Time (US & Canada) (MST)
    ("America/Phoenix", "UTC-07:00"),  # Arizona (MST)
    ("America/Chicago", "UTC-06:00"),  # Central Time (US & Canada) (CST)
    ("America/New_York", "UTC-05:00"),  # Eastern Time (US & Canada) (EST)
    ("America/Caracas", "UTC-04:30"),  # Caracas, Venezuela (VET)
    ("America/Halifax", "UTC-04:00"),  # Atlantic Time (Canada) (AST)
    ("America/Santiago", "UTC-04:00"),  # Santiago, Chile (CLST)
    ("America/St_Johns", "UTC-03:30"),  # Newfoundland (NST)
    ("America/Sao_Paulo", "UTC-03:00"),  # São Paulo, Brazil (BRT)
    ("America/Argentina/Buenos_Aires", "UTC-03:00"),  # Buenos Aires, Argentina (ART)
    ("America/Noronha", "UTC-02:00"),  # Fernando de Noronha, Brazil (FNT)
    ("Atlantic/Azores", "UTC-01:00"),  # Azores, Portugal (AZOT)
    ("UTC", "UTC"),  # Coordinated Universal Time (UTC)
    ("Europe/London", "UTC+00:00"),  # London, Dublin, Lisbon (GMT/BST)
    ("Africa/Lagos", "UTC+01:00"),  # Lagos, Nigeria (WAT)
    ("Europe/Paris", "UTC+01:00"),  # Paris, Berlin, Rome (CET/CEST)
    ("Africa/Johannesburg", "UTC+02:00"),  # Johannesburg, South Africa (SAST)
    ("Europe/Moscow", "UTC+03:00"),  # Moscow, St. Petersburg, Volgograd (MSK)
    ("Asia/Dubai", "UTC+04:00"),  # Dubai, Abu Dhabi (GST)
    ("Asia/Tehran", "UTC+04:30"),  # Tehran, Iran (IRST)
    ("Asia/Kolkata", "UTC+05:30"),  # India Standard Time (IST)
    ("Asia/Kathmandu", "UTC+05:45"),  # Kathmandu, Nepal (NPT)
    ("Asia/Dhaka", "UTC+06:00"),  # Dhaka, Bangladesh (BDT)
    ("Asia/Bangkok", "UTC+07:00"),  # Bangkok, Hanoi, Jakarta (ICT)
    ("Asia/Singapore", "UTC+08:00"),  # Singapore, Kuala Lumpur, Perth (SGT)
    ("Asia/Tokyo", "UTC+09:00"),  # Tokyo, Osaka, Sapporo (JST)
    ("Australia/Sydney", "UTC+10:00"),  # Sydney, Melbourne, Brisbane (AEST)
    ("Pacific/Guam", "UTC+10:00"),  # Guam, Port Moresby (ChST)
    ("Pacific/Fiji", "UTC+12:00"),  # Fiji, Marshall Islands (FJT)
    ("Pacific/Auckland", "UTC+12:00"),  # Auckland, Wellington (NZST)
]

def get_time_zone():
    # Prompt user to select a time zone and return both IANA and UTC formats.
    print("\nSelect your time zone:")
    for idx, (iana, utc) in enumerate(TIME_ZONES, start=1):
        print(f"[{idx}] {iana} ({utc})")

    while True:
        choice = input(f"\nEnter your choice (1-{len(TIME_ZONES)}): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(TIME_ZONES):
                return TIME_ZONES[index]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def print_thoth_logo():
    print("""
    ███        ▄█    █▄     ▄██████▄      ███        ▄█    █▄    
▀█████████▄   ███    ███   ███    ███ ▀█████████▄   ███    ███   
   ▀███▀▀██   ███    ███   ███    ███    ▀███▀▀██   ███    ███   
    ███   ▀  ▄███▄▄▄▄███▄▄ ███    ███     ███   ▀  ▄███▄▄▄▄███▄▄ 
    ███     ▀▀███▀▀▀▀███▀  ███    ███     ███     ▀▀███▀▀▀▀███▀  
    ███       ███    ███   ███    ███     ███       ███    ███   
    ███       ███    ███   ███    ███     ███       ███    ███   
   ▄████▀     ███    █▀     ▀██████▀     ▄████▀     ███    █▀    
""")

# Load the directory of knowledge bases from a JSON file.
def load_directory(filename):
    with open(filename, 'r') as file:
        directory_data = json.load(file)
    return directory_data.get('Knowledge_Bases', [])

# Load questions from a JSON file.
def load_questions(filename):
    # Load questions from a JSON file.
    with open(filename, 'r') as file:
        data = json.load(file)
        questions = data.get("Questions", [])
    return questions

# Function to load data from JSON file
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to save data to JSON file
def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Load a section file and return its content excluding 'Questions'.
def load_section_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        section_data = {key: value for key, value in data.items() if key != 'Questions'}
    return section_data

# Generates sessions ID using UUID version 4
def generate_session_id():
    return str(uuid.uuid4())

# Extract unique items from a list of dictionaries based on a specific key.
def get_unique_items(data, key):
    return sorted(set(item[key] for item in data))

# Print options in a numbered list.
def print_numbered_options(options):
    for idx, option in enumerate(options, start=1):
        print(f"[{idx}] {option}")

# Select an option from a list and return the index.
def select_option(options, message):
    print(message)
    print_numbered_options(options)
    choice = input(f"\nEnter your choice (1-{len(options)}): ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(options):
            return index
        else:
            print("Invalid choice. Please select a valid option.")
            return select_option(options, message)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return select_option(options, message)

# Select an option from a list and return the indices.
def select_multiple_options(options, message):
    print(message)
    print_numbered_options(options)

    while True:
        try:
            choices = input(f"\nEnter your choices (comma-separated numbers between 1-{len(options)}): ")
            indices = [int(choice) - 1 for choice in choices.split(',') if choice.strip()]
            if all(0 <= index < len(options) for index in indices):
                return indices
            else:
                print("Invalid choice. Please select valid options within the given range.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter comma-separated numbers.")

def ask_question(question_data, question_number, missed_questions):
    question_content = list(question_data.values())[0]  # Extract the question data from the nested structure
    user_answers = []

    print(f"\nQuestion {question_number}")
    print(question_content['Prompt'])
    answers_text = [answer['text'] for answer in question_content['Answers']]
    correct_answer_ids = question_content['CorrectAnswerIDs'] if isinstance(question_content['CorrectAnswerIDs'], list) else [question_content['CorrectAnswerIDs']]
    correct_answers_text = [answer['text'] for answer in question_content['Answers'] if answer['id'] in correct_answer_ids]

    if question_content['MultipleCorrectAnswers']:
        indices = select_multiple_options(answers_text, "Select all correct answers (separated by commas):")
        for index in indices:
            user_answers.append(question_content['Answers'][index]['id'])
    else:
        index = select_option(answers_text, "Select an answer:")
        user_answers = [question_content['Answers'][index]['id']]

    selected_answers_text = [answer['text'] for answer in question_content['Answers'] if answer['id'] in user_answers]
    
    input("Type the answer(s) for practice: ")

    if not question_content['OrderAgnostic']:
        if user_answers == correct_answer_ids:
            print("Correct!")
            return True
        else:
                print("Incorrect.")
                missed_questions.append({
                        'Question': question_content['Prompt'],
                        'Your Answer(s)': ', '.join(selected_answers_text),
                        'Correct Answer(s)': ', '.join(correct_answers_text)
                    })
                return False
    else:
        if set(user_answers) == set(correct_answer_ids):
            print("Correct!")
            return True
        else:
                print("Incorrect.")
                missed_questions.append({
                        'Question': question_content['Prompt'],
                        'Your Answer(s)': ', '.join(selected_answers_text),
                        'Correct Answer(s)': ', '.join(correct_answers_text)
                    })
                return False

# Function to calculate time elapsed
def calculate_time_elapsed(start_time, end_time):
    start = datetime.datetime.fromisoformat(start_time)
    end = datetime.datetime.fromisoformat(end_time)
    elapsed = end - start
    return str(elapsed)

def generate_mistakes_breakdown(incorrect_answers):
    # Generate detailed questions data for logging.
    detailed_questions = []
    question_number = 1
    for answer in incorrect_answers:
        detailed_question = {
            "Question_Number": question_number,
            "Question": answer['Question'],
            "User_Answer": answer['Your Answer(s)'],
            "Correct_Answer": answer['Correct Answer(s)'],
            "Is_Correct": False
        }
        detailed_questions.append(detailed_question)
        question_number += 1
    return detailed_questions

def calculate_average_time_per_question(time_elapsed, question_amount):
    # print("This is the time_elapsed variable: " + time_elapsed)
    
    try:
        # Splitting time_elapsed into hours, minutes, seconds, and microseconds
        times = time_elapsed.split(':')
        # print("This is the content of the times variable:")
        # print(times)
        hours = times[0]
        # print("This is the content of the hours variable: " + hours)
        minutes = times[1]
        # print("This is the content of the minutes variable: " + minutes)
        total_seconds = times[2]
        seconds, microseconds = total_seconds.split('.')
        # print("This is the content of the seconds variable: " + seconds)
        # print("This is the content of the microseconds variable: " + microseconds)
        
        # Convert parts into integers
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        microseconds = int(microseconds)

        # Create timedelta object
        time_elapsed = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)
    except ValueError:
        # Handle if the string format does not match expected format
        raise ValueError("Invalid time duration format for time_elapsed")

    # Calculate average time per question
    average_time_per_question = time_elapsed / question_amount
    atpq_string = str(average_time_per_question)
    
    return atpq_string

# Calculate the grade percentage based on correct answers.
def calculate_grade_percentage(correct_count, question_amount):
    if question_amount > 0:
        return (correct_count / question_amount) * 100
    else:
        return 0.0

# Assign letter grade based on the grade percentage.
def assign_letter_grade(grade_percent):
    if 96.5 <= grade_percent <= 100:
        return "A+"
    elif 93.5 <= grade_percent < 96.5:
        return "A"
    elif 89.5 <= grade_percent < 93.5:
        return "A-"
    elif 86.5 <= grade_percent < 89.5:
        return "B+"
    elif 83.5 <= grade_percent < 86.5:
        return "B"
    elif 79.5 <= grade_percent < 83.5:
        return "B-"
    elif 76.5 <= grade_percent < 79.5:
        return "C+"
    elif 73.5 <= grade_percent < 76.5:
        return "C"
    elif 69.5 <= grade_percent < 73.5:
        return "C-"
    elif 66.5 <= grade_percent < 69.5:
        return "D+"
    elif 63.5 <= grade_percent < 66.5:
        return "D"
    elif 59.5 <= grade_percent < 63.5:
        return "D-"
    else:
        return "F"

# Determine pass or fail based on letter grade and section priority.
def determine_pass_fail(letter_grade, is_priority_section):
    if is_priority_section:
        return letter_grade in {"A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-"}
    else:
        return letter_grade in {"A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-"}

def find_knowledge_base(knowledge_bases):
    while True:
        # Get unique options for domain
        domains = get_unique_items(knowledge_bases, 'Knowledge_Domain')
        domain_index = select_option(domains, "\nAvailable Knowledge Domains:")
        selected_domain = domains[domain_index]

        # Filter knowledge bases based on selected domain
        filtered_bases = [kb for kb in knowledge_bases if kb['Knowledge_Domain'] == selected_domain]

        # Get unique subjects for the selected domain
        subjects = get_unique_items(filtered_bases, 'Knowledge_Subject')
        subject_index = select_option(subjects, "\nAvailable Knowledge Subjects:")
        selected_subject = subjects[subject_index]

        # Filter knowledge bases based on selected subject
        filtered_bases = [kb for kb in filtered_bases if kb['Knowledge_Subject'] == selected_subject]

        # Get unique topics for the selected subject
        topics = get_unique_items(filtered_bases, 'Knowledge_Topic')
        topic_index = select_option(topics, "\nAvailable Knowledge Topics:")
        selected_topic = topics[topic_index]

        # Filter knowledge bases based on selected topic
        filtered_bases = [kb for kb in filtered_bases if kb['Knowledge_Topic'] == selected_topic]

        # Get unique sections for the selected topic
        sections = get_unique_items(filtered_bases, 'Knowledge_Section')
        section_index = select_option(sections, "\nAvailable Knowledge Sections:")
        selected_section = sections[section_index]

        # Find the matching knowledge base
        matching_kb = next((kb for kb in filtered_bases if kb['Knowledge_Section'] == selected_section), None)

        if not matching_kb:
            print("\nNo matching knowledge base found. Please try again.")
            continue

        return matching_kb['Filename'], selected_domain, selected_subject, selected_topic, selected_section

def get_current_month_log_file():
    today = datetime.datetime.today()
    month_year = today.strftime('%m-%Y')
    log_filename = f"{month_year}_data_logs.json"

    if not os.path.exists(log_filename):
        with open(log_filename, 'w') as file:
            json.dump({"Data_Logs": []}, file)  # Initialize with empty array
        print(f"Created new data log file: {log_filename}")

    return log_filename

# Function to start a review session
def initialize_review_session(selected_iana, selected_utc, session_id):
    directory_data = load_directory('directory.json')
    filename, domain, subject, topic, section = find_knowledge_base(directory_data)
    print(f"\nLoading questions from {filename}...")

    section_data = load_section_file(filename)
    is_priority_section = section_data.get('Is_Priority_Section', False)

    # Load questions from the matching JSON file
    questions = load_questions(filename)

    if not questions:
        print("No questions found in the selected knowledge base.")
        return
    else:
        print(f"Loaded {len(questions)} questions.")
    
    # Determine the review session mode, i.e. does the user want questions to be randomized or not
    while True:
        print("\nSelect your review session mode:\n[1] Random\n[2] Sequence\n")
        mode = input("Enter Answer: ")
        if mode in ['1', '2']:
            randomize = True if mode == '1' else False
            break
        else:
            print("Invalid input. Please enter '1' for Random or '2' for Sequence.")

    # Determine number of questions to run for given review session
    question_count = len(questions)
    while True:
        print("\nSelect the number of questions you want to review (in increments of 5, up to the total number):")

        # Generate options based on the number of questions available
        options = [(i, f"[-] {i}") for i in range(5, question_count + 1, 5)]
    
        # Add option for reviewing all available questions instead
        options.append((question_count, f"[-] All"))

        # Display options to the user
        for option, description in options:
            print(description)

        answer = input("\nEnter Answer: ")

        try:
            if answer.lower() == "all":
                print(answer)
                question_amount = question_count
                break
            else:
                question_amount = int(answer)
                if question_amount > question_count:
                    print(f"Invalid input. Maximum number of questions is {question_count}.")
                    continue
                elif question_amount % 5 != 0 or question_amount < 5:
                    print("Invalid input. Please select a number in increments of 5.")
                    continue
                break
        except ValueError:
            print("Invalid input. Please enter a number or the word 'All'.")
            continue

    # Initializing data log with all known information thus far
    log_entry = {
            "Review_Instance_Data_Log_ID": "",
            "IANA_Time_Zone": selected_iana,
            "UTC_Time_Zone": selected_utc,
            "Knowledge_Domain": domain,
            "Knowledge_Subject": subject,
            "Knowledge_Topic": topic,
            "Knowledge_Section": section,
            "File_Name": filename,
            "Date": "",
            "Score": "",
            "Letter_Grade": "",
            "Is_Priority_Section": is_priority_section,
            "Pass_Fail": "",
            "Total_Questions": question_amount,
            "Correct_Count": "",
            "Incorrect_Count": "",
            "Mistakes_Breakdown": [],
            "Start_Time": "",
            "End_Time": "",
            "Time_Elapsed": "",
            "Average_Time_Per_Question": "",
            "ISO_8601_Local_Timestamp": "",
            "ISO_8601_UTC_Timestamp": "",
            "HTTP_Date_Timestamp": "",
            "UUID4_Session_ID": session_id,
            "Session_Notes": ""
        }
    
    return questions, question_amount, log_entry, randomize

def track_review_session(selected_iana, selected_utc, log_entry):
    data_logs_filename = get_current_month_log_file()

    # Load existing logs or initialize if not exists
    if os.path.exists(data_logs_filename):
        with open(data_logs_filename, 'r') as file:
            data_logs = json.load(file)
    else:
        data_logs = {"Data_Logs": []}
    
    # Determine the numerical indicator for the new log entry
    log_position = len(data_logs["Data_Logs"]) + 1
    log_entry_number = f"{log_position:02}"  # Zero-padded to two digits

    # Gather information about the review session
    start_time = datetime.datetime.now().isoformat()

    # Get UTC time
    utc_start_time = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat() + 'Z'

    # Get HTTP Date timestamp (RFC 1123 format)
    http_date_time = datetime.datetime.now(pytz.timezone(selected_iana)).strftime('%a, %d %b %Y %H:%M:%S %Z')

    # Format the Data Log ID for the log_entry
    data_log_id = (f"{log_entry_number} | {http_date_time}")

    log_entry["Review_Instance_Data_Log_ID"] = data_log_id
    log_entry["ISO_8601_Local_Timestamp"] = start_time
    log_entry["ISO_8601_UTC_Timestamp"] = utc_start_time
    log_entry["HTTP_Date_Timestamp"] = http_date_time
    log_entry["Date"] = datetime.date.today().strftime("%m-%d-%Y")
    log_entry["Start_Time"] = start_time

    return data_logs_filename, data_logs

# Review questions interactively.
def review_session(questions, question_amount, log_entry, randomize=False):
    correct_count = 0
    question_index = 0
    score = ""
    letter_grade = ""
    pass_fail_status = ""
    missed_questions = []

    print(f"\nStarting review of {question_amount} questions...")

    # Shuffle questions if randomize is True
    if randomize:
        random.shuffle(questions)

    for question in questions:
        if (question_index < question_amount):
            question_index += 1
            correct = ask_question(question, question_index, missed_questions)
            if correct:
                correct_count += 1
        else:
            break

    print("Would you like to add notes to the session? [Y/N]")
    notes = input("Enter Answer: ")
    
    if notes == "Y":
        notes = input("Notes: ")
    else:
        notes = "N/A"

    # Calculate and display score
    if question_amount > 0:
        grade_percent = calculate_grade_percentage(correct_count, question_amount)
        score = f"{grade_percent:.2f}%"
        letter_grade = assign_letter_grade(grade_percent)
        print(f"\nReview complete. You answered {correct_count} out of {question_amount} questions correctly.")
        print(f"Grade Percentage: " + score)
        print(f"Letter Grade: {letter_grade}")

        # Acquire value of is_priority_section
        is_priority_section = log_entry["Is_Priority_Section"]

        # Determine pass or fail
        pass_fail_status = "Pass" if determine_pass_fail(letter_grade, is_priority_section) else "Fail"
        print(f"Pass / Fail: {pass_fail_status}")

        # Display priority section status
        priority_section_status = "Yes" if is_priority_section == True else "No"
        print(f"Priority Section: {priority_section_status}")

        # Display incorrect answers with correct answers
        if missed_questions:
            print("\nPost Review Learning Session (based on the questions you got incorrect)")
            for question in missed_questions:
                print(f"\nQuestion: {question['Question']}")
                print(f"Your Answer: {question['Your Answer(s)']}")
                print(f"Correct Answer(s): {question['Correct Answer(s)']}")

    # Calculate end time after the review session
    end_time = datetime.datetime.now().isoformat()
    time_elapsed = calculate_time_elapsed(log_entry["Start_Time"], end_time)

    log_entry["Session_Notes"] = notes
    log_entry["Score"] = score
    log_entry["Letter_Grade"] = letter_grade
    log_entry["Pass_Fail"] = pass_fail_status
    log_entry["Correct_Count"] = correct_count
    log_entry["Incorrect_Count"] = question_amount - correct_count
    log_entry["Mistakes_Breakdown"] = generate_mistakes_breakdown(missed_questions)
    log_entry["End_Time"] = end_time
    log_entry["Time_Elapsed"] = time_elapsed
    log_entry["Average_Time_Per_Question"] = calculate_average_time_per_question(time_elapsed, question_amount)

    return log_entry

# Finish and add data log to the data_logs.json file.
def log_review_session(data_logs_filename, data_logs, log_entry):
    # Append log entry to DataLogs
    data_logs["Data_Logs"].append(log_entry)

    # Save updated logs back to file
    save_json(data_logs_filename, data_logs)

    print("Review session logged successfully.")

# Review the same set of questions that were just recently reviewed.
def rerun_review_session(questions, question_amount, log_entry, randomize=False):
    
    new_log_entry = {
            "Review_Instance_Data_Log_ID": "",
            "IANA_Time_Zone": log_entry["IANA_Time_Zone"],
            "UTC_Time_Zone": log_entry["UTC_Time_Zone"],
            "Knowledge_Domain": log_entry["Knowledge_Domain"],
            "Knowledge_Subject": log_entry["Knowledge_Subject"],
            "Knowledge_Topic": log_entry["Knowledge_Topic"],
            "Knowledge_Section": log_entry["Knowledge_Section"],
            "File_Name": log_entry["File_Name"],
            "Date": log_entry["Date"],
            "Score": "",
            "Letter_Grade": "",
            "Is_Priority_Section": log_entry["Is_Priority_Section"],
            "Pass_Fail": "",
            "Total_Questions": log_entry["Total_Questions"],
            "Correct_Count": "",
            "Incorrect_Count": "",
            "Mistakes_Breakdown": [],
            "Start_Time": "",
            "End_Time": "",
            "Time_Elapsed": "",
            "Average_Time_Per_Question": "",
            "ISO_8601_Local_Timestamp": "",
            "ISO_8601_UTC_Timestamp": "",
            "HTTP_Date_Timestamp": "",
            "UUID4_Session_ID": log_entry["UUID4_Session_ID"],
            "Session_Notes": ""
    }

    selected_iana = log_entry["IANA_Time_Zone"]
    selected_utc = log_entry["UTC_Time_Zone"]

    data_logs_filename, data_logs = track_review_session(selected_iana, selected_utc, new_log_entry)
    review_session(questions, question_amount, new_log_entry)
    log_review_session(data_logs_filename, data_logs, new_log_entry)

def main():
    print_thoth_logo()

    # Ask user to select time zone
    selected_iana, selected_utc = get_time_zone()
    print(f"\nSelected time zone (IANA format): {selected_iana}")
    print(f"Selected time zone (UTC format): {selected_utc}")
    # Generate Session ID, which we be designated on all data logs created during this session.
    # This Session ID is re-generated every time the user opens a new session - which happens
    # whenever the program is run.
    session_id = generate_session_id()

    while True:
        # Begin Program Loop
        questions, question_amount, log_entry, randomize = initialize_review_session(selected_iana, selected_utc, session_id)
        data_logs_filename, data_logs = track_review_session(selected_iana, selected_utc, log_entry)
        review_session(questions, question_amount, log_entry, randomize)
        log_review_session(data_logs_filename, data_logs, log_entry)

        # Prompt for next action
        print("\nWhat would you like to do next?")
        print("[1] Try Again")
        print("[2] Practice Different Section")
        print("[3] Exit")

        while True:
            choice = input("\nEnter your choice (1-3): ")

            if choice == '1':
                rerun_review_session(questions, question_amount, log_entry)
            elif choice == '2':
                break  # Go back to select a different section
            elif choice == '3':
                print("\nThank you for using Thoth!")
                return  # Exit the program
            else:
                print("\nInvalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()  