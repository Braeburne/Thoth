import json

def load_directory(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def load_questions(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

def get_unique_items(data, key):
    # Extract unique items from a list of dictionaries based on a specific key
    return sorted(set(item[key] for item in data))

def main():
    # Load directory of knowledge bases
    directory = 'directory.json'
    knowledge_bases = load_directory(directory)['Knowledge_Bases']

    # Get unique options for domain, subject, topic, and section
    domains = get_unique_items(knowledge_bases, 'Knowledge_Domain')
    subjects = get_unique_items(knowledge_bases, 'Knowledge_Subject')
    topics = get_unique_items(knowledge_bases, 'Knowledge_Topic')
    sections = get_unique_items(knowledge_bases, 'Knowledge_Section')

    # Print available options for domain
    print("Available Knowledge Domains:")
    for domain in domains:
        print(f"[-] {domain}")

    # Prompt user for domain (case insensitive)
    domain = input("\nEnter Knowledge Domain: ").strip().lower()

    # Print available options for subject
    print("\nAvailable Knowledge Subjects:")
    for subject in subjects:
        print(f"[-] {subject}")

    # Prompt user for subject (case insensitive)
    subject = input("\nEnter Knowledge Subject: ").strip().lower()

    # Print available options for topic
    print("\nAvailable Knowledge Topics:")
    for topic in topics:
        print(f"[-] {topic}")

    # Prompt user for topic (case insensitive)
    topic = input("\nEnter Knowledge Topic: ").strip().lower()

    # Print available options for section
    print("\nAvailable Knowledge Sections:")
    for section in sections:
        print(f"[-] {section}")

    # Prompt user for section (case insensitive)
    section = input("\nEnter Knowledge Section: ").strip().lower()

    # Search for the matching knowledge base (case insensitive comparison)
    matching_kb = None
    for kb in knowledge_bases:
        if (domain == kb['Knowledge_Domain'].lower() and
            subject == kb['Knowledge_Subject'].lower() and
            topic == kb['Knowledge_Topic'].lower() and
            section == kb['Knowledge_Section'].lower()):
            matching_kb = kb
            break

    if matching_kb:
        filename = matching_kb['Filename']
        print(f"\nLoading questions from {filename}...")

        # Load questions from the matching JSON file
        questions = load_questions(filename)
        # Process questions further as needed
        print(f"Loaded {len(questions)} questions.")
    else:
        print("\nNo matching knowledge base found.")

    # Collect amount of questions that user wants to review
    question_count = len(questions)
    question_amount = 0
    print(f"\nWelcome to the {section} Section. It has {question_count} Questions total. How many questions do you want to review?")
    if question_count >= 10:
        print("[-] 5")
    
    if question_count >= 15:
        print("[-] 10")

    if question_count >= 20:
        print("[-] 15")

    if question_count >= 25:
        print("[-] 20")
    
    print("[-] All Questions")  
    answer = input("\nEnter Answer: ")

    if answer == 5:
        question_amount = answer
    elif answer == 10:
        question_amount = answer
    elif answer == 15:
        question_amount = answer
    elif answer == 20:
        question_amount = answer
    else:
        question_amount = question_count

    # Begin the review exercise
    for question in questions:
        

if __name__ == "__main__":
    main()