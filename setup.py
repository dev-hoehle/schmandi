import json
import webbrowser

def get_user_input(prompt):
    return input(prompt + " ")

def open_link_in_browser(url):
    webbrowser.open(url)

def main():
    print("Welcome to the configuration setup!")

    # Open Discord Developer Portal link in browser
    open_link_in_browser("https://discord.com/developers/applications")
    token = get_user_input("Enter your Discord bot token from the above link:")
    
    # Open Tenor API quickstart guide link in browser
    open_link_in_browser("https://developers.google.com/tenor/guides/quickstart")
    tenor_key = get_user_input("Enter your Tenor API key:")
    tenor_name = get_user_input("Enter your Tenor App Name:")

    greetmembers = get_user_input("Greet members? (True/False):").lower() == "true"

    config_data = {
        "token": token,
        "tenor_key": tenor_key,
        "tenor_name": tenor_name,
        "greetmembers": greetmembers
    }

    with open("config.json", "w") as config_file:
        json.dump(config_data, config_file, indent=4)

    print("Configuration saved to 'config.json'. Setup complete!")

if __name__ == "__main__":
    main()
