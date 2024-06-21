import json

def load_directory(filename):
    """Load the directory of knowledge bases from a JSON file."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def load_questions(filename):
    """Load questions from a JSON file."""
    with open(filename, 'r') as file:
        data = json.load(file)
        questions = data.get("Questions", [])
    return questions

def load_section_file(filename):
    """Load a section file and return its content excluding 'Questions'."""
    with open(filename, 'r') as file:
        data = json.load(file)
        # Exclude 'Questions' from the loaded data
        section_data = {key: value for key, value in data.items() if key != 'Questions'}
    return section_data


def get_unique_items(data, key):
    """Extract unique items from a list of dictionaries based on a specific key."""
    return sorted(set(item[key] for item in data))

def print_numbered_options(options):
    """Print options in a numbered list."""
    for idx, option in enumerate(options, start=1):
        print(f"[{idx}] {option}")

def select_option(options, message):
    """Select an option from a list and return the index."""
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

def review_questions(questions, question_amount):
    """Review questions interactively."""
    question_count = len(questions)
    correct_count = 0

    print(f"\nStarting review of {question_amount} questions...\n")

    for index, question_data in enumerate(questions, start=1):
        if index > question_amount:
            break
        
        question_key = f"Question_{index}"
        question = question_data.get(question_key)

        if question:
            print(f"Question {index}: {question['Question']}")
            user_answer = input("Your Answer: ")

            # Get correct answers and split user answer by commas
            correct_answers = [ans.lower().replace(" ", "") for ans in question.get('Answers', [])]
            user_answers = [ans.strip().lower().replace(" ", "") for ans in user_answer.split(',')]

            # Check if all user answers (lowercase, no spaces) are in correct answers (lowercase, no spaces)
            if all(ans in correct_answers for ans in user_answers):
                print("Correct!")
                correct_count += 1
            else:
                print("Incorrect.")
        else:
            print(f"Error: Question '{question_key}' not found in the knowledge base.")

    return correct_count, question_amount

def calculate_grade_percentage(correct_count, question_amount):
    """Calculate the grade percentage based on correct answers."""
    if question_amount > 0:
        return (correct_count / question_amount) * 100
    else:
        return 0.0

def assign_letter_grade(grade_percent):
    """Assign letter grade based on the grade percentage."""
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

def determine_pass_fail(letter_grade, is_priority_section):
    """Determine pass or fail based on letter grade and section priority."""
    if is_priority_section:
        # Critical sections pass with C- or higher
        return letter_grade in {"A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-"}
    else:
        # Non-critical sections pass with D- or higher
        return letter_grade in {"A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-"}

def main():
    # Load directory of knowledge bases
    directory = 'directory.json'
    try:
        knowledge_data = load_directory(directory)
        knowledge_bases = knowledge_data["Knowledge_Bases"]
    except KeyError:
        print(f"Error: 'Knowledge_Bases' key not found in {directory}.")
        return

    while True:
        print("\n")
        print("|||||||||")
        print("T.H.O.T.H")
        print("|||||||||")

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

        filename = matching_kb['Filename']
        print(f"\nLoading questions from {filename}...")

        # Load questions from the matching JSON file
        questions = load_questions(filename)

        if not questions:
            print("No questions found in the selected knowledge base.")
            return
        else:
            print(f"Loaded {len(questions)} questions.")

        section_data = load_section_file(filename)
        # print(section_data)
        is_priority_section = section_data.get('IsPrioritySection', False)  # Check if section is critical
        # print(f"This is the priority section boolean: {is_priority_section}")

        # Review questions
        question_count = len(questions)
        while True:
            print("Select the number of questions you want to review (in increments of 5, up to the total number):")

            # Generate options based on the number of questions available
            options = [(i, f"[-] {i}") for i in range(5, question_count + 1, 5)]

            # Display options to the user
            for option, description in options:
                print(description)

            answer = input("\nEnter Answer: ")

            try:
                question_amount = int(answer)
                if question_amount > question_count:
                    print(f"Invalid input. Maximum number of questions is {question_count}.")
                    continue
                elif question_amount % 5 != 0 or question_amount < 5:
                    print("Invalid input. Please select a number in increments of 5.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            correct_count, _ = review_questions(questions, question_amount)

            # Calculate and display score
            if question_amount > 0:
                grade_percent = calculate_grade_percentage(correct_count, question_amount)
                letter_grade = assign_letter_grade(grade_percent)
                print(f"\nReview complete. You answered {correct_count} out of {question_amount} questions correctly.")
                print(f"Grade Percentage: {grade_percent:.2f}%")
                print(f"Letter Grade: {letter_grade}")

                # Determine pass or fail
                pass_fail_status = "Pass" if determine_pass_fail(letter_grade, is_priority_section) else "Fail"
                print(f"Pass / Fail: {pass_fail_status}")

                # Display priority section status
                priority_section_status = "Yes" if is_priority_section == True else "No"
                print(f"Priority Section: {priority_section_status}")

            # Prompt for next action
            print("\nWhat would you like to do next?")
            print("[1] Try Again")
            print("[2] Practice Different Section")
            print("[3] Exit")

            choice = input("\nEnter your choice (1-3): ")

            if choice == '1':
                continue  # Retry the same section
            elif choice == '2':
                break  # Go back to select a different section
            elif choice == '3':
                print("\nThank you for using Thoth!")
                return  # Exit the program
            else:
                print("\nInvalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()