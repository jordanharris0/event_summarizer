import os  # allows access to env variables
from dotenv import load_dotenv  # loads env variables from .env file
from openai import OpenAI  # OpenAI API client
from colorama import init, Fore, Style  # for colored terminal output

# Initialize colorama for colored output
init(autoreset=True)

# load API key from .env file
load_dotenv()

# prompt user for API key to configure OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print(Fore.RED + Style.BRIGHT + "⚠️  No OpenAI API key found.\n")
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT +
          "💡 Tip: You can create a '.env' file and add:")
    print(Fore.LIGHTWHITE_EX + "OPENAI_API_KEY=your-api-key-here\n")

    while not api_key:
        api_key = input(Fore.LIGHTWHITE_EX +
                        "🔑 Please enter your OpenAI API key: ").strip()
        if not api_key:
            print(Fore.RED + Style.BRIGHT +
                  "❌ API key is required to proceed.\n")

    # save api_key to .env
    try:
        with open(".env", "a") as env_file:
            env_file.write(f"\nOPENAI_API_KEY={api_key}\n")
        print(Fore.GREEN + "✅ Your API key was saved to .env for future use.\n")
    except Exception as e:
        print(Fore.RED + f"⚠️  Could not save API key to .env: {e}\n")

client = OpenAI(api_key=api_key)


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
