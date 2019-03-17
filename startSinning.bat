title sinisterGramV2
start "" "D:\Developed\Automation\Batch\instaIndian\NewSuperstarWithExit.bat"
cd /d D:\Developed\Automation\sinisterGramV2
python "D:\Developed\Automation\python\extractMatchingLines.py" D:\Developed\Automation\inHaste\quicKlip.txt "instagram.com" >>"D:\Developed\Automation\sinisterGramV2\instalinks.opml"
python "D:\Developed\Automation\sinisterGramV2\sinSpider.py"
exit
exit