# parsing-excel-files

# To run the application 
1. Build the Docker Image - unless you have python and this pandas version installed. 
  a. Docker build . - this will build the image, and assigns the cmd to be - "python3 main.py"
  b. From your terminal/CLI in the projects directory an type in the command. 
  c. Files should generate inside the cleaned and validated report data subdirectories. 
  
Excel File parsing with Pandas.
A while back I was confronted with an issue that made validating a scraped report against a finalized report a manual task. I was faced with not only the way the documents format was, but also with the naming conventions that each product had under a given commodity. A little back-story before we dive in. The business followed a specific process when it came to reporting harvested vegetable products that were turned into the cooler, and it can be broken down in the following steps. *The items reported in automated report, were not normalized to how the items reported from the updated count. So, even if you wanted to join map items by the name, nearly everything would end up unmatched*. 

# Cooler Reporting / Validation
1. Recieve an automated report for what was physically turned into the cooler for the given day. 
2. EOW combine all reported items to produce a grand summary for the week. 
3. Receive an updated count of what items passed inspection, and could be sold to vendors. 
4. Update any reported items that did not pass inspections, and deduct the total from what was reported from that day. 
5. Each box description has a unique value known as the "label" assigned to it, but this only comes through the automated system and is not provided. (Wonder if I can map these values out to one another.)

To view the initial reports you can view the automated reported generated by this site [here](https://github.com/sjrojanooo/automated-report/blob/main/data/html-doc/cooler-report.htm).

Now that we are familiar with the processes, lets dive into the issue faced with the naming convention. Commodities that harvest both conventional and organic products shared the exact same harvesting item description. There was no true way of identifying the difference, only by manually validating each product against what was reported, and seeing if the totals matched. The engineer in me just couldn't, no refused to settle with that being the only approach to solve this.  started to analyze this report, and break it down from the useless and usefull items. 

1. Report Date is provided
2. Commodity is listed above each section. 
3. Totals for each items in an aggregated format, summed up for the entire week. 

![Image](https://github.com/sjrojanooo/parsing-excel-files/blob/main/images/example-original-image.png)

The goal is to convert the formatted document in the image above to achieve the format of the image below.

![Image](https://github.com/sjrojanooo/parsing-excel-files/blob/main/images/reformatted_report.png)

After successfully parsing the document and reformatting updated counts, it brought me back to what is italicized in the introduction of this ReadMe. 
"The items reported in automated report, were not normalized to how the items reported from the updated count. So, even if you wanted to join map items by the name, nearly everything would end up unmatched." Bad designs are innevitable and I'm sure I'll make the same mistake along the way, but this definitely taught me to really analyze and understand the data to it's most granular form. 

After a few iterations I was able to identify the correct mapping for the updated report/billing report item descriptions to point #5. Create a mapping to the unique label that is generated from the cooler report. This would allowed me to accurately validate different the cooler counts provided in an automated systems vs the updated counts. Next will be moving away from excel files, and csv, to a more conventional design to this pipeline.  
