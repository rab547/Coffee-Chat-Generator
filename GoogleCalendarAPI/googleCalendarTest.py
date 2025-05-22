import datetime
from googleCalendarAPI import GoogleCalendar
import os

def main():
    # Get file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Define paths relative to the project root
    token_path = os.path.join(project_root, "token.json")
    credentials_path = os.path.join(project_root, "GCal_credentials.json")
    
    # Initialize the calendar
    cal = GoogleCalendar()
    print("Google Calendar initialized\n")
    
    # Get today's date and time for examples
    now = datetime.datetime.now()
    today = now.date()
    
    # List all calendars
    calendars = cal.list_calendars()
    calendar_ids = [calendar["id"] for calendar in calendars]
    
    print(f"\nFound {len(calendar_ids)} calendars")
    
    # Test 1: Get free slots for the primary calendar for the next week
    print("\n\nTEST 1: Free slots for primary calendar (next 7 days)")
    primary_free_slots = cal.find_free_time_slots_next_week(
        calendar_ids="primary", 
        start_hour=9,
        end_hour=17,
        duration_minutes=30
    )
    print(primary_free_slots)
    print(type(primary_free_slots))
    
    # Test 2: Get free slots across all calendars for the next 3 days
    # print("\n\nTEST 2: Free slots across all calendars (next 3 days)")
    # all_calendars_free_slots = cal.find_free_time_slots_next_week(
    #     calendar_ids=calendar_ids,
    #     days_to_check=3,
    #     duration_minutes=60  # 1-hour slots
    # )
    
    print("\nCalendar operations completed successfully!")

if __name__ == "__main__":
    main()