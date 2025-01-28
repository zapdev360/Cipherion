# Cipherion

## Notice ❗
The name "Cipherion" is associated exclusively with this project. Unauthorized use or replication of the name "Cipherion" for similar purposes is discouraged. If you wish to use the name or reference this project, please contact the author for permission.

## Table of Contents 📌
- [Overview 🔍](#overview-)
- [Features ✨](#features-)
- [Installation ⚙️](#installation-️)
  - [Requirements](#requirements)
  - [Compatibility](#compatibility)
- [Usage ✅](#usage-)
  - [Project setup](#project-setup)
  - [Launching the application](#launching-the-application)
- [How it works ❓](#how-it-works-)
- [Contributing 🤝](#contributing-)
- [Disclaimer ⚠️](#disclaimer-️)
- [License ℹ️](#license-ℹ️)

## Overview 🔍
**Cipherion** is a robust tool for encrypting and securely storing sensitive information supporting multiple algorithms such as [AES](https://www.nist.gov/publications/advanced-encryption-standard-aes), [ChaCha20Poly1305](https://datatracker.ietf.org/doc/rfc8439/), [Blowfish](https://www.schneier.com/academic/blowfish/) and [TripleDES (3DES)](https://csrc.nist.gov/pubs/sp/800/67/r2/final). With its intuitive command-line interface and seamless [MySQL](https://dev.mysql.com/downloads/mysql) integration, this tool allows you to manage your data efficiently and securely.

## Features ✨
- **Multiple Encryption Algorithms**: Choose from [AES](https://www.nist.gov/publications/advanced-encryption-standard-aes), [ChaCha20Poly1305](https://datatracker.ietf.org/doc/rfc8439/), [Blowfish](https://www.schneier.com/academic/blowfish/) or [TripleDES (3DES)](https://csrc.nist.gov/pubs/sp/800/67/r2/final) for flexible encryption options, depending on your security needs.
- **MySQL Integration**: Connect to a [MySQL](https://dev.mysql.com/downloads/mysql) database to store all related encrypted data.
- **Recovery Phrase**: An unique recovery phrase is generated with every encryption, ensuring data security.
- **Automatic Key Rotation**: Supports automatic key rotation for the corresponding decrypted record, ensuring encryption keys are updated whilst maintaining data security.
- **Secure Password Masking**: Database password is securely masked during input, protecting sensitive login credentials.
- **User-friendly Command-Line Interface**: Detailed and intuitive prompts, along with informative tables guide you through seamless encryption and decryption.

## Installation ⚙️
### Requirements
- Download [Python](https://www.python.org/downloads/).
- Download [MySQL Community Server](https://dev.mysql.com/downloads/mysql).
- Download [Visual Studio Code](https://code.visualstudio.com/download) or any text editor/IDE.
### Compatibility
- The application is compatible with [Python](https://www.python.org/downloads/) version 3.x and works on any OS that supports it (Windows, macOS, Linux).
- [MySQL Community Server](https://dev.mysql.com/downloads/mysql) version 8.x or higher is recommended for optimal performance and compatibility.

## Usage ✅
### Project setup
1. Click `Star` to support development.
2. **Clone the repository**:
    1. Click the `Code` button.
    2. From the drop-down that appears, click `Download ZIP` to download the entire repository as a ZIP folder.

3. Extract the files to a new folder and open it with [Visual Studio Code](https://code.visualstudio.com/download) or any text editor/IDE of your choice.

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
    - Upon launching the application, you are prompted to enter your [MySQL](https://dev.mysql.com/downloads/mysql) root password and specify the database name. The application checks whether the database exists and creates one if it doesn’t, ensuring a seamless setup for secure data storage.

2. **Encrypting data**:
    - To encrypt your data, simply input the text you want to secure. You’ll then be prompted to choose an encryption algorithm ([AES](https://www.nist.gov/publications/advanced-encryption-standard-aes), [ChaCha20Poly1305](https://datatracker.ietf.org/doc/rfc8439/), [Blowfish](https://www.schneier.com/academic/blowfish/) or [TripleDES (3DES)](https://csrc.nist.gov/pubs/sp/800/67/r2/final)). The application generates an unique recovery phrase, encrypted text, encryption key and a nonce/initialization vector (depending on the chosen algorithm) and thereby encrypts your data.

3. **Storing encrypted data**:
    - The application stores the encrypted text, encryption key, hashed recovery phrase and corresponding algorithm in the database. Each encrypted record is linked to a unique ID, making it easy to retrieve and manage.

4. **Decrypting data**:
    - To decrypt your data, you need to enter the corresponding recovery phrase. The application hashes the recovery phrase input, and matches it against stored hashed recovery phrase(s). If valid, it retrieves the corresponding record id, encrypted text and key from the database and decrypts the data, revealing the original message. Additionally, the application supports automatic key rotation, ensuring re-encryption of corresponding data record with new encrypted data and encryption key.

## Contributing 🤝
We welcome contributions to enhance **Cipherion**! For detailed instructions on how to contribute, please refer to [CONTRIBUTING.md](docs/CONTRIBUTING.md) and follow [CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md). These documents include the contributing guidelines and the code of conduct to be followed.

## Disclaimer ⚠️
**Cipherion** is intended for educational purposes and personal use only. While this application implements encryption techniques, it does not guarantee complete security against data breaches or cyber threats. Users are responsible for the security of their data and should consider additional protective measures as necessary. Use this tool at your own risk.

## License ℹ️
Released under the terms of [Apache License 2.0](LICENSE).
