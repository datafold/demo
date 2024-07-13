from openai import OpenAI
import instructor
from pydantic import BaseModel, EmailStr
from typing import List, Dict
import csv
import time
import pandas as pd
import os


class Person(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    company_name: str

class PersonsList(BaseModel):
    persons: List[Person]
    
def think_of_persons(model="gpt-3.5-turbo-0125"):
    SYSTEM_PROMPT="""You are a writer with great imagination.  You can think of endless imaginary persons with first names, last names, emails, and company names.  All of them are very realistic but not real.  All emails you think of look like real corporate emails and are not in the `example.com` or any free email domain.

    Tips:
    - You don't want email domains to repeat.
    - It is cool when email domains and company names are somehow related to data engineering, data analytics, data science area, or any other modern technology area like artificial intelligence and self-driving cars.
    - Only 50% of emails include both first and last names. Be more creative here.
    - The email part before the @ character includes first and last names in 50% of cases only.
    - Company name is always similar to email domain name but contains spaces
    """

    tools = client.chat.completions.create(
        model=model,
        response_model=PersonsList,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Come up with exactly 100, no more, no less realistic, but still unreal characters."}
        ]
    )
    return tools

def append_to_csv(persons_list: PersonsList, file_path: str):
    # Open the file in append mode
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the data rows
        for person in persons_list.persons:
            writer.writerow([person.first_name, person.last_name, person.email, person.company_name])

def deduplicate_clean_csv(input_file: str, output_file: str):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
    # Remove duplicate rows
    df_deduplicated = df.drop_duplicates()
    df_cleaned = df_deduplicated.dropna()
    
    # Write the deduplicated DataFrame back to a CSV file
    df_cleaned.to_csv(output_file, index=False)



if __name__ == "__main__":
    openai_api_key = os.environ['OPENAI_API_KEY']

    client = instructor.patch(OpenAI(api_key=openai_api_key))


    for i in range(0,100):
        print(i, '==========================================================================')
        try:
            a = think_of_persons()
            print(a)

            append_to_csv(a, 'persons_pool_raw.csv')
        except:
            time.sleep(15)
        time.sleep(15)

    input_file = 'persons_pool_raw.csv'
    output_file = 'persons_pool.csv'
    deduplicate_clean_csv(input_file, output_file)
