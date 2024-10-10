This is a walk-through of using Claude.AI to write code to validate insurance data.

LLMs have limited ability to hold and process large amounts of data but they are good at writing code for programs that can do these things well so we will use the LLM to write the code and then we will run it.

The process followed was as follows:
1. Prompted Claude as follows:
   > I am doing work for an international professional organization that is looking to understand potential use-cases of AI / generative AI / LLMs in the insurance space, in particular they are looking to understand how it can be used for data validation and cleaning. I need you to help me generate a response for this. When we are done, I will need you to have provided (1) an approach for using this tech to do data cleaning (2) a dummy data set of insurance records with at least 15 columns and 1000 entries, each one randomly generated (3) the approach for how we can use LLMs to clean it (preferably in Python) (4) clear explanation of what this approaches strengths are and what the shortfalls or weaknesses are
3. It returned Python code which I reviewed, gave the proper location of the CSV to analyse and ran it.
4. There was a Python error, I simply copied the error text and pasted it for Claude and it re-wrote the code to handle it
5. That code worked but did not write anything as output. I prompted it as follows:
> Great! Now add code to save this output meaningfully to file in a standard format

> Change it to write the field analysis to a table and save that as a DOCX file
7. At this point it is doing exactly what I wanted it to.
7.1 test.py: The Python code
7.2 flagged_records.csv: the records that the Python code identified as requiring a closer look
7.3 field_analysis.docx: Python output file with analysis of fields, including field names, number of missing values and basic summary stats on fields that contain numerical values

This was tested on 1000 rows synthetic data generated by Claude to have 15 columns and 1000 rows. I took this data and manually inserted questionable values. (insurance_dummy_data.csv)

How succesful was the testing done:
