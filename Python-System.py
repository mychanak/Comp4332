#!/usr/bin/python
#
#  The program was written by Raymond WONG.
#  The program is used for illustrating how to execute a command (originally typed in a command prompt)
#  in Python.
#
#  Put this file under the folder "testCrawl" (under the working directory)
#

import subprocess

strCommand = "scrapy crawl OneWebpage"

subprocess.run(strCommand, shell=True)  

