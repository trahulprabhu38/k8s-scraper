import os
from dotenv import load_dotenv
from browser_use.llm import ChatOpenAI
from browser_use import Agent, Controller, Browser
from pydantic import BaseModel
from browser_use.agent.views import ActionResult
import asyncio
import pandas as pd
import pandas as pd
import asyncio
import os
import pandas as pd
import asyncio
from openpyxl import load_workbook
from openpyxl import Workbook
from pandas import ExcelWriter
# Load environment variables
load_dotenv()
# Initialize OpenAI model for use in the agent
llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.1
)
browser = Browser(headless=True)  # Add headless=True to run in headless mode
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
    campus_facilities: list[str] # e.g., {"Library": "Available", "Labs": "Available", "Sports": "Available"}
    total_students: int
    residential_students: int
    non_residential_students: int
    about_university: str
    admission_requirements: list[str]  # e.g., ["GRE", "TOEFL", "Documents"]
    scholarships: list[str]  # e.g., ["Merit-based", "Need-based"]
    cost_info: list[str]  # e.g., ["Domestic: $10,000", "International: $20,000"]
    tuition_fee_structure: list[str]  # e.g., ["Per Year: $30,000", "Per Semester: $15,000"]
    application_fee: float
    housing_fee_info: list[str]  # e.g., ["On-campus: $5,000", "Off-campus: $4,000"]
    living_expenses_per_month: float
    total_cost_of_attendance: float
    student_experience_details: str
    campus_life_highlights: str
    university_size: str
controller = Controller(output_model=ExtractUniversityData)
# Define your task to extract the university data
async def main(website_url):
    # Create a task description to explore the website
    task = f"""
        You are tasked with exploring the university website provided and extracting the following details.
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
        The website URL you will be exploring will be passed as an argument. You should dynamically fetch the details from the site and structure the response accordingly.
    """
    # Initialize the Agent with the task and pass the website URL
    agent = Agent(
        task=task,
        llm=llm,
        controller=controller
    )
    # Execute the agent's task and fetch results
    result: ActionResult = await agent.run()
    # Print the result (or store it as needed)
    print(result)
    result_agent = result.final_result()
    if result_agent:
        parsed: ExtractUniversityData = ExtractUniversityData.model_validate_json(result_agent)
        university_name = parsed.university_name
        programs = parsed.programs
        top_programs = parsed.top_programs
        city = parsed.city
        state = parsed.state
        country = parsed.country
        degree_levels = parsed.degree_levels
        mode_of_study = parsed.mode_of_study
        qs_ranking = parsed.qs_ranking
        acceptance_rate = parsed.acceptance_rate
        institution_type = parsed.institution_type
        campus_facilities = parsed.campus_facilities
        total_students = parsed.total_students
        residential_students = parsed.residential_students
        non_residential_students = parsed.non_residential_students
        about_university = parsed.about_university
        admission_requirements = parsed.admission_requirements
        scholarships = parsed.scholarships
        cost_info = parsed.cost_info
        tuition_fee_structure = parsed.tuition_fee_structure
        application_fee = parsed.application_fee
        housing_fee = parsed.housing_fee_info
        living_expenses_per_month = parsed.living_expenses_per_month
        total_cost_of_attendance = parsed.total_cost_of_attendance
        student_experience_details = parsed.student_experience_details
        campus_life_highlights = parsed.campus_life_highlights
        university_size = parsed.university_size
        # Here you can process or store the extracted data as needed
        # Prepare the data as a dictionary for DataFrame
        data = {
            "university_name": university_name,
            "programs": ", ".join(programs),
            "top_programs": ", ".join(top_programs),
            "city": city,
            "state": state,
            "country": country,
            "degree_levels": ", ".join(degree_levels),
            "mode_of_study": ", ".join(mode_of_study),
            "qs_ranking": qs_ranking,
            "acceptance_rate": acceptance_rate,
            "institution_type": institution_type,
            "campus_facilities": campus_facilities,
            "total_students": total_students,
            "residential_students": residential_students,
            "non_residential_students": non_residential_students,
            "about_university": about_university,
            "admission_requirements": admission_requirements,
            "scholarships": scholarships,
            "cost_info": cost_info,
            "tuition_fee_structure": tuition_fee_structure,
            "application_fee": application_fee,
            "housing_fee_info": housing_fee,
            "living_expenses_per_month": living_expenses_per_month,
            "total_cost_of_attendance": total_cost_of_attendance,
            "student_experience_details": student_experience_details,
            "campus_life_highlights": campus_life_highlights,
            "university_size": university_size
        }
        return data
    return {"university_name": {website_url}}
        # # Convert nested dicts to strings for Excel storage
        # for key in ["location", "campus_facilities", "admission_requirements", "scholarships", "cost_info", "tuition_fee_structure", "housing_fee_info"]:
        #     if isinstance(data[key], dict):
        #         data[key] = str(data[key])
        # # Create DataFrame and save to Excel
        # df = pd.DataFrame([data])
        # df.to_excel("university_data.xlsx", index=False)

async def process_universities_from_excel(excel_file, output_file):
    # Create a new workbook for saving the results
    wb = Workbook()
    sheet = wb.active
    sheet.title = "University Data"
    
    try:
        df = pd.read_csv(excel_file)

        # Define headers for the new Excel sheet
        headers = [
            "university_name", "programs", "top_programs", "city", "state", "country",
            "degree_levels", "mode_of_study", "qs_ranking", "acceptance_rate", "institution_type",
            "campus_facilities", "total_students", "residential_students", "non_residential_students",
            "about_university", "admission_requirements", "scholarships", "cost_info", "tuition_fee_structure",
            "application_fee", "housing_fee_info", "living_expenses_per_month", "total_cost_of_attendance",
            "student_experience_details", "campus_life_highlights", "university_size"
        ]
        
        # Write headers to the new sheet
        sheet.append(headers)

        # Utility function to safely join lists or return strings
        def safe_join(field):
            if isinstance(field, list):
                return ", ".join(field)
            elif isinstance(field, str):
                return field
            else:
                return ""

        # Loop through each row in the DataFrame and process the university URLs
        for _, row in df.iterrows():
            website_url = row['HD2023.Institution\'s internet website address']
            
            # Call the main function to extract university data
            result = await main(website_url)
            
            if result:
                result_values = [
                    result.get("university_name", ""),
                    safe_join(result.get("programs")),
                    safe_join(result.get("top_programs")),
                    result.get("city", ""),
                    result.get("state", ""),
                    result.get("country", ""),
                    safe_join(result.get("degree_levels")),
                    safe_join(result.get("mode_of_study")),
                    result.get("qs_ranking", ""),
                    result.get("acceptance_rate", ""),
                    result.get("institution_type", ""),
                    safe_join(result.get("campus_facilities")),
                    result.get("total_students", ""),
                    result.get("residential_students", ""),
                    result.get("non_residential_students", ""),
                    result.get("about_university", ""),
                    safe_join(result.get("admission_requirements")),
                    safe_join(result.get("scholarships")),
                    safe_join(result.get("cost_info")),
                    safe_join(result.get("tuition_fee_structure")),
                    result.get("application_fee", ""),
                    safe_join(result.get("housing_fee_info")),
                    result.get("living_expenses_per_month", ""),
                    result.get("total_cost_of_attendance", ""),
                    result.get("student_experience_details", ""),
                    result.get("campus_life_highlights", ""),
                    result.get("university_size", "")
                ]
                
                # Append the data row to the Excel sheet
                sheet.append(result_values)

                print(f"Data saved for {website_url}")
        
        # Save the newly created Excel file
        wb.save(output_file)
        print(f"All data has been saved to {output_file}")

    except Exception as e:
        wb.save(output_file)
        print(f"An error occurred while processing the file: {excel_file}")
        print(f"Error details: {e}")


chunk_number = os.getenv("CHUNK_NUMBER")
excel_file = f"chunker/input_chunks/chunk_{chunk_number}.csv"
output_file = f"/data/output_{chunk_number}.xlsx"

asyncio.run(process_universities_from_excel(excel_file, output_file))
