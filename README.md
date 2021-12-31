1.  Install Requirements
```
pip3 install -r requirements.txt 
```
2.  Run Project
```
python3 index.py
```

## Adding New Batch into the Website
1. Navigate through the [link](https://bzcontesttracker.herokuapp.com/) 
2. Click on the New registration section in the navbar.
3. You will now be redirected to a new page where you need to fill the basic details regarding the batch.
4. The College code can needs to be Upper case letter and short (Ex: CMRCET).
5. Select the batch (If a batch graduates in 2023 then select 1923 and the batch graduates in 2025 then select 2125 and so on).
6. Give the contest leaderboard url as input in Hackerrank URL section.
7. Upload the Handles sheet file in the upload section. The file should be with .xlsx extension. Also, the sheet should be of [this](https://docs.google.com/spreadsheets/d/e/2PACX-1vQ0_60yThFlq75CI0bsF6W3DNdccRToQWXZCvUmHTQQQ0wA5Q6iGc3U2B4P-Fquvwwz1bFFbDf20qy4/pub?output=csv) format.
8. Now click on submit.
9. As soon as the data gets uploaded into the Cloud, you will be redirected to home page.
10. Now navigate to the desired batch page and you will now be seeing a leaderboard with no participation statistics.
11. Click on the Update participation button to fetch the latest participation details.
12. The above process takes 2-3 minutes of time and hence reload the page after 3 minutes. Now the updated leaderboard will be displayed.

## Steps to Update the Student Participation details
1. Navigate to the desired batch page and you will now be seeing a leaderboard with past participation statistics.
2. Click on the Update participation button to fetch the latest participation details.
3. The above process takes 2-3 minutes of time and hence reload the page after 3 minutes. Now the updated leaderboard will be displayed.


## Admin Rights
This section is present for every batch in leaderboard page and can only be accessed by logging in.
``` 
Login Credentials
Username : bzadmin
Password : admin@beingzero
```
The 6 main features included here are
### Force Update
On clicking this button all the submissions of the recent contests will be fetched again and overwritten in the Database. 
### Remove Participants
This sections helps in removing the students from the course. 
#### Steps to Use
1. Navigate to desired course leaderboard page.
2. Click on Admin Rights section and then navigate to **Remove Participants**.
3. Click on the dropdown and start selecting the list of students to be removed, and finally click on Submit button to remove them from the Course.
### Add Blocked Participants
The students who have been removed from training can be added back using this section. All the removed students will be appeared here.
#### Steps to Use
1. Navigate to desired course leaderboard page.
2. Click on Admin Rights section and then navigate to **Add Blocked Participants**.
3. Click on the dropdown (this dropdown comprises the list of removed students) and start selecting the list of students to be added back and finally click on Submit button to add the students back to the course.
### Update Handles
If any student updated their handle in Mentorpick and to make that update reflect here you need to upload the sheet of their new handles through this section.
#### Steps to Use
1. Navigate to desired course leaderboard page.
2. Click on Admin Rights section and then navigate to **Update Handles**.
3. Download the Handle sheet from [scores.mentorpick.com](https://scores.mentorpick.com/) and upload the sheet in this page and click on submit.

[This](https://docs.google.com/spreadsheets/d/e/2PACX-1vQ0_60yThFlq75CI0bsF6W3DNdccRToQWXZCvUmHTQQQ0wA5Q6iGc3U2B4P-Fquvwwz1bFFbDf20qy4/pub?output=csv) is the sample upload sheet.

### Add participants
New students can be added to the course through this section. Here you need to upload the list of new students with their handles.
#### Steps to Use
1. Navigate to desired course leaderboard page.
2. Click on Admin Rights section and then navigate to **Add participants**.
3. Upload the sheet comprising of list of students and their handles.

[This](https://docs.google.com/spreadsheets/d/e/2PACX-1vQ0_60yThFlq75CI0bsF6W3DNdccRToQWXZCvUmHTQQQ0wA5Q6iGc3U2B4P-Fquvwwz1bFFbDf20qy4/pub?output=csv) is the sample upload sheet.

### Remove Submissions
This feature helps us in removing all the submissions for a particular date.
#### Steps to Use
1. Navigate to desired course leaderboard page.
2. Click on Admin Rights section and then navigate to **Remove Submissions**.
3. Select a date for which you need to remove submissions and then click on submit.

## New Features to be added

1. Integrating Google Sign in to the site.
2. Auto update of Leaderboard after every day.