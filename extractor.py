from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

def extract_json(report_text):
    with open("prompt_template.txt", "r") as f:
        template = f.read()
    prompt = template.replace("{report}", report_text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract JSON from disaster reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# 🔬 Test with a sample report
if __name__ == "__main__":
    sample_report = """
Environmental Disaster Report
Incident Title:
Major Oil Spill off the Gulf Coast – MV Ocean Star

Date of Incident:
April 12, 2025

Location:
Gulf of Mexico, 45 nautical miles off the coast of Louisiana

Type of Disaster:
Marine Oil Spill

Cause of Incident:
Ruptured pipeline from MV Ocean Star due to structural failure during offloading

Reporting Agency:
U.S. Environmental Protection Agency (EPA) – Region 6
National Oceanic and Atmospheric Administration (NOAA)

1. Description of the Incident
At approximately 03:45 AM local time on April 12, 2025, the crude oil tanker MV Ocean Star reported a rupture in its starboard offloading pipeline while transferring oil to an offshore storage platform. An estimated 2.5 million gallons of light crude oil were discharged into the Gulf of Mexico over a period of four hours before the flow was contained.

2. Affected Areas
Marine zone: 50 square miles contaminated

Coastal impact: Oil slicks reached parts of the Louisiana shoreline within 36 hours

Wildlife: Initial reports confirm contamination of sea birds, fish, and marine mammals

Economic zones: Commercial fishing operations suspended in a 100-mile radius

3. Environmental Impact
Marine Life:

Deaths of over 400 seabirds reported in the first 72 hours

Observed disruption of dolphin pods and fish migration routes

Coral reefs near the impact zone show signs of early bleaching

Water Quality:

Elevated hydrocarbon levels measured in water samples

Disruption to oxygen levels in affected waters

Air Quality:

Increased VOCs (Volatile Organic Compounds) recorded near coastlines

4. Response Actions
Immediate:

Deployment of 15 containment vessels and 5 aerial dispersant aircraft

Activation of the National Response Framework

Evacuation of offshore platform workers

Short-term:

Shoreline protection using booms and skimmers

Rehabilitation centers established for injured wildlife

Temporary ban on fishing and recreational boating

Long-term:

Environmental monitoring for at least 12 months

Legal investigation into vessel maintenance records

Compensation plan being negotiated for affected local industries

5. Responsible Party
Oceanic Transport Corp., owner/operator of MV Ocean Star
Initial statement accepts partial liability pending full investigation

6. Estimated Damages
Environmental: $130 million

Economic: $75 million (fisheries, tourism, cleanup)

Total Initial Estimate: $205 million

7. Recommendations
Mandatory safety audits for all oil transfer operations

Improved leak detection systems on oil tankers

Stricter enforcement of maritime environmental compliance

Prepared by:
EPA Region 6, Disaster Response Division
Report Date: April 14, 2025

    """
    result = extract_json(sample_report)
    print(result)
