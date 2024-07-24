import json
import datetime
import pytz

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

def redesign_json(selected_iana):
    # Get HTTP Date timestamp (RFC 1123 format)
    http_date_time = datetime.datetime.now(pytz.timezone(selected_iana)).strftime('%a, %d %b %Y %H:%M:%S %Z')

    # Get file that user wants converted
    file_name = input("Enter the name of the file you want re-designed (including file extension): ")
    print(f"file_name: {file_name}")

    # Load the provided JSON file
    file_path = f'{file_name}'
    print(f"file_path: {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Transform the structure of each question to match the new format
    transformed_questions = []
    for idx, question in enumerate(data['Questions']):
        key = list(question.keys())[0]  # Get the question key
        question_content = question[key]
        print(f"question_content: {question_content}")
        
        # Determine if there are multiple correct answers
        multiple_correct_answers = isinstance(question_content['Answers'], list) and len(question_content['Answers']) > 1
    
        if question_content['HasOptions']:
            # Determine the Answers List
            answer_list = [{"id": i + 1, "text": option} for i, option in enumerate(question_content.get('Options', question_content['Answers']))]
            print(f"answer_list: {answer_list}")
            
            # Determine the correct answer IDs
            correct_answer_ids = [
                option['id'] for option in answer_list
                if option['text'] in question_content['Answers']
            ]

            transformed_question = {
                f"Question_{idx + 1}": {
                    "Prompt": question_content['Question'],
                    "Answers": answer_list,
                    "HasGraphic": question_content['HasGraphic'],
                    "Graphic": question_content['Graphic'] if question_content['HasGraphic'] else None,
                    "OrderAgnostic": question_content['OrderAgnostic'],
                    "MultipleCorrectAnswers": multiple_correct_answers,
                    "CorrectAnswerIDs": correct_answer_ids
                }
            }
        else:
            # Determine the Answers List
            answer_list = [{"id": i + 1, "text": option} for i, option in enumerate(question_content.get('Answers', question_content['Answers']))]
            print(f"answer_list: {answer_list}")
            
            # Determine the correct answer IDs
            correct_answer_ids = [
                option['id'] for option in answer_list
                if option['text'] in question_content['Answers']
            ]
            
            transformed_question = {
                f"Question_{idx + 1}": {
                    "Prompt": question_content['Question'],
                    "Answers": answer_list,
                    "HasGraphic": question_content['HasGraphic'],
                    "Graphic": question_content['Graphic'] if question_content['HasGraphic'] else None,
                    "OrderAgnostic": question_content['OrderAgnostic'],
                    "MultipleCorrectAnswers": multiple_correct_answers,
                    "CorrectAnswerIDs": correct_answer_ids
                }
            }
        transformed_questions.append(transformed_question)

    # Create the new JSON structure
    transformed_data = {
        "Knowledge_Domain": data['Knowledge_Domain'],
        "Knowledge_Subject": data['Knowledge_Subject'],
        "Knowledge_Topic": data['Knowledge_Topic'],
        "Knowledge_Section": data['Knowledge_Section'],
        "Is_Priority_Section": data['Is_Priority_Section'],
        "Questions": transformed_questions
    }

    file_name = file_name.removesuffix(".json")
    print(f"file_name with suffixed removed: {file_name}")
    print(f"http_date_time: {http_date_time}")
    # Apply all transformations in one go
    transformed_http_date_time = http_date_time .replace(" ", "_") \
                                                .replace(":", "_") \
                                                .replace(",", "")
    print(f"transformed_http_date_time: {transformed_http_date_time}")
    transformed_file_name = f"transformed_{file_name}_{transformed_http_date_time}.json"
    print(f"transformed_file_name: {transformed_file_name}")

    # Save the transformed data to a new JSON file
    output_path = f'Sandbox/{transformed_file_name}'
    with open(output_path, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)
    
    print(f"Transformed file saved to: {output_path}")

selected_iana, selected_utc = get_time_zone()
redesign_json(selected_iana)

# def main():
#     selected_iana, selected_utc = get_time_zone()
#     redesign_json(selected_iana)

# if __name__ == "__main__":
#     main()  