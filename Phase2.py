import json
import re
import logging


# =========================================================
# INPUT / OUTPUT FILES
# =========================================================

INPUT_JSON = "extracted_text.json"

OUTPUT_JSON = "extracted_equation.json"


# =========================================================
# LOGGER SETUP
# =========================================================

# Configure and return logger object
def setup_logger():

    logger = logging.getLogger("EquationExtractor")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


logger = setup_logger()


# =========================================================
# LOAD JSON FILE
# =========================================================

# Load extracted text JSON file
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
            f"Error loading JSON file: {error}"
        )

        return {}


# =========================================================
# IGNORE INVALID PAGES
# =========================================================

# Check whether page should be ignored
def should_ignore_page(text):

    ignore_words = [
        "index",
        "contents",
        "appendix",
        "bibliography",
        "references",
        "acknowledgement",
        "acknowledgment"
    ]

    lower_text = text.lower()

    for word in ignore_words:

        if word in lower_text[:1000]:
            return True

    return False


# =========================================================
# EQUATION NUMBER EXTRACTION
# =========================================================

# Extract equation numbers using regex
def extract_equation_numbers(text):

    equation_pattern = r"\(\d+\.\d+\)"

    equation_numbers = re.findall(
        equation_pattern,
        text
    )

    return equation_numbers


# =========================================================
# EQUATION EXTRACTION
# =========================================================

# Extract equation-like expressions using regex
def extract_equations(text):

    equation_regex = (
        r"[A-Za-z0-9∇∆∂εμσπλφθωΩαβγρ→+\-*/=<>·^]+"
        r"\s*=\s*"
        r"[A-Za-z0-9∇∆∂εμσπλφθωΩαβγρ→+\-*/=<>·^ ]+"
    )

    equations = re.findall(
        equation_regex,
        text
    )

    return equations


# =========================================================
# TOPIC EXTRACTION
# =========================================================

# Extract possible topics using regex
def extract_topics(text):

    topic_pattern = r"\b[A-Z][a-zA-Z]{3,}(?:\s+[A-Z][a-zA-Z]{3,})*\b"

    topics = re.findall(
        topic_pattern,
        text
    )

    return topics


# =========================================================
# FIND CLOSEST TOPIC
# =========================================================

# Find closest topic near equation
def find_closest_topic(text, equation_position):

    nearby_text = text[
        max(0, equation_position - 300):
        equation_position + 300
    ]

    topics = extract_topics(nearby_text)

    if topics:
        return topics[0]

    return "Unknown Topic"


# =========================================================
# BUILD DICTIONARIES
# =========================================================

# Build topic and equation dictionaries
def build_dictionaries(extracted_pages):

    Dict_Equations = {}

    Dict_Topics = {}

    # Loop through every page
    for page_number, text in extracted_pages.items():

        logger.info(
            f"Processing page {page_number}"
        )

        # Ignore invalid pages
        if should_ignore_page(text):

            logger.info(
                f"Ignored page {page_number}"
            )

            continue

        # Extract equation numbers
        equation_numbers = extract_equation_numbers(
            text
        )

        # Extract equations
        equations = extract_equations(text)

        # Extract topics
        topics = extract_topics(text)

        # -------------------------------------------------
        # STORE TOPICS
        # -------------------------------------------------

        for topic in topics:

            if topic not in Dict_Topics:

                Dict_Topics[topic] = {
                    "frequency": 0,
                    "pages": [],
                    "related_equations": []
                }

            Dict_Topics[topic]["frequency"] += 1

            if page_number not in Dict_Topics[topic]["pages"]:

                Dict_Topics[topic]["pages"].append(
                    page_number
                )

        # -------------------------------------------------
        # STORE EQUATIONS
        # -------------------------------------------------

        for index in range(
            min(len(equation_numbers), len(equations))
        ):

            equation_number = equation_numbers[index]

            equation_text = equations[index]

            # Find equation position
            equation_position = text.find(
                equation_text
            )

            # Find closest topic
            closest_topic = find_closest_topic(
                text,
                equation_position
            )

            if equation_number not in Dict_Equations:

                Dict_Equations[equation_number] = {
                    "equation_text": equation_text,
                    "frequency": 0,
                    "pages": [],
                    "related_topics": []
                }

            # Increase frequency
            Dict_Equations[equation_number][
                "frequency"
            ] += 1

            # Store page number
            if (
                page_number
                not in Dict_Equations[equation_number]["pages"]
            ):

                Dict_Equations[equation_number][
                    "pages"
                ].append(page_number)

            # Store related topic
            if (
                closest_topic
                not in Dict_Equations[equation_number][
                    "related_topics"
                ]
            ):

                Dict_Equations[equation_number][
                    "related_topics"
                ].append(closest_topic)

            # Add equation to topic dictionary
            if closest_topic in Dict_Topics:

                if (
                    equation_number
                    not in Dict_Topics[closest_topic][
                        "related_equations"
                    ]
                ):

                    Dict_Topics[closest_topic][
                        "related_equations"
                    ].append(equation_number)

    return Dict_Equations, Dict_Topics


# =========================================================
# SAVE JSON FILE
# =========================================================

# Save extracted dictionaries to JSON
def save_json(data, output_file):

    try:

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as json_file:

            json.dump(
                data,
                json_file,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            f"Saved JSON file: {output_file}"
        )

    except Exception as error:

        logger.error(
            f"Error saving JSON file: {error}"
        )


# =========================================================
# MAIN FUNCTION
# =========================================================

# Main processing pipeline
def process_equation_extraction():

    # Load extracted text
    extracted_pages = load_json_file(
        INPUT_JSON
    )

    if not extracted_pages:

        logger.error(
            "No extracted text data found"
        )

        return

    # Build dictionaries
    Dict_Equations, Dict_Topics = build_dictionaries(
        extracted_pages
    )

    # Final output dictionary
    final_output = {
        "Dict_Equations": Dict_Equations,
        "Dict_Topics": Dict_Topics
    }

    # Save output JSON
    save_json(
        final_output,
        OUTPUT_JSON
    )

    logger.info(
        "Equation extraction completed successfully"
    )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    process_equation_extraction()     