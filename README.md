[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AHFn7Vbn)
# Superjoin Hiring Assignment

### Welcome to Superjoin's hiring assignment! 🚀

### Objective
Build a solution that enables real-time synchronization of data between a Google Sheet and a specified database (e.g., MySQL, PostgreSQL). The solution should detect changes in the Google Sheet and update the database accordingly, and vice versa.

### Problem Statement
Many businesses use Google Sheets for collaborative data management and databases for more robust and scalable data storage. However, keeping the data synchronised between Google Sheets and databases is often a manual and error-prone process. Your task is to develop a solution that automates this synchronisation, ensuring that changes in one are reflected in the other in real-time.

### Requirements:
1. Real-time Synchronisation
  - Implement a system that detects changes in Google Sheets and updates the database accordingly.
   - Similarly, detect changes in the database and update the Google Sheet.
  2.	CRUD Operations
   - Ensure the system supports Create, Read, Update, and Delete operations for both Google Sheets and the database.
   - Maintain data consistency across both platforms.
   
### Optional Challenges (This is not mandatory):
1. Conflict Handling
- Develop a strategy to handle conflicts that may arise when changes are made simultaneously in both Google Sheets and the database.
- Provide options for conflict resolution (e.g., last write wins, user-defined rules).
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

## Submission ⏰
The timeline for this submission is: **Next 2 days**

Some things you might want to take care of:
- Make use of git and commit your steps!
- Use good coding practices.
- Write beautiful and readable code. Well-written code is nothing less than a work of art.
- Use semantic variable naming.
- Your code should be organized well in files and folders which is easy to figure out.
- If there is something happening in your code that is not very intuitive, add some comments.
- Add to this README at the bottom explaining your approach (brownie points 😋)
- Use ChatGPT4o/o1/Github Co-pilot, anything that accelerates how you work 💪🏽. 

Make sure you finish the assignment a little earlier than this so you have time to make any final changes.

Once you're done, make sure you **record a video** showing your project working. The video should **NOT** be longer than 120 seconds. While you record the video, tell us about your biggest blocker, and how you overcame it! Don't be shy, talk us through, we'd love that.

We have a checklist at the bottom of this README file, which you should update as your progress with your assignment. It will help us evaluate your project.

- [x] My code's working just fine! 🥳
- [ ] I have recorded a video showing it working and embedded it in the README ▶️
- [x] I have tested all the normal working cases 😎
- [x] I have even solved some edge cases (brownie points) 💪
- [x] I added my very planned-out approach to the problem at the end of this README 📜

## Got Questions❓
Feel free to check the discussions tab, you might get some help there. Check out that tab before reaching out to us. Also, did you know, the internet is a great place to explore? 😛

We're available at techhiring@superjoin.ai for all queries. 

All the best ✨.

## Developer's Section
*Add your video here, and your approach to the problem (optional). Leave some comments for us here if you want, we will be reading this :)*
Video Link: https://drive.google.com/file/d/1KO1l0xG5fBKsWALypRU2MYqC-B7Ki4Vr/view?usp=sharing
My approach addresses the problem of ensuring consistency with the data within these two different contexts through the availability of a mechanism for bi-directional synchronization. The application watches the updates in both Google Sheets and the database simultaneously so updates made in one do not have to be entered manually in the other.
It makes this possible to ensure real time synchronization since differences in the data can be detected. For instance, it involves the comparison of the current status of the Google Sheet with the data, existing in the MySQL database with a defined frequency of 5 seconds. Here, if there is any change, the system selects the new one and updates the corresponding platform, meaning that it supports CRUD operations, that include creation, reading, updating and deletion. This would for instance make it possible for it to not only bring new data into the two platforms but also data that has been updated or erased on the other platform.
One of the main characteristics that can be identified is the use of the pause mechanism which can be initiated by making a change in the Google Sheet, for example, changing the cell value. This means that the user has control over when to perform sync and how to do it, which also prevents overwriting at such times.
This solution replaces a process that is usually done manually and which is likely to produce wrong results as well as inconsistent results between the Google Sheets and MySQL database. Being capable of real-time data synchronization, and ensuring the servers’ capability to process massive amounts of data, the solution achieves the purpose of this project: providing the means for data interchange between these platforms to be smooth, fast, and stable.
For scalability I implemented batch processing, which divides large datasets into smaller chunks for processing, rather than handling the entire dataset at once. This minimizes memory usage and reduces the risk of overwhelming Google Sheets API limits or MySQL resources during high-frequency updates. Additionally, batch updates and inserts optimize performance, allowing only the necessary data to be synchronized, which decreases the load on both systems. These enhancements ensure efficient handling of large datasets and frequent updates, preventing performance degradation while maintaining synchronization integrity between Google Sheets and MySQL.







