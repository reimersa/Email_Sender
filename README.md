# Sending automatic emails with attachments with python

This repo is initially intended for TAs at UZH that are required to send corrected homeworks to a list of students.

# Instructions

Download the repo with:

```bash
git clone https://github.com/ViniciusMikuni/Email_Sender.git
```
The script requires the following structure:

* A file called ```students.txt```, containing the name, surname and email of each student (Exactly like the excell sheet we first received with the student list). Example:

```bash
John Doe john.doe@uzh.ch
Joe Doe joe.doe@uzh.ch
```
The script now supports special characters, both in the PDF file names, as well as in ```students.txt```. The file ```students.txt``` needs to be encoded in UTF-8. 

If the students sometimes hand in with special characters (ä, ö, ü), and sometimes without (ae, oe, ue), it is recommended to duplicate their entry to satisfy both conventions. 

* A folder called ```HWN```, where ```N``` stands for the homework number which files are saved. Ex: ```HW7```. Save the homeworks in this folder after correction. The name of the files in the folder should follow the same pattern the students are required to follow. In the script itself, change the default message to your liking.

# Running the script:

```bash
python send_emails.py --sender your.email@uzh.ch --pwd YOURPASSWORD --HW N
```

Before sending, verify in the screen if all students are associated to the respective homeworks and emails. If everything seems right, run the same code again, but with the flag ```--send```:

```bash
python send_emails.py --sender your.email@uzh.ch --pwd YOURPASSWORD --HW N --send
```
In order to avoid your password being stored in clear text in the command history, it is recommended to run the command without writing to history. To do so, you need to make sure the variable HISTCONTROL is set to 'ignorespace' or 'ignoreboth': 

```bash
echo $HISTCONTROL
```
And if it is not the case, set it:

```bash
export HISTCONTROL=ignorespace
```

Then, you can run commands by starting them with a leading space, and avoid them being stored in the history: 
```bash
 python send_emails.py --sender your.email@uzh.ch --pwd YOURPASSWORD --HW N --send
```
(For more details, see: https://stackoverflow.com/questions/8473121/execute-command-without-keeping-it-in-history)

