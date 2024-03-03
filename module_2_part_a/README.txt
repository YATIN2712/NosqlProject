NAME: JANAPALA SWATHI
ROLL: 23CS60R80
Github link: https://github.com/YATIN2712/NosqlProject
user id's:
    ->ranivenigalla
    ->swathijanapala
    ->YATIN2712

###First task:###

->I have implemented the module-2 part-a task that is "Extracting all the worldwide news for all the times" (code stored in 
module_2_part_a directory) and have extracted the each month timeline news and stored in seperate text files like 
"month_year.txt" and added those text files to "module_2_part_a/Timeline_news" directory.

For execution:
        ->use the command "make run_extract" to extract all the Timeline news.


###Second task:###
->For above module-2 part-a i have implemented the  MapReduce paradigm of NoSQLmodule(3.2 module part-a)
"Showing all the worldwide news between the time range". This mapreduce part stored in module_2_part_a/Timelines_Query 
directory.
->I have removed the combiner part as it unnecessary for my task.

To execute this part:
        ->change the directory to "Timelines_Query".
        ->use the command make run_Query
        ->Enter the valid start and end dates. 
            for example:
                start time: 2-2-2022 (2nd february 2022)
                end time: 3-3-2023 (3rd march 2023)
        ->All Timeline news between that range got extracted and stored in result.txt file
