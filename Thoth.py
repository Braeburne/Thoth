import json

def load_directory(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def load_questions(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        questions = data.get("Questions", [])
    return questions

def get_unique_items(data, key):
    # Extract unique items from a list of dictionaries based on a specific key
    return sorted(set(item[key] for item in data))

def print_numbered_options(options):
    # Print options in a numbered list
    for idx, option in enumerate(options, start=1):
        print(f"[{idx}] {option}")

def main():
    # Load directory of knowledge bases
    directory = 'directory.json'
    try:
        knowledge_data = load_directory(directory)
        knowledge_bases = knowledge_data["Knowledge_Bases"]
    except KeyError:
        print(f"Error: 'Knowledge_Bases' key not found in {directory}.")
        return

    # Get unique options for domain, subject, topic, and section
    domains = get_unique_items(knowledge_bases, 'Knowledge_Domain')
    subjects = get_unique_items(knowledge_bases, 'Knowledge_Subject')
    topics = get_unique_items(knowledge_bases, 'Knowledge_Topic')
    sections = get_unique_items(knowledge_bases, 'Knowledge_Section')

    print("Welcome to the Thoth program. The only note you'll have to make is this. " +
        "For questions that have multiple answers, separate them with commas and no spaces. " +  
        "Example: 'Cloud Storage,Filestore,Persistent Disks.' Thank you. Enjoy.")

    # Print numbered options for domain
    print("\nAvailable Knowledge Domains:")
    print_numbered_options(domains)

    # Prompt user to select domain by number
    domain_choice = int(input("\nEnter Domain Number: "))
    selected_domain = domains[domain_choice - 1] if 1 <= domain_choice <= len(domains) else None

    # Filter knowledge bases based on selected domain
    filtered_bases = [kb for kb in knowledge_bases if kb['Knowledge_Domain'] == selected_domain]

    # If no bases match the selected domain, return
    if not filtered_bases:
        print("No matching knowledge bases found for the selected domain.")
        return

    # Get unique subjects, topics, and sections for the selected domain
    subjects = get_unique_items(filtered_bases, 'Knowledge_Subject')
    topics = get_unique_items(filtered_bases, 'Knowledge_Topic')
    sections = get_unique_items(filtered_bases, 'Knowledge_Section')

    # Print numbered options for subject
    print("\nAvailable Knowledge Subjects:")
    print_numbered_options(subjects)

    # Prompt user to select subject by number
    subject_choice = int(input("\nEnter Subject Number: "))
    selected_subject = subjects[subject_choice - 1] if 1 <= subject_choice <= len(subjects) else None

    # Filter knowledge bases based on selected subject
    filtered_bases = [kb for kb in filtered_bases if kb['Knowledge_Subject'] == selected_subject]

    # If no bases match the selected subject, return
    if not filtered_bases:
        print("No matching knowledge bases found for the selected subject.")
        return

    # Get unique topics and sections for the selected subject
    topics = get_unique_items(filtered_bases, 'Knowledge_Topic')
    sections = get_unique_items(filtered_bases, 'Knowledge_Section')

    # Print numbered options for topic
    print("\nAvailable Knowledge Topics:")
    print_numbered_options(topics)

    # Prompt user to select topic by number
    topic_choice = int(input("\nEnter Topic Number: "))
    selected_topic = topics[topic_choice - 1] if 1 <= topic_choice <= len(topics) else None

    # Filter knowledge bases based on selected topic
    filtered_bases = [kb for kb in filtered_bases if kb['Knowledge_Topic'] == selected_topic]

    # If no bases match the selected topic, return
    if not filtered_bases:
        print("No matching knowledge bases found for the selected topic.")
        return

    # Get unique sections for the selected topic
    sections = get_unique_items(filtered_bases, 'Knowledge_Section')

    # Print numbered options for section
    print("\nAvailable Knowledge Sections:")
    print_numbered_options(sections)

    # Prompt user to select section by number
    section_choice = int(input("\nEnter Section Number: "))
    selected_section = sections[section_choice - 1] if 1 <= section_choice <= len(sections) else None

    # Find the matching knowledge base
    matching_kb = None
    for kb in filtered_bases:
        if (kb['Knowledge_Domain'] == selected_domain and
            kb['Knowledge_Subject'] == selected_subject and
            kb['Knowledge_Topic'] == selected_topic and
            kb['Knowledge_Section'] == selected_section):
            matching_kb = kb
            break
        else:
            print("\nNo matching knowledge base found.")
            return

    if matching_kb:
        filename = matching_kb['Filename']
        print(f"\nLoading questions from {filename}...")

    # Load questions from the matching JSON file
    questions = load_questions(filename)

    if not questions:
        print("No questions found in the selected knowledge base.")
        return
    else:
        print(f"Loaded {len(questions)} questions.")

    # Collect amount of questions that user wants to review
    question_count = len(questions)
    question_amount = 0
    print(f"\nWelcome to the {selected_section} Section. It has {question_count} questions total.")
    print("Select the number of questions you want to review:")

    # Generate options based on the number of questions available
    options = [(i, f"[-] {i}") for i in range(1, question_count + 1)]

    # Display options to the user
    for option, description in options:
        print(description)

    answer = input("\nEnter Answer: ")

    try:
        question_amount = int(answer)
    except ValueError:
        print("Invalid input. Defaulting to review all questions.")
        question_amount = question_count

    if question_amount > question_count:
        question_amount = question_count

    # Begin the review exercise
    print(f"\nStarting review of {question_amount} questions...\n")

    correct_count = 0

    # Iterate over the range of question_amount (1 to question_amount + 1)
    for index in range(1, question_amount + 1):
        question_key = f"Question_{index}"  # Construct the question key
        if index <= len(questions):
            question_data = questions[index - 1]  # Access the question dictionary
            question = question_data.get(question_key)
            if question:
                print(f"Question {index}: {question['Question']}")
                user_answer = input("Your Answer: ")

                # Get correct answers and split user answer by commas
                correct_answers = question.get('Answers', [])
                user_answers = [ans.strip() for ans in user_answer.split(',')]

                # Check if all user answers are in correct answers
                if all(ans in correct_answers for ans in user_answers):
                    print("Correct!")
                    correct_count += 1
                else:
                    print("Incorrect.")
            else:
                print(f"Error: Question '{question_key}' not found in the knowledge base.")
        else:
            print(f"Error: Question index '{index}' out of range.")

    # Calculate and display score
    if question_amount > 0:
        score = correct_count / question_amount * 100
        print(f"\nReview complete. You answered {correct_count} out of {question_amount} questions correctly.")
        print(f"Score: {score:.2f}%")

    print("\nThank you for using Thoth!")

if __name__ == "__main__":
    main()