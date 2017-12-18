CPSC 571 
Lean Miguel - 10160542

Running the Twitter Sentiment Analysis Tool

The Twitter Sentiment Analysis Tool runs on Python and uses several libraries.

First install Python: https://www.python.org/downloads/

If python and pip is not found in system path : https://www.londonappdeveloper.com/setting-up-your-windows-10-system-for-python-development-pydev-eclipse-python/
If on Windows 10, after the clicking system, navigate to the right side and click on system info and continue the tutorial from there.
The Python path on your computer is usually "C:\Users\*username*\AppData\Local\Programs\Python\Python36-32".
The Python pip path on your computer is usually "C:\Users\*username*\AppData\Local\Programs\Python\Python36-32\Scripts".
Make sure to include both the python and the pip path in the system path.

After Python and pip can be found in the system path, run these commands in the command line to install libraries that the
Twitter Sentiment Analysis tool is dependent on.

pip install vaderSentiment
pip install tweepy
pip install matplotlib
pip install numpy

Once libraries have been installed, the program is ready to run. Run this line on the command line to start the program.

python twitterSentiment.py

*Notes*
Creating a CSV file does not work when the CSV file is currently open.
There are no datasets that my program is run against, as it was only compared to other websites results. 
The query tested from the other websites can be found in the paper.