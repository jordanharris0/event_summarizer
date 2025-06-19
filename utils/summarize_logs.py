import os  # allows access to env variables
from dotenv import load_dotenv  # loads env variables from .env file
from openai import OpenAI  # OpenAI API client

# load API key from .env file
load_dotenv()

# configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_logs(log_string: str) -> str:
    """
    Summarizes the provided log string using OpenAI's GPT model.

    Args:
        log_string (str): The string containing logs to be summarized.

    Returns:
        str: Summary of the logs.
    """
    if not log_string:
        return "No logs provided for summarization."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at summarizing Windows Event Viewer logs into clear, concise reports."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following logs:\n\n{log_string}"
                }
            ],
            max_tokens=500,
            temperature=0.5
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error summarizing logs: {str(e)}"
