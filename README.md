# Overview
This is a walk-through of using Claude.AI to write code to validate insurance data.

LLMs have limited ability to hold and process large amounts of data but they are good at writing code for programs that can do these things well so we will use the LLM to write the code and then we will run it.

# Process
1. Prompted Claude as follows:
   > I am doing work for an international professional organization that is looking to understand potential use-cases of AI / generative AI / LLMs in the insurance space, in particular they are looking to understand how it can be used for data validation and cleaning. I need you to help me generate a response for this. When we are done, I will need you to have provided (1) an approach for using this tech to do data cleaning (2) a dummy data set of insurance records with at least 15 columns and 1000 entries, each one randomly generated (3) the approach for how we can use LLMs to clean it (preferably in Python) (4) clear explanation of what this approaches strengths are and what the shortfalls or weaknesses are
3. It returned Python code which I reviewed, gave the proper location of the CSV to analyse and ran it.
4. There was a Python error, I simply copied the error text and pasted it for Claude and it re-wrote the code to handle it
5. That code worked but did not write anything as output. I prompted it as follows:
> Great! Now add code to save this output meaningfully to file in a standard format

> Change it to write the field analysis to a table and save that as a DOCX file
7. I reviewed the code once more and made one small change, tt was classifying dates as being invalid if they are 100 years away from the mean of the column which is too far, I changed this to 30,000 days from 365,000
7. At this point it is doing exactly what I wanted it to.
8.1 test.py: The Python code
8.2 flagged_records.csv: the records that the Python code identified as requiring a closer look
8.3 field_analysis.docx: Python output file with analysis of fields, including field names, number of missing values and basic summary stats on fields that contain numerical values

This was tested on 1000 rows synthetic data generated by Claude to have 15 columns and 1000 rows. I took this data and manually inserted questionable values. (insurance_dummy_data.csv)

# Results
The script identified 181 records as having data issues.
* 46 of these were for names with lengths that were longer / shorter than expected (false postive, could adjust to ask it to not test length on name field to fix)
* The record with age = flag (correct)
* 30 values of gender missing (correct)
* The record where gender = Auto (correct)
* The record where is_active = spanner (correct)
* 92 where is_active = FALSE for too long (incorrect)
* 10 where zip_code is invalid (correct)

OF the 181 identified records
* 138 were false positives (but which could easily be fixed with two more iterations with Claude
* 43 were correctly identified

It did not identify the following errors:
* Start date = 1 in row 7
* annual_income = -100 in row 3

If we iterate with Claude until false-positives are 0 then the tool identified 43 out of the 45 errors.

# Final thoughts
This is very basic example of what can be done.

To further improve this, continue with Claude giving it the following prompts:
> Adjust the code so that if the field is a persons name then no testing is done.

> Adjust the code for fields that are TRUE / FALSE to not test the length of the field to determine outliers.


Beyond that, you would not just use code written by an LLM as-is. In practice, you would likely:
* Give the LLM the exact fields and an explanation of what each one represents along with precise definition of values that are and not allowed to have more precise test-code to start with. All of the code is run on your system so the only information the LLM is getting is the name of the fields and tables in your DB, if this is data-privacy concern then re-name the fields and table names before providing it to Claude.
* Change the approach used to determine outliers, possibly using different approaches on different fields using your own knowledge of the expected distribution of values within that field
* When doing the descriptive statistics you would likely want to iterate with the LLM to improve the formatting of the output and possibly include some graphs.

