**# ARG8000**

This project is a part of our junior-level engineering project where we developed an Automated Grape Picking Robot.
The robot is designed to address labor shortages and reduce the physically demanding nature of grape harvesting. The robot uses computer vision techniques for navigation and object detection, specifically for identifying and picking ripe grapes.


## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python 3.x (Ensure Python 3.6 or later is installed)
- PyCharm (or any Python IDE of your choice)
- Homebrew (macOS/Linux): Optional for installing dependencies (macOS only).
- Visual Studio Build Tools (Windows): Needed for building some dependencies like OpenCV.



  **## Setup Instructions**

### Clone the Repository

First, clone the repository to your local machine:
    git clone <repository_url>
    cd <repository_directory>

### Create and Activate a Virtual Environment
#### MacOS/Linux
python3 -m venv .venv
source .venv/bin/activate

#### Windows
python -m venv .venv
.venv\Scripts\activate

### Install Dependencies
(for macOS use pip3)
pip install opencv-python opencv-contrib-python numpy


## Run the programm

python3 main.py
