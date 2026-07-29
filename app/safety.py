# Keywords indicating a potential medical emergency
EMERGENCY_KEYWORDS = [
    "chest pain",
    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "severe bleeding",
    "heavy bleeding",
    "unconscious",
    "not breathing",
    "stroke",
    "seizure",
    "heart attack",
    "severe burn",
    "choking",
    "anaphylaxis",
    "poisoning",
    "no pulse",
    "collapsed",
    "overdose"
]


EMERGENCY_RESPONSE = (
    "🚨 **This sounds like it could be a medical emergency.**\n\n"
    "Please call your local emergency number immediately (e.g., 911 / 108 / 112) "
    "or go to the nearest emergency room right away. If you're with the person, "
    "stay with them and follow emergency dispatcher instructions.\n\n"
    "I'm an AI assistant and cannot provide emergency medical care."
)


# Keywords indicating possible self-harm or suicidal thoughts
SELF_HARM_KEYWORDS = [
    "suicidal",
    "suicide",
    "want to kill myself",
    "want to die",
    "don't want to live",
    "end my life",
    "hurting myself",
    "self harm",
    "self-harm",
    "kill myself"
]


SELF_HARM_RESPONSE = (
    "💙 I'm really sorry you're feeling this way. You don't have to go through this alone.\n\n"
    "**Please reach out right now to someone who can help:**\n"
    "- If you're in immediate danger, call your local emergency number.\n"
    "- You can also reach a crisis helpline — for example, in India: **iCall (9152987821)** "
    "or **AASRA (9820466726)**; in the US: **988 Suicide & Crisis Lifeline**.\n"
    "- Please also consider reaching out to a trusted friend, family member, or counselor.\n\n"
    "I'm an AI and can't provide crisis support myself, but real help is available and you deserve it."
)


# Phrases suggesting the user wants a definitive diagnosis
DIAGNOSIS_TRIGGERS = [
    "do i have",
    "am i having",
    "diagnose me",
    "what disease do i have",
    "tell me what's wrong with me",
    "what illness do i have"
]


def check_emergency(user_text: str) -> bool:
    text = user_text.lower()
    return any(keyword in text for keyword in EMERGENCY_KEYWORDS)


def check_self_harm(user_text: str) -> bool:
    text = user_text.lower()
    return any(keyword in text for keyword in SELF_HARM_KEYWORDS)


def check_diagnosis_request(user_text: str) -> bool:
    text = user_text.lower()
    return any(phrase in text for phrase in DIAGNOSIS_TRIGGERS)


DIAGNOSIS_GUARD_NOTE = (
    "\n\n(Note: I can't provide a diagnosis. I'll explain general possibilities, "
    "but please see a doctor for an accurate diagnosis.)"
)