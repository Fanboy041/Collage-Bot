# CollegeBot

CollegeBot is a Telegram bot designed to assist students with various tasks, providing different functionalities based on the user's role within a group.

## Features

### Start Command
When a user sends the `/start` command, the bot checks if the user has joined a specific group.

- **Not Joined**: The bot will send a message explaining its functionalities and provide a button with the group link.
- **Joined**: The bot will check if the user is a member or an owner.

### Member Status
After verifying the user ID, the bot differentiates between two user roles:

- **Member**: The bot displays the user menu.
- **Owner**: The bot displays the owner menu.

### Menu Pattern
The menus for owners and users are mostly similar with the following exceptions:

- **Owner**:
  - Can view, upload, and modify existing content.
  - Can delete subject content.
  - These options are available after the owner selects the subject name button.
  
- **Member**:
  - Cannot modify bot menu contents.
  - Menu structure includes:
    - First menu: Buttons for grades 1 to 4.
    - Second menu: Buttons for "فصل أول" (First Semester) and "فصل ثاني" (Second Semester).
    - Third menu: Buttons for subject names.

### Credits
Developed by [@Fanboy041](https://github.com/Fanboy041) with assistance from [@wal6ed](https://github.com/wal6ed).

## Setup Instructions

### Prerequisites

- Python 3.7+
- Telethon Library
- Telegram Bot API token
- Group chat ID

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/CollegeBot.git
    cd CollegeBot
    ```

2. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your bot token and group ID:

    ```python
    API_ID='your_api_id'
    API_HASH='your_api_hash'
    BOT_TOKEN='your_bot_token'
    GROUP_ID='your_group_id'
    ```

### Running the Bot

  ```sh
  python main.py
  ```

## Usage

- Send `/start` to initiate the bot and join the specified group if not already a member.
- Use the provided menus to navigate through grades and subjects.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

For any questions or issues, please contact [@Fanboy041](https://github.com/Fanboy041) or [@wal6ed](https://github.com/wal6ed).
