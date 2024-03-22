# SC2 Bot AI Project

## Introduction
This project focuses on developing a StarCraft II (SC2) bot AI utilizing the PySC2 library, a Python library for playing StarCraft II using the SC2 API. The ultimate goal of this project is to create a sophisticated AI agent capable of competing against human players or other AI opponents. The AI employs a combination of strategic decision-making, resource management, and real-time gameplay tactics to achieve victory.

## Objective
The primary objective of this project is to enhance the AI's capabilities by integrating a Convolutional Neural Network (CNN) with a Long Short-Term Memory (LSTM) network. The CNN will be utilized to extract features from the game's visual data obtained through the `intel()` method's visualization. Meanwhile, the LSTM will utilize both previous actions and the extracted features as context to predict the next action. This integration aims to improve the AI's decision-making process by providing it with a deeper understanding of the game environment and history.

## Features
### 1. Real-time Gameplay
The AI bot interacts with the SC2 environment in real-time, making decisions on resource management, unit production, base expansion, scouting, and combat tactics dynamically during the game.

### 2. Visualization
The `intel()` method provides visualization of the game state, including the locations of various game elements such as units, structures, resources, and enemy units. This visualization serves as the input data for the CNN-LSTM hybrid model.

### 3. Strategic Decision-making
The AI employs strategic decision-making algorithms to determine optimal actions based on current game conditions and long-term objectives. This includes building structures, training units, expanding bases, and launching attacks.

### 4. Machine Learning Integration
The integration of machine learning techniques, specifically CNNs and LSTMs, enhances the AI's decision-making capabilities by allowing it to learn from past experiences and adapt its strategies over time.

### 5. Parallelization
The project explores the possibility of parallelizing the AI's learning capabilities using the Discovery cluster. By distributing computational tasks across multiple nodes, the AI can potentially accelerate its learning process and improve overall performance.

## Setup Instructions
To set up and run the SC2 bot AI project, follow these steps:
1. Install Python and required libraries, including PySC2, OpenCV, NumPy, and TensorFlow.
2. Download and install StarCraft II and the SC2 API.
3. Clone the project repository from GitHub.
4. Configure the bot's parameters, such as race, difficulty level, and map, in the provided Python script.
5. Execute the Python script to run the AI bot and observe its performance in simulated games.

## Usage
The project can be used for various purposes, including:
- Testing and benchmarking different AI strategies and algorithms in SC2 gameplay.
- Studying the integration of machine learning techniques with real-time strategy games.
- Exploring parallelization techniques for accelerating AI learning and decision-making processes.

## Contribution Guidelines
Contributions to the project are welcome and encouraged. If you wish to contribute, please follow these guidelines:
- Fork the repository and create a new branch for your contributions.
- Make your changes, ensuring adherence to coding standards and best practices.
- Submit a pull request detailing your changes, including a brief description of the modifications and their purpose.

## Conclusion
The SC2 Bot AI project aims to create an advanced AI agent capable of competing in the complex and dynamic environment of StarCraft II. By integrating machine learning techniques, parallelization, and strategic decision-making algorithms, the project seeks to push the boundaries of AI research in real-time strategy gaming. With further development and experimentation, the project holds the potential to contribute valuable insights to the fields of AI and machine learning.
