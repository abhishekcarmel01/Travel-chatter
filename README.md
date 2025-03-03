# Travel Assistant Chatbot

A Flask-based conversational travel assistant that builds customized travel itineraries based on user input. This project integrates several components:

- **Flask** – for the web server and API endpoints.
- **Ollama's Orca Mini** – for generating itinerary responses.
- **ChromaDB** – for storing and querying travel attraction embeddings.
- **OpenTripMap API** – for retrieving travel attraction data.
- **spaCy** – for extracting destination entities from user prompts.
- **Flask-Session** – for managing conversation history.

## Features

- **Multi-turn Conversation:**  
  Maintains conversation context using server-side sessions.
  
- **Travel Details Extraction:**  
  Uses spaCy to extract key details (destination, budget, duration, trip type) from natural language prompts.

- **Attraction Retrieval:**  
  Integrates OpenTripMap API data with ChromaDB to dynamically fetch relevant attractions for a given destination.

- **Itinerary Generation:**  
  Combines travel data and user prompts to generate detailed itineraries using the Orca Mini model.

- **User-friendly UI:**  
  A clean HTML/CSS chat interface with message bubbles and auto-scrolling.

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/download) installed and running
- OpenTripMap API key
- (Optional) OpenWeather API key if weather integration is desired


