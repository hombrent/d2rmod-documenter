# d2rmod-documenter
Document items in a d2r mod


## How to Use

### Initial Assumptions (due to early Work In Progress)
* you are running the script from inside the src directory
* from the src directory, we will look for ../BTdiablo/btdiablo.mpq/ containing all mod files

Run python create-documentation.py 

It will update/create human readable text versions in the text directory 

It will also create an html version in the html directory.  ( the html version is very incomplete - the idea was to have hyperlinks to navigate around - like if you are on the Gull page, you could click on dagger to see stats on the base item, then navigate to the exceptional/elite versions, then navigate to the unique versions of those bases. )  You might not want to use the html version until it is done 

If any items have been removed from the game, we do not remove the files.  you might want to nuke the contents of html and text before you run the script so you have a fresh copy




