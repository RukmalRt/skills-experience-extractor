from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model = "llama-3.3-70b-versatile")
def extract(article_text):
    prompt = '''
    From the following text, which may be either a job posting or a CV/resume,
    extract skills and experience information.

    Return the output in valid JSON format with the following keys:

    - 'document_type': either 'job posting' or 'cv'
    - 'skills': a list of skills mentioned (technical and soft skills)
    - 'experience_years': total years of experience if explicitly stated, otherwise null
    - 'experience_summary': a short summary of experience described in the text
    - 'tools_technologies': a list of tools, frameworks, platforms, or programming languages mentioned

    Rules:
    - Infer document_type based on the content.
    - Do NOT hallucinate skills or experience.
    - If a field is not present, return an empty list or null.
    - Skills should be normalized (e.g., \"Python\", \"Machine Learning\", \"SQL\").
    - Only return valid JSON.
    - No preamble, no explanation, no markdown.

    Text
    ==========

    {text}
    '''
    pt = PromptTemplate.from_template(prompt)
    global llm

    chain = pt | llm
    res = chain.invoke({"text": article_text})
    parser = JsonOutputParser()
    try:
        output_json = parser.parse(res.content)
    except OutputParserException:
        raise OutputParserException("Context is too large. Unable to parse jobs.")

    return output_json


text = """
Full job description
About Us

VibeCodingAcademy is a new initiative helping people who’ve never written a single line of code get confident with modern digital skills. We run friendly, beginner-focused online classes that show students how to build real websites and apps, using both traditional coding and modern tools like Lovable (AI-assisted app builder).

Our students are mostly complete beginners – often children, teens, or adults with no technical background at all. Your job is to make the tech feel simple, welcoming, and practical.

The Role

We are looking for patient, engaging instructors to deliver small-group online classes. Lessons are delivered via video call (e.g. Zoom/Teams) using prepared lesson structures and exercises.

Typical topics include:

Basic computer and internet skills
Intro to coding and logic (e.g. Scratch or simple Python)
Building simple websites (e.g. basic HTML/CSS, or using templates)
Using tools like Lovable to quickly build simple web apps
Problem-solving and “how to think like a programmer”
You don’t need to be a senior software engineer – but you do need solid basic coding knowledge and/or experience with modern website/app builders.

Responsibilities

Teach live online classes to small groups (e.g. 10–20 students)
Follow and adapt lesson plans to suit the group’s pace
Demonstrate how to:
Build simple websites (with or without code)
Use tools like Lovable in a simple, step-by-step way
Explain technical ideas in plain English, using everyday examples
Support students who are struggling and build confidence in beginners
Provide basic feedback on student progress where needed
Attend occasional check-in meetings with the organiser
Requirements

Confident with at least one of the following:
Beginner-friendly coding (Scratch, Python, or basic HTML/CSS/JavaScript)
AND/OR website or app builders (e.g. Lovable, Wix, Webflow, Bubble, etc.)
Strong communication skills and clear spoken English
Comfortable teaching complete beginners (no prior knowledge assumed)
Reliable internet connection, webcam, and a quiet space to teach from
Punctual, organised, and able to commit to agreed time slots
Experience with Lovable or similar AI-assisted tools is a strong plus. If you haven’t used Lovable before but are confident learning new tools quickly, we can provide guidance/training.

Desirable (nice to have, not essential):

Experience teaching or tutoring (online or in person)
Experience working with children/teenagers or adult learners
Teaching qualification, PGCE, or STEM degree
Based in/near Bradford or West Yorkshire (not required but a plus)
Hours

Flexible, part-time
Mainly evenings and/or weekends/afternoons/mornings to suit students’ schedules
Ideal for university students, PGCE trainees, teachers, or developers wanting extra income
What We Offer

Flexible, remote work
Opportunity to help under-served communities build real digital skills
Teach using modern, practical tools (including Lovable)
Small, supportive team and growing academy
Potential for more hours and responsibility as we expand
If you’d like to speed up the process, you can also email your CV + short cover note to: contact@vibecodingacademy.co.uk

Shortlisted candidates will be invited to a short teaching/demo first, followed by a brief online interview.

Job Type: Part-time

Pay: From £50.00 per hour

Expected hours: 1 – 10 per week

Benefits:

Flextime
Work from home
Work Location: Remote

Job Types: Full-time, Part-time, Zero hours contract

Pay: From £50.00 per hour

Expected hours: 5 – 30 per week

Benefits:

Flexitime
Work Location: Remote
"""

rs = extract(text)
print(rs)