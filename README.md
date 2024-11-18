# Pepper Natural Dialogue System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Institution](https://img.shields.io/badge/Institution-KCL%20Robotics-red.svg)](https://www.kcl.ac.uk/research/robotics)

A research project from the Centre for Robotics Research at King's College London, focusing on natural human-robot interaction through the Pepper robot platform. This system integrates advanced dialogue capabilities with sophisticated robot control, enabling Pepper to engage in natural conversations while maintaining appropriate non-verbal behaviors such as face tracking, gesture generation, and spatial awareness.

[中文文档](README_CN.md)

![Pepper Robot](https://github.com/evannli1/Pepper-GPT/raw/main/docs/images/pepper.jpg)

## 📺 Demo Video

Watch our system in action:

[![Pepper Natural Dialogue System Demo](https://img.youtube.com/vi/6OpSl6kfg8Q/maxresdefault.jpg)](https://youtu.be/6OpSl6kfg8Q)

## 🌟 Key Features

- 🤖 Intelligent face tracking and engagement
- 🗣️ Natural language understanding and generation
- 🎭 Context-aware behavior generation
- 👆 Responsive touch interaction
- 🧠 Advanced dialogue management
- 👀 Social awareness and appropriate gaze behavior

## File Structure

- `pepper_face_tracking.py`: Face detection and tracking functionality
- `pepper_idle_animations.py`: Idle animations and touch response
- `pepper_basic_awareness.py`: Basic awareness functionality
- `pepper_disable_autonomous.py`: Autonomous life control
- `pepper_stop_behaviors.py`: Behavior control
- `pepper_wake_up.py`: Wake-up functionality
- `pepper_voice_chat.py`: Voice dialogue functionality
- `pepper_main_controller.py`: Main control program
- `chat_server.py`: GPT dialogue server

## Requirements

### Software Requirements
- Python 2.7 (for Pepper robot control)
- Python 3.x (for GPT server)
- NAOqi SDK 2.5.5+
- OpenCV 4.5.0+
- Other dependencies listed in requirements.txt

### Hardware Requirements
- Pepper Robot
- Computer with network connection
- Microphone (for voice recognition)

### NAOqi SDK Installation
1. Download NAOqi SDK from Softbank Robotics website
2. Extract the SDK to your preferred location
3. Set environment variables:
```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/path/to/pynaoqi-python2.7-2.5.5.5-linux64/lib
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd Pepper-GPT
```

2. Create and activate a Python 2.7 virtual environment for Pepper control:
```bash
virtualenv -p python2.7 venv_pepper
source venv_pepper/bin/activate
pip install -r requirements_pepper.txt
```

3. Create and activate a Python 3.x virtual environment for the GPT server:
```bash
python3 -m venv venv_server
source venv_server/bin/activate
pip install -r requirements.txt
```

4. Configure the environment:
```bash
cp .env.example .env
```
Edit `.env` file with your:
- Groq API key
- Pepper robot IP address
- Pepper robot port

## Usage

1. Start the GPT server (in Python 3.x environment):
```bash
source venv_server/bin/activate
python3 chat_server.py
```

2. In a new terminal, run the main controller (in Python 2.7 environment):
```bash
source venv_pepper/bin/activate
python2 pepper_main_controller.py
```

## Features in Detail

### Face Tracking
- Real-time face detection using OpenCV
- Automatic head movement to follow detected faces
- Mouth detection and response

### Voice Interaction
- Wake word detection ("hi" or "hello")
- Continuous speech recognition
- Natural language processing with GPT
- Animated speech responses

### Idle Behaviors
- Various predefined animations
- Touch sensor responses
- Automatic behavior switching
- Natural movement patterns

### System Control
- Autonomous life management
- Basic awareness control
- Behavior management
- Wake-up and rest states

## Troubleshooting

### Common Issues
1. NAOqi Connection Error
   - Check if Pepper is on the same network
   - Verify IP address and port
   - Ensure NAOqi SDK is properly installed

2. Speech Recognition Issues
   - Check microphone connection
   - Verify internet connection
   - Adjust noise threshold if needed

3. GPT Server Problems
   - Verify API key in .env file
   - Check server logs for errors
   - Ensure Python 3.x environment is active

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Research conducted at the [Centre for Robotics Research (CORE)](https://www.kcl.ac.uk/research/robotics), Department of Engineering, King's College London.

Project Lead: Yifan and Jiayu ([evannli1](https://github.com/evannli1))

## Acknowledgments

- Centre for Robotics Research at King's College London
- SoftBank Robotics for Pepper robot and NAOqi SDK
- Groq for GPT API
- OpenCV community
- All contributors to this project
