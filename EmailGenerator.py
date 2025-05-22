from dotenv import load_dotenv
import os
import requests
import json
import datetime
from GoogleCalendarAPI.googleCalendarAPI import GoogleCalendar
load_dotenv() 
from groq import Groq
from app import firebase
from urllib.parse import urlparse

API_KEY = os.getenv("API_KEY_PROXYCURL")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"
DEFAULT_COUNTRY = "US"

def searchLinkedIn(collegeName, companyNames, role, country=DEFAULT_COUNTRY):
    if len(companyNames) == 0:
        return "No Company Inputted"

    company = companyNames[0]
    for i in range(1, len(companyNames)):
        company += " OR " + companyNames[i]

    company = company.lower()


    api_key = os.getenv("API_KEY_PROXYCURL")
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/search/person'

    params = {
        'country': country,
        'education_school_name': collegeName,
        'current_company_name': company,
        'enrich_profiles': 'enrich',
        'current_role_title': role,
        'page_size': '1'
    }

    response = requests.get(api_endpoint, params=params, headers=headers)
    data = response.json()

    if data.get("total_result_count", 0) == 0:
        params = {
            'country': country,
            'education_school_name': collegeName,
            'current_company_name': company,
            'enrich_profiles': 'enrich',
            'page_size': '1'
        }
        response = requests.get(api_endpoint, params=params, headers=headers)
        data = response.json()
        if data.get("total_result_count", 0) == 0:
            params = {
            'country': country,
            'current_company_name': company,
            'enrich_profiles': 'enrich',
            'page_size': '1'
            }
            response = requests.get(api_endpoint, params=params, headers=headers)
            data = response.json()

    return data

def cleanLinkedInData(data):
    if isinstance(full_response, str):
        full_response = json.loads(full_response)
    
    cleaned = {}
    
    education_list = []
    for edu in full_response.get("education", []):
        school_name = edu.get("school")
        degree_name = edu.get("degree_name")
        start_year = None
        end_year = None
        if edu.get("starts_at"):
            start_year = edu["starts_at"].get("year")
        if edu.get("ends_at"):
            end_year = edu["ends_at"].get("year")
        education_list.append({
            "school": school_name,
            "degree": degree_name,
            "start_year": start_year,
            "end_year": end_year
        })
    cleaned["education"] = education_list
    
    work_list = []
    for exp in full_response.get("experiences", []):
        company = exp.get("company")
        role = exp.get("title")
        start_date = None
        end_date = None
        if exp.get("starts_at"):
            start_year = exp["starts_at"].get("year")
            start_month = exp["starts_at"].get("month")
            if start_year and start_month:
                start_date = f"{start_year}-{start_month:02d}"
            elif start_year:
                start_date = str(start_year)
        if exp.get("ends_at"):
            end_year = exp["ends_at"].get("year")
            end_month = exp["ends_at"].get("month")
            if end_year and end_month:
                end_date = f"{end_year}-{end_month:02d}"
            elif end_year:
                end_date = str(end_year)
        work_list.append({
            "company": company,
            "role": role,
            "start_date": start_date,
            "end_date": end_date
        })
    cleaned["work_experiences"] = work_list
    
    volunteer_list = []
    for vol in full_response.get("volunteer_work", []):
        organization = vol.get("company") 
        role = vol.get("title")         
        start_date = None
        end_date = None
        if vol.get("starts_at"):
            year = vol["starts_at"].get("year")
            month = vol["starts_at"].get("month")
            if year and month:
                start_date = f"{year}-{month:02d}"
            elif year:
                start_date = str(year)
        if vol.get("ends_at"):
            year = vol["ends_at"].get("year")
            month = vol["ends_at"].get("month")
            if year and month:
                end_date = f"{year}-{month:02d}"
            elif year:
                end_date = str(year)
        volunteer_list.append({
            "organization": organization,
            "role": role,
            "start_date": start_date,
            "end_date": end_date
        })
    cleaned["volunteer_experiences"] = volunteer_list
    
    languages_list = []
    for lang in full_response.get("languages", []):
        if isinstance(lang, dict):
            name = lang.get("name") or lang.get("language") 
            prof = lang.get("proficiency")
        else:
            name = lang
            prof = None
        languages_list.append({
            "name": name,
            "proficiency": prof
        })
    cleaned["languages"] = languages_list
    
    skills = []
    for skill in full_response.get("skills", []):
        if isinstance(skill, dict):
            skill_name = skill.get("name") or skill.get("skill") or str(skill)
        else:
            skill_name = str(skill)
        skills.append(skill_name)
    cleaned["skills"] = skills
    
    return cleaned

def getFreeTimeSlots():
    cal = GoogleCalendar()
    
    now = datetime.datetime.now()
    
    calendars = cal.list_calendars()
    calendar_ids = [calendar["id"] for calendar in calendars]

    free_slots_dict = cal.find_free_time_slots_next_week(
        calendar_ids=calendar_ids, 
        start_hour=9,
        end_hour=17,
        duration_minutes=30
    )

    output = ["# Available Free Time Slots\n"]
    
    sorted_dates = sorted(free_slots_dict.keys())
    
    for date in sorted_dates:
        day_name = date.strftime("%A")
        month_name = date.strftime("%B")
        day = date.strftime("%d").lstrip("0")  
        year = date.strftime("%Y")
        
        output.append(f"## {day_name}, {month_name} {day}, {year}")
        
        slots = free_slots_dict[date]
        
        if not slots:
            output.append("- No free time available\n")
            continue
        
        for start, end in slots:
            start_time = start.strftime("%I:%M %p").lstrip("0").replace(" 0", " ") 
            end_time = end.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
            
            duration_minutes = (end - start).total_seconds() / 60
            hours = int(duration_minutes // 60)
            minutes = int(duration_minutes % 60)
            
            if hours > 0 and minutes > 0:
                duration_str = f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
            elif hours > 0:
                duration_str = f"{hours} hour{'s' if hours != 1 else ''}"
            else:
                duration_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
            
            output.append(f"- {start_time} - {end_time} ({duration_str})")
        
        output.append("")
    
    return "\n".join(output)

def generateEmail(collegeName, companyNames, role, resumeData, country=DEFAULT_COUNTRY):

    #THIS BLOCK USES LINKEDIN API
    # personData = searchLinkedIn(collegeName, companyNames, role)['results'][0]


    #THIS BLOCK LOADS FROM JSON

    search_result = {}
    with open('search_results.json', 'r') as f:
        search_result = json.load(f)
    print(search_result)
    personData = search_result['results'][0]

    #End







    freeTimeSlots = getFreeTimeSlots()
    content = "You are an assistant helping to write a professional networking message to request a conversation.\n"
    content += "Here is my resume: " + resumeData + "\n\n"
    content += "Here is information about the employee: \n" + str(personData) + "\n\n"
    content += "Here is my time availability: " + freeTimeSlots + "\n\n"
    content += """
    Using the provided information, write a single concise and polite networking message that can be directly sent over LinkedIn or email without any further editing. 

    The message should:
    - Begin with a polite greeting mentioning their name (if available).
    - Introduce me in one to two sentences based on my resume.
    - Briefly explain why I am reaching out based on their background and my interests.
    - Propose scheduling a conversation by offering three or more available times. Format these as bullet points in an easily readable format
    - End with a warm, polite, and open-ended closing.
    - Sign off the email with my information

    Output **only the email text itself** — no explanations, no extra formatting, no preambles, and only a single version.
    """

    print(content)

    client = Groq(api_key=os.getenv("API_KEY_GROQ"))
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {
            "role": "user",
            "content": content
        },
    ],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=1,
    stream=False,
    stop=None,
    )
    email = str(completion.choices[0].message.content)



    personalSummary = "Give a concise proffesional summary of the following person. Focus on career information: \n" + str(personData)
    personalSummary += "\n\nOutput **only the summary itself** — no explanations, no extra formatting, no preambles, and only a single version."
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {
            "role": "user",
            "content": personalSummary
        },
    ],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=1, 
    stream=False,
    stop=None,
    )
    personalSummary = str(completion.choices[0].message.content)
    pfp = personData['profile']["profile_pic_url"]
    #GET RID OF THIS SHIT
    pfp = None
    if pfp == None:
        pfp = "https://i.seadn.io/gae/y2QcxTcchVVdUGZITQpr6z96TXYOV0p3ueLL_1kIPl7s-hHn3-nh8hamBDj0GAUNAndJ9_Yuo2OzYG5Nic_hNicPq37npZ93T5Nk-A?auto=format&dpr=1&w=1000"
        
    emailAddress = findEmail(personData['profile']["first_name"], personData['profile']["last_name"], personData["linkedin_profile_url"])

    return[pfp, personalSummary, emailAddress, str(email), makeSubjectLine(str(email)), personData] 


    output = completion.choices[0].message
    email = ""
    
    return ["rab547@cornell.edu", "Hello, I am tech support"]
    returnable = [email, output]
    return returnable

def editEmail(email, edits, pfp, personalSummary, emailAddress, resumeData, personData, subjectLine):
    content = "You are an professional assistant tasked with editing my emails. Here is some context: \n" 
    content += "My information: " + resumeData
    content += "\n\n Here is information about the person I'm emailing: \n" + str(personData)
    content += "\n\n Here is my current written email: \n" + email
    content += "\n\n Here are the edits I want made: " + edits
    content += "\nOutput **only the email text itself** — no explanations, no extra formatting, no preambles, and only a single version."
    client = Groq(api_key=os.getenv("API_KEY_GROQ"))
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {
            "role": "user",
            "content": content
        },
    ],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=1,
    stream=False,
    stop=None,
    )
    return [pfp, personalSummary, emailAddress, str(completion.choices[0].message.content), subjectLine, personData]

def makeSubjectLine(email):
    content = "Make a concise (Less than 8 words) tile line for the following email: \n" + email
    content += "\n\nOutput **only the subject line itself** — no explanations, no extra formatting, no preambles, and only a single version."
    client = Groq(api_key=os.getenv("API_KEY_GROQ"))
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {
            "role": "user",
            "content": content
        },
    ],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=1,
    stream=False,
    stop=None,
    )
    return str(completion.choices[0].message.content)

def findEmail(firstName, lastName, linkedin_url):
    url = "https://api.apollo.io/api/v1/people/match?first_name="+ firstName + "&last_name="+ lastName + "&linkedin_url=" + linkedin_url + "&reveal_personal_emails=true&reveal_phone_number=false"

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": os.getenv("API_KEY_APOLLO")
    }

    response = requests.post(url, headers=headers)
    data = response.json()
    print(str(data["person"]["email"]))
    

