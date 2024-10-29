# Cipherion

## Notice ❗
The name "Cipherion" is associated exclusively with this project. Unauthorized use or replication of the name "Cipherion" for similar purposes is discouraged. If you wish to use the name or reference this project, please contact the author for permission.

## Table of Contents 📌
- [Overview 🔍](#overview-)
- [Features ✨](#features-)
- [Installation ⚙️](#installation-️)
  - [Requirements](#requirements)
  - [Compatibility](#compatibility)
  - [File structure](#file-structure)
- [Usage ✅](#usage-)
  - [Project setup](#project-setup)
  - [Launching the application](#launching-the-application)
- [How it works ❓](#how-it-works-)
- [Contributing 🤝](#contributing-)
- [Disclaimer ⚠️](#disclaimer-️)
- [License ℹ️](#license-ℹ️)

## Overview 🔍
**Cipherion** is a robust tool for encrypting and securely storing sensitive information using AES encryption. With its intuitive command-line interface and seamless MySQL integration, this tool allows you to manage your data efficiently and securely.

## Features ✨
- **Robust AES encryption**: Safeguard your data with industry-standard encryption methods.
- **MySQL Database integration**: Store and retrieve encrypted data with ease.
- **Simple command-line interface**: User-friendly nature enables effortless navigation.
- **Unique key generation**: Automatically create new encryption keys for each session to enhance security.

## Installation ⚙️
### Requirements
- Download [Python](https://python.org/).
- Download [MySQL Community Server](https://dev.mysql.com/downloads/mysql).
- Download [Visual Studio Code](https://code.visualstudio.com/download) or any text editor/IDE.
### Compatibility
- The application is compatible with Python version 3.x and works on any OS that supports it (Windows, macOS, Linux).
- MySQL Community Server version 8.x or higher is recommended for optimal performance and compatibility.
### File structure
```markdown
└── /root
    └── 📁docs
        └── CODE_OF_CONDUCT.md
        └── CONTRIBUTING.md
    └── 📁src
        └── db.py
        └── process.py
        └── welcome.py
    └── .gitignore
    └── LICENSE
    └── README.md
    └── main.py
    └── requirements.txt
```

## Usage ✅
### Project setup
1. Click `Star` to support development.
2. **Clone the repository**:
    1. Click the `Code` button.
    2. From the drop-down that appears, click `Download ZIP` to download the entire repository as a ZIP folder.

3. Extract the files to a new folder and open it with Visual Studio Code or any text editor/IDE of your choice.

4. **Install required packages**: Run the command to get all dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Launching the application
To run the application, execute the following command in your terminal:
```bash
python main.py
```

## How it works ❓
1. **Connecting to MySQL**:
    - Upon launching, the application prompts you to enter your MySQL root password and the desired database name. It checks for the database's existence and creates it if necessary.

2. **Encrypting data**:
    - You can choose to encrypt data by entering the text you wish to secure. The application generates a unique key and initialization vector (IV) for AES encryption, then stores the encrypted data in the database.

3. **Storing encrypted data**:
    - The application saves both the encrypted text and the encryption key into a MySQL table. Each record is assigned a unique ID for easy retrieval.

4. **Decrypting data**:
    - To decrypt, you input the record ID associated with the encrypted entry. The application retrieves the corresponding encrypted text and key from the database, then decrypts the text using the key, revealing the original message.

## Contributing 🤝
We welcome contributions to enhance **Cipherion**! For detailed instructions on how to contribute, please refer to [CONTRIBUTING.md](docs/CONTRIBUTING.md) and follow [CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md). These documents include the contributing guidelines and the code of conduct to be followed.

## Disclaimer ⚠️
**Cipherion** is intended for educational purposes and personal use only. While this application implements encryption techniques, it does not guarantee complete security against data breaches or cyber threats. Users are responsible for the security of their data and should consider additional protective measures as necessary. Use this tool at your own risk.

## License ℹ️
Released under the terms of [Apache License 2.0](LICENSE).
