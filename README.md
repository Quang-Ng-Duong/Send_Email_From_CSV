# SEND_EMAIL_FROM_CSV

*Automate Outreach, Amplify Impact Instantly*

![Last Commit](https://img.shields.io/badge/last%20commit-november%202024-blue)
![Language](https://img.shields.io/badge/python-100%25-blue)
![Languages](https://img.shields.io/badge/languages-1-blue)

*Built with the tools and technologies:*  
![Markdown](https://img.shields.io/badge/-Markdown-black?logo=markdown)
![Python](https://img.shields.io/badge/-Python-blue?logo=python)

---

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)

---

## Overview

**Send_Email_From_CSV** is a developer-focused tool that automates bulk email outreach through Gmail's SMTP server, making large-scale communication effortless. It securely manages credentials and reads recipient lists from CSV files, enabling efficient and reliable email campaigns.

### Why Send_Email_From_CSV?

This project simplifies the process of sending themed emails about Vietnam to multiple recipients, integrating seamlessly into broader communication automation workflows. The core features include:

- 👤 **Secure Credential Management**: Stores and accesses user credentials safely to authenticate with Gmail.
- 📧 **Bulk Email Delivery**: Sends messages to a list of recipients from a CSV file, supporting large outreach efforts.
- 📡 **SMTP Integration**: Utilizes Gmail's SMTP server for reliable email transmission.
- 🎯 **Customizable Content**: Facilitates themed messaging, adaptable to various campaign needs.
- ⚙️ **Easy Integration**: Designed to fit into larger automation architectures, streamlining communication tasks.

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language**: Python  
- **Package Manager**: Conda  

---

### Installation

Build **Send_Email_From_CSV** from the source and install dependencies:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Quang-Ng-Duong/Send_Email_From_CSV
    ```

2. **Navigate to the project directory**:

    ```bash
    cd Send_Email_From_CSV
    ```

3. **Install the dependencies**:

    Using **conda**:

    ```bash
    conda env create -f conda.yml
    ```

---

### Usage

Run the project with:

Using **conda**:

```bash
conda activate {venv}
python {entrypoint}
