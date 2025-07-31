import os
import pandas as pd
from dotenv import load_dotenv
from browser_use.llm import ChatOpenAI
from browser_use import Agent, Controller, Browser
from pydantic import BaseModel
from browser_use.agent.views import ActionResult
import asyncio
from openpyxl import Workbook
# Load environment variables
load_dotenv()
# Initialize OpenAI model for use in the agent
llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.1
)
# Initialize the browser (headless for no UI)
browser = Browser(headless=True)
# Define the model to store university data
class ExtractUniversityData(BaseModel):
    university_name: str
    programs: list[str]
    top_programs: list[str]
    city: str
    state: str
    country: str
    degree_levels: list[str]
    mode_of_study: list[str]
    qs_ranking: str
    acceptance_rate: str
    institution_type: str
    campus_facilities: list[str]
    total_students: int
    residential_students: int
    non_residential_students: int
    about_university: str
    admission_requirements: list[str]
    scholarships: list[str]
    cost_info: list[str]
    tuition_fee_structure: list[str]
    application_fee: float
    housing_fee_info: list[str]
    living_expenses_per_month: float
    total_cost_of_attendance: float
    student_experience_details: str
    campus_life_highlights: str
    university_size: str
# Controller to output model
controller = Controller(output_model=ExtractUniversityData)
# Define task to extract university data
async def main(website_url):
    task = f"""
        You are tasked with exploring the university website provided and extracting the following details:
        The website URL is: {website_url}
        1) Identify and list all programs available at the university, such as AIML, etc.
           Also, list the top 3 programs offered by the university based on relevance or ranking.
        2) Get the location of the university: city, state, and country.
        3) Identify the degree levels available at the university: Bachelors, Masters, PhD.
        4) Check for the mode of study options: Full-time, Part-time, Online.
        5) Fetch the QS World University Ranking for the university, if available.
        6) Determine the university's acceptance rate.
        7) Identify if the institution is public or private.
        8) Look for information on campus facilities such as Library, Labs, Sports facilities, etc.
        9) Find the total number of students currently enrolled at the university.
        10) Identify how many students are residential and how many are non-residential.
        11) Write a short description (about) of the university, including details like exams required and available scholarships.
        12) Gather the university's admission requirements, including exams, documents, and other prerequisites.
        13) Investigate the available scholarships: merit-based, need-based, or any other types.
        14) Extract cost-related information for both domestic and international students, including:
            i) Cost for domestic students.
            ii) Cost for international students.
            iii) On-campus accommodation cost and off-campus accommodation cost.
        15) Find out the tuition fee structure: per year and per semester.
        16) Identify the application fee.
        17) Extract housing fee information if available.
        18) Calculate the average living expenses per month for students.
        19) Estimate the total cost of attendance for a year, including tuition and living expenses.
        20) Collect student experience details such as reviews or comments.
        21) Look for highlights of campus life, including extracurricular activities, student groups, etc.
        22) Determine the university size: small (<10k students), medium (10k–30k students), or large (>30k students).
    """
    agent = Agent(task=task, llm=llm, controller=controller)
    result: ActionResult = await agent.run()
    result_agent = result.final_result()
    if result_agent:
        parsed: ExtractUniversityData = ExtractUniversityData.model_validate_json(result_agent)
        return parsed.dict()
    return {"university_name": website_url}  # In case of failure
# Function to process universities from an input CSV file and save to output Excel
async def process_universities_from_excel(excel_file, output_file):
    # Initialize Workbook
    wb = Workbook()
    sheet = wb.active
    sheet.title = "University Data"
    # Define headers for Excel
    headers = [
        "university_name", "programs", "top_programs", "city", "state", "country",
        "degree_levels", "mode_of_study", "qs_ranking", "acceptance_rate", "institution_type",
        "campus_facilities", "total_students", "residential_students", "non_residential_students",
        "about_university", "admission_requirements", "scholarships", "cost_info", "tuition_fee_structure",
        "application_fee", "housing_fee_info", "living_expenses_per_month", "total_cost_of_attendance",
        "student_experience_details", "campus_life_highlights", "university_size"
    ]
    sheet.append(headers)
    # Save the headers initially
    wb.save(output_file)
    # Helper function to join list fields
    def safe_join(field):
        if isinstance(field, list):
            return ", ".join(field)
        return field or ""
    # Read the input CSV
    df = pd.read_csv(excel_file)
    # Iterate over each row in the CSV
    for idx, row in df.iterrows():
        website_url = row.get("HD2023.Institution's internet website address", "").strip()
        if not website_url:
            print(f"[{idx}] No URL found, skipping.")
            continue
        try:
            # Process each website URL
            data = await main(website_url)
            result_values = [
                data.get("university_name", ""),
                safe_join(data.get("programs")),
                safe_join(data.get("top_programs")),
                data.get("city", ""),
                data.get("state", ""),
                data.get("country", ""),
                safe_join(data.get("degree_levels")),
                safe_join(data.get("mode_of_study")),
                data.get("qs_ranking", ""),
                data.get("acceptance_rate", ""),
                data.get("institution_type", ""),
                safe_join(data.get("campus_facilities")),
                data.get("total_students", ""),
                data.get("residential_students", ""),
                data.get("non_residential_students", ""),
                data.get("about_university", ""),
                safe_join(data.get("admission_requirements")),
                safe_join(data.get("scholarships")),
                safe_join(data.get("cost_info")),
                safe_join(data.get("tuition_fee_structure")),
                data.get("application_fee", ""),
                safe_join(data.get("housing_fee_info")),
                data.get("living_expenses_per_month", ""),
                data.get("total_cost_of_attendance", ""),
                data.get("student_experience_details", ""),
                data.get("campus_life_highlights", ""),
                data.get("university_size", "")
            ]
            sheet.append(result_values)
            wb.save(output_file)  # Save after each row
            print(f"[{idx}] :heavy_tick: Saved data for {website_url}")
        except Exception as e:
            print(f"[{idx}] :heavy_multiplication_x: Failed for {website_url}: {e!r}")
    print(f"Done. Partial results (and any successes) are in {output_file}")
# Test setup
excel_file = 'Manual_Collection_University_7_18_US.csv'  # Path to the input CSV file
output_file = 'University_Data_Output_2.xlsx'  # Path to the output Excel file
# Run the async function to process the websites
asyncio.run(process_universities_from_excel(excel_file, output_file))