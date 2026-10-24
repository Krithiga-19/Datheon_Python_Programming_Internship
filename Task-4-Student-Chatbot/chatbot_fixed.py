import json
import re
from pathlib import Path

FAQ_FILE = Path(__file__).resolve().parent / "sample_faq.json"

EXIT_WORDS = {"bye", "exit", "quit", "goodbye"}

DEFAULT_ANSWERS = {
    "hours": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST.",
    "submit_project": "You can submit your public GitHub repository link through your Student Workspace.",
    "certificate": "Certificates are reviewed and issued within 3-5 business days after your code review.",
}

INTENT_KEYWORDS = {
    "hours": [
        r"\bhours?\b", r"\bworking\b", r"\btimings?\b",
        r"\bopen\b", r"\bclose\b", r"\bbusiness hours\b",
        r"\boperating\b",
    ],
    "submit_project": [
        r"\bsubmit\b", r"\bsubmission\b", r"\bturn in\b",
        r"\bupload\b", r"\binternship project\b",
        r"\bgithub\b", r"\brepository\b", r"\brepo\b",
    ],
    "certificate": [
        r"\bcertificate\b", r"\bcertification\b",
    ],
}


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s'-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_faq_data():
    try:
        with FAQ_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("The JSON root must be an object.")
        if not isinstance(data.get("faqs", []), list):
            raise ValueError("'faqs' must be a list.")
        data.setdefault("greetings", [])
        data.setdefault("faqs", [])
        print(f"FAQ dataset loaded: {FAQ_FILE}")
        return data

    except FileNotFoundError:
        print(f"Warning: {FAQ_FILE.name} was not found. Using built-in FAQ answers.")
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Warning: Could not read FAQ JSON ({error}). Using built-in FAQ answers.")

    return {"greetings": [], "faqs": []}


def find_intents(message):
    text = normalize(message)
    intents = []

    # Detect hours questions.
    if any(re.search(pattern, text) for pattern in INTENT_KEYWORDS["hours"]):
        intents.append("hours")

    # Project submission requires both a project-related term and an action,
    # so the word "project" alone does not trigger the answer.
    has_project = bool(re.search(
        r"\b(project|internship|github|repository|repo)\b", text
    ))
    has_action = bool(re.search(
        r"\b(submit|submission|turn in|upload|send)\b", text
    ))
    if has_project and has_action:
        intents.append("submit_project")

    if any(re.search(pattern, text) for pattern in INTENT_KEYWORDS["certificate"]):
        intents.append("certificate")

    # Remove duplicates while preserving order.
    return list(dict.fromkeys(intents))


def answer_from_json(intent, faq_data):
    """Find a matching FAQ entry. Return None if the JSON has no match."""
    question_terms = {
        "hours": ["hours of operation", "hours", "timings", "working hours"],
        "submit_project": ["submit my internship project", "internship project", "github"],
        "certificate": ["certificate", "certification"],
    }

    for faq in faq_data.get("faqs", []):
        if not isinstance(faq, dict):
            continue

        question = normalize(str(faq.get("question", "")))
        answer = faq.get("answer")

        if (
            isinstance(answer, str)
            and answer.strip()
            and any(term in question for term in question_terms[intent])
        ):
            return answer.strip()

    return None


def is_greeting(message, faq_data):
    text = normalize(message)
    greetings = {
        normalize(item)
        for item in faq_data.get("greetings", [])
        if isinstance(item, str)
    }
    greetings.update({
        "hello", "hi", "hey", "good morning",
        "good afternoon", "good evening",
    })
    return text in greetings


def respond(message, faq_data):
    text = normalize(message)

    if text in EXIT_WORDS:
        return None

    if not text:
        return "Please type a question so I can help."

    if is_greeting(message, faq_data):
        return (
            "Hello! I'm the student support assistant. "
            "Ask me about working hours, project submission, or certificates."
        )

    if "thank" in text:
        return "You're welcome! Is there anything else I can help you with?"

    if "help" in text or "what can you do" in text:
        return (
            "I can answer questions about business hours, internship project "
            "submission, and certificate timelines."
        )

    intents = find_intents(message)
    answers = []

    for intent in intents:
        answer = answer_from_json(intent, faq_data)
        if answer is None:
            answer = DEFAULT_ANSWERS[intent]
        if answer not in answers:
            answers.append(answer)

    if answers:
        return "\n".join(f"- {answer}" for answer in answers)

    return (
        "Sorry, I didn't understand that question. Please ask about business "
        "hours, how to submit your internship project, or when you'll receive "
        "your certificate."
    )


def main():
    faq_data = load_faq_data()

    print("=" * 50)
    print("STUDENT SUPPORT CHATBOT")
    print("=" * 50)
    print("Ask about working hours, project submission, or certificates.")
    print("Type 'bye', 'exit', or 'quit' to close.")
    print("-" * 50)

    while True:
        try:
            message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        answer = respond(message, faq_data)
        if answer is None:
            print("Bot: Goodbye! Thank you for chatting.")
            break

        print(f"Bot: {answer}")


if __name__ == "__main__":
    main()
