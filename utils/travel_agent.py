import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import google.generativeai as genai
from pydantic import BaseModel
import requests
import json

class TravelPreferences(BaseModel):
    budget: str
    duration: int
    start_date: datetime
    end_date: datetime
    start_location: str
    destination: str
    purpose: str
    dietary_preferences: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    mobility_requirements: Optional[str] = None
    accommodation_type: Optional[str] = None
    walking_tolerance: Optional[str] = None
    specific_interests: Optional[Dict[str, List[str]]] = None
    meal_preferences: Optional[Dict[str, str]] = None
    hidden_gems_preference: Optional[bool] = False

class TravelAgent:
    def __init__(self, api_key: str):
        
        genai.configure(api_key=api_key)
        
        # Set up the model configuration
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
)
        
    def _create_initial_prompt(self) -> str:
        return """You are an expert travel agent AI assistant. Your goal is to help users plan 
        their perfect trip by gathering necessary information and creating personalized itineraries.
        
        Please gather the following essential information from the user:
        1. Budget (specific amount or range)
        2. Trip duration and dates
        3. Starting location and destination
        4. Purpose of travel
        
        Then, dive deeper into preferences:
        1. Dietary Requirements:
           - Any specific dietary restrictions (vegetarian, vegan, gluten-free, etc.)
           - Preferred cuisines
           - Any food allergies
        
        2. Activity Preferences:
           - Interest in local culture and history
           - Adventure activities
           - Shopping preferences
           - Art and museum interests
           - Nature and outdoor activities
           - Nightlife preferences
        
        3. Mobility and Accessibility:
           - Walking tolerance (hours per day)
           - Need for accessibility accommodations
           - Preferred transportation methods
        
        4. Accommodation Details:
           - Preferred type (hotel, hostel, apartment)
           - Must-have amenities
           - Location preferences (city center, quiet area)
        
        5. Special Interests:
           - Hidden gems vs. popular attractions
           - Local experiences
           - Photography spots
           - Special events or festivals
        
        Be conversational and friendly while gathering this information."""

    def _get_destination_info(self, destination: str) -> Dict:
        """Use AI to generate destination information when web search is not available."""
        destination_prompt = f"""Generate detailed travel information for {destination} including:
        1. Top 5 must-visit attractions
        2. 3 hidden gems or local secrets
        3. 5 recommended restaurants (mix of cuisines and price ranges)
        4. Current popular events or seasonal activities
        
        Format the response as a JSON with these keys: attractions, hidden_gems, restaurants, events.
        Each should be a list of strings with brief descriptions."""

        try:
            response = self.model.generate_content(destination_prompt)
          
            info_text = response.text.strip()
            if info_text.startswith('```json'):
                info_text = info_text[7:-3]  # Remove ```json and ``` markers
            destination_data = json.loads(info_text)
            return destination_data
        except:
          
            return {
                "attractions": [
                    "Popular Landmark 1",
                    "Historic Site 1",
                    "Cultural Center",
                    "Local Market",
                    "City Park"
                ],
                "hidden_gems": [
                    "Local Secret Spot 1",
                    "Off-beaten Path Location",
                    "Local Favorite Place"
                ],
                "restaurants": [
                    "Local Cuisine Restaurant",
                    "Fine Dining Option",
                    "Casual Eatery",
                    "Street Food Spot",
                    "Cultural Restaurant"
                ],
                "events": [
                    "Local Festival",
                    "Cultural Event",
                    "Seasonal Activity"
                ]
            }
def _create_daily_schedule(self, preferences: TravelPreferences, day_num: int, 
                             attractions: List[str], restaurants: List[str]) -> str:
    """Create a structured schedule for a single day."""
    morning_prompt = f"""Create a detailed morning schedule for day {day_num} in {preferences.destination},
    considering the following preferences:
    - Walking tolerance: {preferences.walking_tolerance}
    - Dietary preferences: {', '.join(preferences.dietary_preferences)}
    - Available attractions: {', '.join(attractions[:3])}
    - Breakfast options: {', '.join(restaurants[:2])}
    """

    afternoon_prompt = """Create an afternoon schedule that includes:
    - Lunch recommendations
    - Main attractions or activities
    - Rest periods
    - Alternative indoor options in case of bad weather"""

    evening_prompt = """Plan an evening that includes:
    - Dinner recommendations
    - Evening activities or entertainment
    - Transportation back to accommodation"""

        
        
    morning = self.model.generate_content(morning_prompt).text.strip()
    afternoon = self.model.generate_content(afternoon_prompt).text.strip()
    evening = self.model.generate_content(evening_prompt).text.strip()
        
    return f"""Day {day_num}:

Morning:
{morning}

Afternoon:
{afternoon}

Evening:
{evening}"""
def generate_itinerary(self, preferences: TravelPreferences, feedback: str = "") -> str:
    """Generate a complete, personalized travel itinerary."""
    try:
        # Gather destination information
        destination_info = self.get_destination_info(preferences.destination)

        # Create the initial prompt for the itinerary
        itinerary_prompt = f"""Create a detailed {preferences.duration}-day travel itinerary for a trip to {preferences.destination}.
Trip Details:
- Budget: {preferences.budget}
- Dates: {preferences.start_date.strftime('%Y-%m-%d')} to {preferences.end_date.strftime('%Y-%m-%d')}
- Purpose: {preferences.purpose}
- Interests: {', '.join(preferences.interests) if preferences.interests else 'Various activities'}
- Dietary Preferences: {', '.join(preferences.dietary_preferences) if preferences.dietary_preferences else 'No restrictions'}
- Mobility: {preferences.mobility_requirements} (Can walk for {preferences.walking_tolerance})
- Accommodation: {preferences.accommodation_type}

Available Attractions: {', '.join(destination_info['attractions'])}
Hidden Gems: {', '.join(destination_info['hidden_gems'])}
Restaurants: {', '.join(destination_info['restaurants'])}
Events: {', '.join(destination_info['events'])}

Please create a day-by-day itinerary that:
1. Starts each day with a breakfast recommendation
2. Groups nearby attractions together to minimize travel time
3. Includes specific timing for each activity
4. Suggests restaurants that match dietary preferences
5. Incorporates rest periods and flexible time
6. Provides transportation recommendations
7. Includes estimated costs for activities
8. Suggests indoor alternatives for bad weather
9. Balances tourist attractions with hidden gems
10. Considers walking tolerance and mobility needs

Format the itinerary clearly with day numbers, times, and sections for morning, afternoon, and evening."""

        # Generate the itinerary
        response = self.model.generate_content(itinerary_prompt)
        if not response.text:
            return "Unable to generate itinerary. Please try again."

        # Add header and practical information
        full_itinerary = f"""Personalized Travel Itinerary for {preferences.destination}
Duration: {preferences.duration} days
Dates: {preferences.start_date.strftime('%Y-%m-%d')} to {preferences.end_date.strftime('%Y-%m-%d')}
Budget: {preferences.budget}
{response.text}

Practical Information:
- Emergency Numbers: Save local emergency contacts
- Weather: Check daily forecast
- Transportation: Download local transit apps
- Bookings: Make reservations in advance
- Local Customs: Research and respect local traditions"""

        return full_itinerary.strip()

    except Exception as e:
        return f"An error occurred while generating the itinerary: {str(e)}"

def refine_suggestions(self, preferences: TravelPreferences, feedback: str) -> str:
    """Refine the itinerary based on user feedback."""
    refinement_prompt = f"""
    Based on the user's feedback: {feedback}
    Please refine the suggestions for their trip to {preferences.destination}.
    
    Consider:
    1. Original preferences
    2. New feedback
    3. Alternative options
    4. Local seasonal events
    5. Current weather conditions
    6. Special requirements

    Provide specific adjustments to:
    1. Activity timing
    2. Restaurant selections
    3. Transportation options
    4. Alternative activities
    """
    
    response = self.model.generate_content(refinement_prompt)
    return response.text if response.text else "Unable to refine itinerary. Please try again."

            
    response = self.model.generate_content(refinement_prompt)
    return response.text if response.text else "Unable to refine itinerary. Please try again."

    def gather_preferences(self, user_input: str) -> Dict:
        """Gather and refine user preferences through conversation."""
        initial_prompt = self._create_initial_prompt()
        response = self.model.generate_content(f"{initial_prompt}\n\nUser: {user_input}")
        
        # Process the response and extract structured preferences
        preferences = self._parse_preferences(response.text)
        
        # Follow up with clarifying questions if needed
        if preferences.get('needs_clarification'):
            clarification_prompt = self._create_clarification_prompt(preferences)
            clarification = self.model.generate_content(clarification_prompt)
            # Update preferences with clarified information
            preferences.update(self._parse_preferences(clarification.text))
        
        return preferences

    def _create_clarification_prompt(self, preferences: Dict) -> str:
        """Create prompts for clarifying unclear preferences."""
        clarification_needed = []
        
        if not preferences.get('dietary_preferences'):
            clarification_needed.append("Could you tell me about any dietary preferences or restrictions?")
        
        if not preferences.get('walking_tolerance'):
            clarification_needed.append("How comfortable are you with walking during the day?")
        
        if not preferences.get('specific_interests'):
            clarification_needed.append("What specific activities or experiences interest you the most?")
        
        return "\n".join(clarification_needed)

    def _parse_preferences(self, response: str) -> Dict:
        """Parse the AI response into structured preferences."""
        try:
            # Simple parsing logic - extract key information using AI
            parse_prompt = f"""Extract key travel preferences from this conversation:
            {response}
            
            Format the response as a JSON with these keys:
            - dietary_preferences (list)
            - walking_tolerance (string)
            - specific_interests (list)
            - needs_clarification (boolean)
            """
            
            parse_response = self.model.generate_content(parse_prompt)
            preferences = json.loads(parse_response.text)
            return preferences
        except:
            # Return default structure if parsing fails
            return {
                "needs_clarification": True,
                "dietary_preferences": [],
                "walking_tolerance": None,
                "specific_interests": []
            } 
