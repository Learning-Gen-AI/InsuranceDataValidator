# Overview
This is a walk-through of using Claude.ai to write code to validate insurance data.

This does not cover correcting the data which might differ by organization based on your data processing policies.

LLMs have limited ability to hold and process large amounts of data but they are good at writing code for programs that can do these things well so we will use the LLM to write the code and then we will run it.


# Process
1. Prompted Claude as follows:
   > I am doing work for an international organization that is looking to understand potential use-cases of AI / generative AI / LLMs in the insurance space, in particular they are looking to understand how it can be used for data validation and cleaning. I need you to help me generate a response for this. When we are done, I will need you to have provided (1) an approach for using this tech to do data cleaning (2) a dummy data set of insurance records with at least 15 columns and 1000 entries, each one randomly generated (3) the approach for how we can use LLMs to clean it (preferably in Python) (4) clear explanation of what this approaches strengths are and what the shortfalls or weaknesses are
3. It returned Python code which I reviewed, gave the proper location of the CSV to analyse and ran it.
4. There was a Python error, I simply copied the error text and pasted it for Claude and it re-wrote the code to handle it
5. That code worked but it was writing the output to the terminal and I wanted it to write it to files for a person to review. I prompted it as follows:
> Great! Now add code to save this output meaningfully to file in a standard format

> Change it to write the field analysis to a table and save that as a DOCX file
7. I reviewed the code once more and made one small change, it was classifying dates as being invalid if they are 100 years away from the mean of the column which is too far, I changed this to 30,000 days from 365,000
8. At this point it is doing exactly what I wanted it to. The main files are as follows:
   * **test.py**: The Python code
   * **flagged_records.csv**: (output) contains the records that the Python code identified as requiring a closer look
   * **field_analysis.docx**: (output) contians the analysis of fields, including field names, number of missing values and basic summary stats on fields that contain numerical values

This was tested on 1000 rows of synthetic data generated by Claude to have 15 columns and 1000 rows. It had added some unexpected values to gender and zip code. I manually inserted some other out-of-place values. (**insurance_dummy_data.csv**). The script used to generate the synthetic before I made adjustments is **generate data.py**


# Results
The flagged records are contained in file **flagged_records.csv** and the analysis of the fields is in **field_analysis.docx**

The script identified 181 records as having data issues.
* 46 of these were for names with lengths that were longer / shorter than expected (incorrect)
* The record with age = flag (correct)
* 30 values of gender missing (correct)
* The record where gender = Auto (correct)
* The record where is_active = spanner (correct)
* 92 where is_active = FALSE for too long (incorrect)
* 10 where zip_code is invalid (correct)

Of the 181 identified records
* 138 were false positives (but which could easily be fixed with two more iterations with Claude, possible prompts are given further below)
* 43 were correctly identified

It failed to identify the following errors:
* Start date = 1 in row 7 (which is interesting because this value is 44649 away from the median of this field and I adjusted the code to have a cut-off of 30000, I will need to look closer at this one)
* annual_income = -100 in row 3 (I had initially asked it to test for negative values but it looks like this never made it through to the final piece of code)

If we iterate with Claude until false-positives are 0 then the tool identified 5 of the 7 data inconsistencies so even after doing something like this you always needs to do a final round of checks on the data to pick up the remaining outliers.


# Further developments and final thoughts

This is very basic example of what can be done.

To correct the false-positives you could do something like this:
> Adjust the code so that if the field is a persons name then no testing is done.

> Adjust the code for fields that are TRUE / FALSE to not test the length of the field to determine outliers.

> The testing is not flagging negative values in fields that store numbers, please adjust (this should fix 1 of the 2 issues it failed to fix)

> The testing is not flagging low dates, flag any date before 1980 (this should fix the second of the 2 issues it failed to fix)

Beyond that, you would not just use code written by an LLM as-is. In practice, you would likely do the following:
* Before running any code written by an LLM understand what every line of code is doing before using it.
* Check each package that is being used and make sure that there are no known issues or vulnerabilities with those packages. If there are, then interate with the LLM asking it to not use that package. It will not always be possible to use a different package.
* Give the LLM the exact fields and an explanation of what each one represents along with precise definition of values that are and not allowed to have more precise test-code to start with. All of the code is run on your system so the only information the LLM is getting is the name of the fields and tables in your DB, if this is data-privacy concern then re-name the fields and table names before providing it to Claude.
* Change the approach used to determine outliers, possibly using different approaches on different fields using your own knowledge of the expected distribution of values within that field
* When doing the descriptive statistics you would likely want to iterate with the LLM to improve the formatting of the output and possibly include some graphs.
* You likely have a lot of data that does not live in a CSV so when the code is ready you would need to adjust it to connect to your data source.
* You would want to train the code on data that contains known issues and make sure it identifies all of them. The step on generating synthetic data could be greatly expanded to generate synthetic data that mimics your own actual data which you can then adjust to contain examples of known data issues. Iterate until all known issues are identified.
* You could add a step to clean the data, perhaps you have a default assumption for gender when the client doesn't provide one; you could code that in. Some fields can be derived from others, for example if you have a South African ID number you can derive the date of birth and gender from the ID number and use that to validate those two fields. In order to do something like this responsibly you would need it to generate very clear output of exactly what it changed and you would want to do a test afterwards to ensure that changes were made as it claims. A better approach here might be to let a human analyze the errors then manually write code to make the fixes and run that. Keeping a human in the loop here is critical to ensuring nothing goes wrong in the cleaning step.
* In practice you would have several underlying source tables, you would want to run testing on each individual table so this type of thing would need to be iterated for each table. In a case like this you could extend the testing to cover tests applied to primary keys of each table to look for and flag duplicates. 

# What not to do
In one earlier iteration of a similar exercise the LLM wrote code that guessed the person's gender given their name if the gender was missing! This is an exmaple of why you need to read the code carefully before using it because the LLM might be doing something you never asked it to do and don't want it to do!
