import json
import logging

from groq import Groq


# =========================================================
# GROQ API KEY
# =========================================================

GROQ_API_KEY = "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"


# =========================================================
# INPUT FILES
# =========================================================

TEXT_JSON = "extracted_text.json"

EQUATION_JSON = "extracted_equation.json"


# =========================================================
# LOGGER SETUP
# =========================================================

# Configure and return logger object
def setup_logger():

    logger = logging.getLogger(
        "GroqPhysicsExplainer"
    )

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            console_handler
        )

    return logger


logger = setup_logger()


# =========================================================
# LOAD JSON FILE
# =========================================================

# Load JSON file safely
def load_json_file(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as json_file:

            data = json.load(json_file)

        logger.info(
            f"Loaded JSON file: {file_path}"
        )

        return data

    except FileNotFoundError:

        logger.error(
            f"File not found: {file_path}"
        )

        return {}

    except Exception as error:

        logger.error(
            f"Error loading JSON: {error}"
        )

        return {}


# =========================================================
# NORMALIZE EQUATION NUMBER
# =========================================================

# Normalize equation input
def normalize_equation_number(
    equation_input
):

    cleaned_input = equation_input.strip()

    # Add opening bracket
    if not cleaned_input.startswith("("):

        cleaned_input = (
            "(" + cleaned_input
        )

    # Add closing bracket
    if not cleaned_input.endswith(")"):

        cleaned_input = (
            cleaned_input + ")"
        )

    return cleaned_input


# =========================================================
# FIND EQUATION DATA
# =========================================================

# Find equation information
def find_equation_data(
    equation_name,
    equation_data
):

    equations = equation_data.get(
        "Dict_Equations",
        {}
    )

    normalized_name = (
        normalize_equation_number(
            equation_name
        )
    )

    if normalized_name in equations:

        logger.info(
            f"Found equation: {normalized_name}"
        )

        return (
            normalized_name,
            equations[normalized_name]
        )

    logger.warning(
        f"Equation not found: {normalized_name}"
    )

    return None, None


# =========================================================
# FIND TOPIC DATA
# =========================================================

# Find topic information
def find_topic_data(
    topic_name,
    equation_data
):

    topics = equation_data.get(
        "Dict_Topics",
        {}
    )

    # Case-insensitive search
    for topic in topics:

        if topic.lower() == topic_name.lower():

            logger.info(
                f"Found topic: {topic}"
            )

            return (
                topic,
                topics[topic]
            )

    logger.warning(
        f"Topic not found: {topic_name}"
    )

    return None, None


# =========================================================
# GET PAGE TEXT
# =========================================================

# Get full text from page numbers
def get_page_text(
    page_numbers,
    extracted_text
):

    combined_text = ""

    for page_number in page_numbers:

        page_key = str(page_number)

        if page_key in extracted_text:

            combined_text += (
                "\n\n"
                + extracted_text[page_key]
            )

    return combined_text


# =========================================================
# BUILD PROMPT
# =========================================================

# Build prompt for Groq model
def build_prompt(

    equation_name,
    topic_name,

    equation_info,
    topic_info,

    equation_text,
    topic_text
):

    # -----------------------------------------------------
    # CASE 1
    # ONLY EQUATION
    # -----------------------------------------------------

    if equation_name and not topic_name:

        prompt = f"""
You are an expert physics teacher.

The student asked about this equation:

{equation_name}

Equation text:

{equation_info.get('equation_text', '')}

Related topics:

{equation_info.get('related_topics', [])}

Full textbook content related to this equation:

{equation_text}

Explain:
1. Meaning of equation
2. Physical intuition
3. Dependencies between concepts
4. Relationship to related topics
5. Why this equation matters
"""

        return prompt

    # -----------------------------------------------------
    # CASE 2
    # ONLY TOPIC
    # -----------------------------------------------------

    if topic_name and not equation_name:

        prompt = f"""
You are an expert physics teacher.

The student asked about this topic:

{topic_name}

Related equations:

{topic_info.get('related_equations', [])}

Full textbook content related to this topic:

{topic_text}

Explain:
1. Meaning of topic
2. Related equations
3. Physical intuition
4. Dependencies between concepts
5. Important relationships
"""

        return prompt

    # -----------------------------------------------------
    # CASE 3
    # BOTH EQUATION + TOPIC
    # -----------------------------------------------------

    if equation_name and topic_name:

        prompt = f"""
You are an expert physics teacher.

The student asked about:

Equation:
{equation_name}

Topic:
{topic_name}

Equation text:

{equation_info.get('equation_text', '')}

Related topics:

{equation_info.get('related_topics', [])}

Related equations:

{topic_info.get('related_equations', [])}

Equation textbook content:

{equation_text}

Topic textbook content:

{topic_text}

Explain:
1. Relationship between topic and equation
2. Physical interpretation
3. Dependencies between concepts
4. Important intuition
5. How concepts connect
"""

        return prompt

    return "No valid input."


# =========================================================
# SEND REQUEST TO GROQ
# =========================================================

# Send prompt to Groq API
def ask_groq(prompt):

    try:

        client = Groq(
            api_key=GROQ_API_KEY
        )

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        output = (
            response
            .choices[0]
            .message
            .content
        )

        logger.info(
            "Groq response received"
        )

        return output

    except Exception as error:

        logger.error(
            f"Groq API error: {error}"
        )

        return "Groq request failed."
# =========================================================
# MAIN PROGRAM
# =========================================================

# Main execution function
def main():

    logger.info(
        "Starting Groq physics explanation system"
    )

    # -----------------------------------------------------
    # LOAD JSON FILES
    # -----------------------------------------------------

    extracted_text = load_json_file(
        TEXT_JSON
    )

    equation_data = load_json_file(
        EQUATION_JSON
    )

    # -----------------------------------------------------
    # USER INPUT
    # -----------------------------------------------------

    print("\nSearch for equation or topic\n")

    equation_input = input(
        "Enter equation number (or press Enter): "
    ).strip()

    topic_input = input(
        "Enter topic name (or press Enter): "
    ).strip()

    # -----------------------------------------------------
    # STORAGE VARIABLES
    # -----------------------------------------------------

    equation_name = None
    equation_info = None

    topic_name = None
    topic_info = None

    equation_text = ""
    topic_text = ""

    # -----------------------------------------------------
    # EQUATION LOOKUP
    # -----------------------------------------------------

    if equation_input:

        equation_name, equation_info = (
            find_equation_data(
                equation_input,
                equation_data
            )
        )

        if equation_info:

            equation_text = get_page_text(

                equation_info.get(
                    "pages",
                    []
                ),

                extracted_text
            )

        else:

            print(
                "\nEquation not found.\n"
            )

    # -----------------------------------------------------
    # TOPIC LOOKUP
    # -----------------------------------------------------

    if topic_input:

        topic_name, topic_info = (
            find_topic_data(
                topic_input,
                equation_data
            )
        )

        if topic_info:

            topic_text = get_page_text(

                topic_info.get(
                    "pages",
                    []
                ),

                extracted_text
            )

        else:

            print(
                "\nTopic not found.\n"
            )

    # -----------------------------------------------------
    # STOP IF NOTHING FOUND
    # -----------------------------------------------------

    if (
        equation_info is None
        and
        topic_info is None
    ):

        logger.warning(
            "No valid equation or topic found"
        )

        return

    # -----------------------------------------------------
    # BUILD PROMPT
    # -----------------------------------------------------

    prompt = build_prompt(

        equation_name,
        topic_name,

        equation_info if equation_info else {},
        topic_info if topic_info else {},

        equation_text,
        topic_text
    )

    logger.info(
        "Prompt built successfully"
    )

    # -----------------------------------------------------
    # SEND TO GROQ
    # -----------------------------------------------------

    print(
        "\nSending request to Groq...\n"
    )

    explanation = ask_groq(
        prompt
    )

    # -----------------------------------------------------
    # DISPLAY RESULT
    # -----------------------------------------------------

    print("\n==============================")
    print("PHYSICS EXPLANATION")
    print("==============================\n")

    print(explanation)


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    main()
