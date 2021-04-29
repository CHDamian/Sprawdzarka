
*Copyright © 2020 by Damian Chańko*<br/>
*All rights reserved*<br/>


# Sprawdzarka
App to solve algorytmic problems written in Django (project in Polish).

## Functions
- App has login function.
- Inside app there are multiple tasks to solve (you can find some tasks on https://students.mimuw.edu.pl/~dc394127).
- User can read tasks all saved in .pdf.
- User can send solution in c++. App will compile code and run on prepared tests then check answers for those.
- User can check reports of his old solutions.
- App is compatible with Windows

## How to add tasks
- Into folder static/Tester/tasks put folder named by this task id (3 letters)
- Inside put text.pdf which is your task text and folder tests
- Inside folder tests put yuour tests
- Al tests have format <nr>.in <nr>.out, where <nr> is number of test from 1 to 5
- Right now u can only add 5 tests
- Add task into database (id has to be the same as folder name and give difficulty from 1 to 3)
- There are examples inside project without .pdf files.

## To be added
- Visual improvement (css, etc.)
- Code improvement (SOLID, etc)
- Docker (for testing)

## Future improvements
- Normal/Admin user
- Adding tasks and tests inside app
- Users Ranking
- Linux/Mac compatibility 

*To be continued...*

**Damian Chańko dc394127**
