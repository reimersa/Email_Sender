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

* A folder called ```HWN```, where ```N``` stands for the homework number which files are saved. Ex: ```HW7```. Save the homeworks in this folder after correction. The name of the files in the folder should follow the same pattern the students are required to follow. In the script itself, change the default message to your liking.

# Running the script:

```bash
python send_emails.py --sender your.email@uzh.ch --pwd YOURPASSWORD --HW N
```

Before sending, verify in the screen if all students are associated to the respective homeworks and emails. If everything seems right, run the same code again, but with the flag ```--send```:

```bash
python send_emails.py --sender your.email@uzh.ch --pwd YOURPASSWORD --HW N --send
```

