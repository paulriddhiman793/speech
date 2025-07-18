# J.A.R.V.I.S. - AI Speech Assistant

This is a simple AI speech assistant, inspired by J.A.R.V.I.S., that can perform various tasks on your computer based on voice commands.

## Functionalities

### System Control
*   **Volume & Brightness**: Adjust the system volume and screen brightness.
*   **Power Management**: Shutdown, restart, or put the computer to sleep.

### File Management
*   **File & Folder Operations**: Create, rename, and delete files and folders.
*   **File Search**: Search for files on your computer.

### Productivity & Information
*   **Web Search & Browsing**: Open Google and YouTube, and perform searches in a specific Chrome profile.
*   **Wikipedia**: Get summaries from Wikipedia on any topic.
*   **Calculator**: Perform basic mathematical calculations.
*   **Time**: Get the current time.
*   **Dictionary**: Look up word definitions.
*   **Chat**: Have a conversation with the assistant.
*   **News**: Get the latest world and financial news.
*   **Email**: Send emails through your configured account.

### Entertainment
*   **Music**: Play music from a local directory or on Spotify.

## Setup and Usage

1.  **Prerequisites**: Ensure you have Python installed on your system.

2.  **Install Dependencies**: Open a terminal in the project directory and install the required libraries using the following command:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Add Music**: Place your favorite music files (e.g., `.mp3` files) into the `music` directory.

4.  **Run the Assistant**: Execute the main script to start the assistant:
    ```bash
    python main.py
    ```

## Voice Commands

### System Control
*   `"set volume to [level]"`: Adjusts the system volume (0-100).
*   `"set brightness to [level]"`: Adjusts the screen brightness (0-100).
*   `"shutdown"`: Shuts down the computer.
*   `"restart"`: Restarts the computer.
*   `"sleep"`: Puts the computer to sleep.

### File Management
*   `"create file [filename]"`: Creates a new file.
*   `"create folder [foldername]"`: Creates a new folder.
*   `"rename file [old_name] to [new_name]"`: Renames a file.
*   `"delete file [filename]"`: Deletes a file.
*   `"search for file [filename]"`: Searches for a file on your C: drive.

### Productivity & Information
*   `"search on youtube [your query]"`: Searches YouTube for your query.
*   `"open youtube"`: Opens YouTube in your default web browser.
*   `"search on google [your query]"`: Searches Google for your query.
*   `"open google"`: Opens Google in your default web browser.
*   `"play on spotify [song name]"`: Searches for a song on Spotify and clicks the play button. **Note:** You may need to adjust the coordinates in `main.py` for the click to work correctly on your screen. To find the correct coordinates, run the `get_mouse_coords.py` script.
*   `"wikipedia [your query]"`: Searches Wikipedia for your query and reads a summary.
*   `"calculate [expression]"`: Performs a mathematical calculation.
*   `"time"`: Tells you the current time.
*   `"define [word]"`: Looks up the definition of a word.
*   `"send email"`: Initiates sending an email.

### Entertainment
*   `"play music"`: Plays a song from the `music` directory.

### General
*   `"exit"`: Stops the assistant.
*   `"world news"`: Get the latest world news headlines.
*   `"financial news"`: Get the latest financial news headlines.
*   Any other command will be treated as a chat message.

## Chrome Profile Configuration

To use a specific Chrome profile for web searches, you need to configure the `chrome_path` and `profile_directory` variables in the `open_with_profile` function in `main.py`.

### Finding Your Chrome Path and Profile Directory

1.  **Find the Chrome executable path:**
    *   Right-click on the Google Chrome shortcut on your desktop or in the Start Menu.
    *   Select "Properties".
    *   In the "Shortcut" tab, the "Target" field will contain the full path to the Chrome executable.

2.  **Find the profile directory name:**
    *   Open Google Chrome.
    *   In the address bar, type `chrome://version` and press Enter.
    *   Look for the "Profile Path" field. The profile directory name is the last part of the path (e.g., "Profile 1").

## News API Key Configuration

To use the news functionality, you must set the following environment variable:

*   `NEWS_API_KEY`: Your News API key. You can get a free developer key from [https://newsapi.org/](https://newsapi.org/) by registering for an account.

## Groq API Key Configuration

To use the chat functionality, you must set the following environment variable:

*   `GROQ_API_KEY`: Your Groq Cloud API key.

## Email Configuration

To use the email functionality, you must set the following environment variables:

*   `EMAIL_USER`: Your email address.
*   `EMAIL_PASSWORD`: Your email password or an app-specific password.

**Note:** For security reasons, it is highly recommended to use an app-specific password if you have two-factor authentication enabled on your email account.

--