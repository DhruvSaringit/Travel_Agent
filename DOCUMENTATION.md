# AI Travel Planner Documentation

## 1. Prompts Used

### System Prompt (Travel Agent Initialization)

```python
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
```

### Destination Information Prompt

```python
destination_prompt = f"""Generate detailed travel information for {destination} including:
1. Top 5 must-visit attractions
2. 3 hidden gems or local secrets
3. 5 recommended restaurants (mix of cuisines and price ranges)
4. Current popular events or seasonal activities

Format the response as a JSON with these keys: attractions, hidden_gems, restaurants, events.
Each should be a list of strings with brief descriptions."""
```

### Daily Schedule Generation Prompt

```python
morning_prompt = f"""Create a detailed morning schedule for day {day_num} in {destination},
considering the following preferences:
- Walking tolerance: {preferences.walking_tolerance}
- Dietary preferences: {', '.join(preferences.dietary_preferences)}
- Available attractions: {', '.join(attractions[:3])}
- Breakfast options: {', '.join(restaurants[:2])}"""

afternoon_prompt = """Create an afternoon schedule that includes:
- Lunch recommendations
- Main attractions or activities
- Rest periods
- Alternative indoor options in case of bad weather"""

evening_prompt = """Plan an evening that includes:
- Dinner recommendations
- Evening activities or entertainment
- Transportation back to accommodation"""
```

## 2. Sample Inputs and Outputs

### Sample Input 1

```json
{
  "budget": "$2000-3000",
  "duration": 3,
  "start_date": "2024-04-01",
  "end_date": "2024-04-04",
  "start_location": "New York",
  "destination": "Paris",
  "purpose": "Cultural",
  "dietary_preferences": ["Vegetarian"],
  "interests": ["History & Culture", "Art & Museums", "Food & Dining"],
  "mobility_requirements": "No special requirements",
  "walking_tolerance": "6 hours",
  "accommodation_type": "Mid-range",
  "hidden_gems_preference": true
}
```

### Sample Output 1

```markdown
# Your Personalized Paris Itinerary

## Trip Overview

Budget: $2000-3000
Duration: 3 days
Dates: April 1-4, 2024
Purpose: Cultural Experience

Day 1:
Morning:

- 8:30 AM: Breakfast at Le Petit Pain, a charming local bakery known for fresh croissants and vegetarian options
- 9:30 AM: Visit the Louvre Museum (skip-the-line tickets recommended)
- Highlights: Mona Lisa, Venus de Milo, Winged Victory

Afternoon:

- 1:00 PM: Lunch at L'As du Fallafel in Le Marais (excellent vegetarian options)
- 2:30 PM: Explore Le Marais district
- Hidden Gem: Visit Musée Carnavalet for Paris history (free entry)
- 4:30 PM: Place des Vosges and Victor Hugo's House

Evening:

- 7:00 PM: Dinner at Le Potager du Marais (vegetarian restaurant)
- 8:30 PM: Seine River evening walk
- 9:30 PM: Eiffel Tower light show viewing from Trocadéro

[Days 2 and 3 continue with similar detailed breakdowns...]
```

### Sample Input 2

```json
{
  "budget": "$1000",
  "duration": 2,
  "start_location": "London",
  "destination": "Amsterdam",
  "purpose": "Adventure",
  "interests": ["Nature & Outdoors", "Local Experiences"],
  "dietary_preferences": ["None"],
  "accommodation_type": "Budget",
  "hidden_gems_preference": true
}
```

[Sample Output 2 would follow similar format...]

## 3. Process Documentation

### Initial Prompt Development

The system prompt was designed to be comprehensive yet conversational. It focuses on gathering all necessary information while maintaining a friendly tone. The structured approach ensures no important details are missed while planning the trip.

### Destination Information Generation

The destination prompt was crafted to provide a balanced mix of popular attractions and hidden gems. The JSON format ensures structured data that can be easily processed and incorporated into the itinerary. The prompt specifically requests varied price ranges for restaurants to accommodate different budgets.

### Daily Schedule Generation

The daily schedule prompts were split into morning, afternoon, and evening segments to ensure detailed attention to each part of the day. They consider user preferences, weather contingencies, and practical aspects like rest periods and transportation. The prompts are designed to create realistic, well-paced itineraries that don't overwhelm travelers.

## 4. Live Application

The AI Travel Planner is hosted on Streamlit Cloud and can be accessed at:
[https://travel-agent-dhruvsaringit.streamlit.app](https://travel-agent-dhruvsaringit.streamlit.app)

### Features:

- Interactive form for gathering travel preferences
- Real-time itinerary generation
- Itinerary refinement based on feedback
- Responsive design
- Detailed day-by-day planning
- Consideration for dietary restrictions and accessibility needs

### Technical Stack:

- Frontend: Streamlit
- AI Model: Google Gemini Pro
- Deployment: Streamlit Cloud
- Version Control: GitHub
