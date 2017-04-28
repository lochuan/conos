
# Conos API Spec

### URLs

```
/user/
/user/register/
/user/get_token/
/user/get_confirm_mail/
/user/forget_password/
/user/change_password/
/user/change_name/
/user/device_token/ (For pushing notification to clients)

/todo/
/toto/move_to_ongoing/
/todo/move_to_done/

/board/

/member/

/memo

/meetup/
```

### User management

#### Register:

```
URL: http://166.62.32.120:5000/user/register/ (**Token free**)
Method: POST
POST Format: {"name":"foo", "email":"bar@foo.com", "password":"bar"}
{
  "message": "Successfully registered. Confirmation mail has been sent to (some@something.com)",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4MjA1NiwiZXhwIjoxNDkzODg2ODU2fQ.eyJ1c2VyX25hbWUiOiJMb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWVAc29tZXRoaW5nLmNvbSIsInVzZXJfaWQiOm51bGx9.Qk1GeLWtWM7eqYcCS6iOivXwzX8Ft_X0b3kLgy24SXI"
}
```
After registeration, a token would return back, this token is for authorization, please keep it carefully.

#### Get Token:

```
URL: http://166.62.32.120:5000/user/get_token/ (**Token free**)
Method: POST
POST Format: {"email":"bar@foo.com", "password":"foo"}
Response: {
  "message": "Successfully generate the token",
  "status": "success",
  "token": "eyJleHAiOjE0OTIzOTY3MDQsImFsZyI6IkhTMjU2IiwiaWF0IjoxNDkyMzkzMTA0fQ.eyJ1c2VyX25hbWUiOiJMb2NodWFuIiwidXNlcl9pZCI6NCwidXNlcl9lbWFpbCI6ImxvY2h1YW5AbmF2ZXIuY29tIn0.Xy9IAsZLUqUMfKm842GyZ7mnuNiz7Lbm8MrbUWR5KUE"
}
```
You got a token from registeration, if you lost the token somehow, you can get a new one from here.

#### Get confirmation mail:

```
URL: http://166.62.32.120:5000/user/get_confirm_mail/ (**Token free**)
Method: POST
POST Format: {"email":"foo@bar.com"}
Response: {
  "message": "Confirmation mail has been sent to (lochuan@naver.com)",
  "status": "success"
}
```
The email has been using for reseting password.  The confirmation mail send to user after finishing the registeration. But if the users  forget to verify their email in an hour, the confirmation email will be expired. So, This why we need this API.

#### Forget password:

```
URL: http://166.62.32.120:5000/user/forget_password/ (**Token free**)
Method: POST
POST Format: {"email":"bar@foo.com"}
Response: {
  "message": "New password has been sent to lochuan@naver.com",
  "status": "success"
}
```
The client post the user's email to here, then the server will regenerate a random 6 digits new password and send it to user's email address.

#### Change password:

```
URL: http://166.62.32.120:5000/user/change_password/ (**Token free**)
Method: POST 
POST Format: {"email":"some@something.com", "old_password":"12345", "new_password":"45678"}
Response:{
  "message": "Password has changed successfully",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4Mjg4NiwiZXhwIjoxNDkzODg3Njg2fQ.eyJ1c2VyX25hbWUiOiJMb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWVAc29tZXRoaW5nLmNvbSIsInVzZXJfaWQiOjF9.yXO_RPFCr7Ab1YBtuu8ZTyu2Ux_JTvtnq6YuF25WMjM"
}
```

#### Change name:

```
URL: http://166.62.32.120:5000/user/change_name/
Method: PUT
POST Format: {"name":"Good Name"}
Response:{
  "message": "You have changed your name from (user1) to (Good Name)",
  "status": "success"
}
```

#### Upload device_token

```
URL: http://166.62.32.120:5000/user/device_token/
Method:POST
POST Format: {"device_token":"abc123213lkuiouaewrasdfa"}
Response:{
  "message": "You have been added your device_token",
  "status": "success"
}
```

#### Update device_token

```
URL: http://166.62.32.120:5000/user/device_token/
Method:PUT
POST Format: {"device_token":"abadsfadsfadfkuiouaewrasdfa"}
Response:{
  "message": "You have been updated your device_token",
  "status": "success"
}
```


### Board

#### Add a board

```
URL:http://166.62.32.120:5000/board/
Method: POST
POST Format: {"board_name":"Computer Architecure"}
Response:{
  "message": "(Computer Architecture) has been added",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4Mzk2MywiZXhwIjoxNDkzODkxMjg2fQ.eyJ1c2VyX2VtYWlsIjoic29tZUBzb21ldGhpbmcuY29tIiwidXNlcl9pZCI6MSwidXNlcl9uYW1lIjoiTG9jaHVhbiJ9.yUgHJhnV69Ur_pa6SZBHB69IlsH134UUkM4WlYYt7a8"
}
```

#### Delete a board

```
URL:http://166.62.32.120:5000/board/
Method: DELETE
POST Format: {"board_id":"4"}
Response:{
  "message": "(English Writing) has been deleted",
  "status": "success",
  "token": "eyJleHAiOjE0OTM4MTYwOTksImFsZyI6IkhTMjU2IiwiaWF0IjoxNDkzMjg1MTk3fQ.eyJ1c2VyX2lkIjoyLCJ1c2VyX25hbWUiOiJaaGFuZyIsInVzZXJfZW1haWwiOiJzb21lQHNvbWV0aGluZy5jb20ifQ.3IGkMrGC0iZ6wUQw3QCcwWPg-1AY_ZVexaJXm04CovA"
}
```

#### Change name of the board

```
URL:http://166.62.32.120:5000/board/
Method: PUT
PUT Format: {"board_id":"5","board_name":"Communication in multil-culture"}
Response:{
  "message": "The board name have changed from (English Speaking) to (Communication in multil-culture)",
  "status": "success",
  "token": "eyJleHAiOjE0OTM4MTYwOTksImFsZyI6IkhTMjU2IiwiaWF0IjoxNDkzMjg1MjgyfQ.eyJ1c2VyX2lkIjoyLCJ1c2VyX25hbWUiOiJaaGFuZyIsInVzZXJfZW1haWwiOiJzb21lQHNvbWV0aGluZy5jb20ifQ.l0l_i2_yKTw-vwqP10iwo0x4Od2NBY_rFwecSDQjVnQ"
}
```

### Member

#### Add member to a board

```
URL:http://166.62.32.120:5000/member/
Method: POST
POST Format: {"board_id":"5","user_email":"some@something.com"}
Response: {
  "message": "(Lochuan) has been added in the (Communication in multil-culture)",
  "status": "success",
  "token": "eyJleHAiOjE0OTM4MTYwOTksImFsZyI6IkhTMjU2IiwiaWF0IjoxNDkzMjg1NDMwfQ.eyJ1c2VyX2lkIjoyLCJ1c2VyX25hbWUiOiJaaGFuZyIsInVzZXJfZW1haWwiOiJzb21lQHNvbWV0aGluZy5jb20ifQ.Rz5HxQHlCTJkzIriuocOFfNfpfy_mx54piYA7ChaBHI"
}
```
Above POST will add foo@bar.com to board with its id == 1

#### Delete member from a board

```
URL:http://166.62.32.120:5000/member/
Method: DELETE
POST Format: {"board_id":"1","user_email":"some@good.com"}
Response:{
  "message": "(이창섭) deleted from the (board1)",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5Mzg5NDQ3NCwiaWF0IjoxNDkzMjg3MjY1fQ.eyJ1c2VyX2VtYWlsIjoic29tZTFAZ29vZC5jb20iLCJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9pZCI6bnVsbH0.4qd2EINia0oQfITERoQxm6aC6cpN8qIiknYhx0ttJl8"
}
```
Above DELETE operation will remove user foo@bar.com from board with its id == 1, if you want to leave a board, you can POST like this: {"user_email":"your@email.com","board_id":"1"}

### Todo

#### Add a todo to a board

```
URL:http://166.62.32.120:5000/todo/
Method: POST
POST Format:{"board_id":"1","item":"Meeting at Friday"}
Response: {
  "message": "(lochuan) has been added (Meeting at Friday) to (board1)",
  "status": "success",
  "token": "eyJpYXQiOjE0OTMyODczNzksImV4cCI6MTQ5Mzg5NDQ3NCwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX2VtYWlsIjoic29tZTFAZ29vZC5jb20iLCJ1c2VyX2lkIjpudWxsLCJ1c2VyX25hbWUiOiJsb2NodWFuIn0.m9iYylS15i7WBv9OIw-w7xDPW1-wOPgTxMNKVGUxT58"
}
```
#### Delete a todo

```
URL:http://166.62.32.120:5000/todo/
Method: DELETE
POST Format: {"todo_id":"1"}
Response: {
  "message": "(Meeting at Friday) has been deleted",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4ODEwMCwiZXhwIjoxNDkzODk0NDc0fQ.eyJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIiwidXNlcl9pZCI6bnVsbH0.hFP7cpO0sWPUdobbaKd0lxMK4zyLFdk1t-zR8PFCVmk"
}
```
Only the todo_id is needed for deleting, the server can detect which board the todo belongs to, so you don't need to give a board_id.

#### Change name of a todo

```
URL:http://166.62.32.120:5000/todo/
Method: PUT
POST Format: {"todo_id":"1", "todo_item":"New todo item"}
Response: {
  "message": "The todo has been changed from (Task2) to (New todo item)",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4ODI2MiwiZXhwIjoxNDkzODk0NDc0fQ.eyJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIiwidXNlcl9pZCI6bnVsbH0.TmIVBaWf8p9BAvpYAXbLOBsmsJzzN30nPe6mOtkY3gw"
}
```

#### Move todo to ongoing

```
URL:http://166.62.32.120:5000/todo/move_to_ongoing/
Method: POST
POST Format:{"todo_id":"2"}
Response: {
  "message": "(New todo item) has been moved to ongoing",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4ODU0NSwiZXhwIjoxNDkzODk0NDc0fQ.eyJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIiwidXNlcl9pZCI6bnVsbH0.MrNNMVzfyaOvtouBcEBFIuMfQpXL8tPCMTnGbe3iRV0"
}
```

#### Move ongoing to done

```
URL:http://166.62.32.120:5000/todo/move_to_done/
Method: POST
POST Format:{"todo_ongoing_id":"3"}
Response: {
  "message": "(Task4) has been moved to done",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4ODgxNCwiZXhwIjoxNDkzODk0NDc0fQ.eyJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIiwidXNlcl9pZCI6bnVsbH0.DbuTArT7X9oGblWWCiJiDmSTYn7zxfei7hqt6hRPm9g"
}
```
#### Thankyou

```
URL:http://166.62.32.120:5000/todo/thankyou/
Method: POST
POST Format:{"todo_done_id":"1"}
Response:{
  "message": "(이창섭) thanks to (lochuan), for his/her hard working",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzI4ODk3NiwiZXhwIjoxNDkzODk0NDQwfQ.eyJ1c2VyX25hbWUiOiJcdWM3NzRcdWNjM2RcdWMxMmQiLCJ1c2VyX2VtYWlsIjoic29tZUBnb29kLmNvbSIsInVzZXJfaWQiOm51bGx9.mV8z9OAa7e78pFPVMTKXIVpwH47XRSGNaDILkgjrBNw"
}
```

### Memo

#### Add a memo to a board

```
URL:http://166.62.32.120:5000/memo/
Method: POST
POST Format:{"board_id":"1","title":"memo2","content":"철학적인 관점에서 세계는 실재를 이루는 모든 것다."}
Response:{
  "message": "(lochuan) has been added (memo2) to (board1)",
  "status": "success",
  "token": "eyJleHAiOjE0OTM4OTQ0NzQsImlhdCI6MTQ5MzI5MDgwOSwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX2lkIjpudWxsLCJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIn0.6gzyItfoNuQ4P-8sAvkwmM8g3U5n8p1l0RPa-MdifrA"
}
```
#### Delete a memo

```
URL:http://166.62.32.120:5000/memo/
Method: DELETE
POST Format:{"memo_id":"2"}
Response:{
  "message": "(memo2) has been deleted",
  "status": "success",
  "token": "eyJpYXQiOjE0OTMyOTEwMDgsImV4cCI6MTQ5Mzg5NDQ3NCwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIiwidXNlcl9pZCI6bnVsbH0.4QJEzcurmRNH5NT-HjYMgheUGoe4Bg5biJ51fcPY-Cc"
}
```
#### Update a memo

```
URL:http://166.62.32.120:5000/memo/
Method: PUT
POST Format:{"memo_id":"1", "title":"new title", "content":"new content"}
Response:{
  "message": "The (memo1) has been changed",
  "status": "success",
  "token": "eyJpYXQiOjE0OTMyOTExMTUsImV4cCI6MTQ5Mzg5NDQ3NCwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIiwidXNlcl9pZCI6bnVsbH0.RHXfL0FJscL2psfuHhZZHgbCBVX0fmrDyih98AtxbxE"
}
```

### Meetup

#### Add a meetup to a board

```
URL:http://166.62.32.120.5000/meetup/
Method: POST
POST Format: {"board_id":"1","location":"room-101","start_time":"2017-04-23 09:30:21", "end_time":"2017-04-23 12:00:00"}
Response:{
  "message": "Meetup has been added in (컴퓨터과학), wait for others response",
  "status": "success",
  "token": "eyJpYXQiOjE0OTMzNTAzMzIsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDkzOTU2OTA4fQ.eyJ1c2VyX2VtYWlsIjoic29tZTFAZ29vZCIsInVzZXJfaWQiOm51bGwsInVzZXJfbmFtZSI6InVzZXIxIn0.B4HSq7ChvY7nSL3XPTdXGqmUep7mRBI-kt_sV8TEO8c"
}
```
Both the start_time and the end_time must be in format of 'yyyy-mm-dd hh:mm:ss'. For production, all of the datetime must be in UTC standard time. Some tips below:

1. If you don't want to decide the location, assign location as null. -> "location":"null"
2. If the location has been uploaded, but you want to change it. -> "location":"room-100", then location would be changed to room-100.
3. If the meetup time doesn't match, you must re-update your start_time or end_time, then you can post with {"board_id":"1","location":"null","start_time":"new time", "end_time":"new time"}, in this case, you just want to re-update your time, no want to change the meetup location, so you must be assign location as null.
4. Still confusing? **One board only have one meetup location, but can have multiple meetup_time response from different users**. For this API, surely I can divide it to add_meetup, add_meetup_location, update_meetup_location, add_meetup_time, update_meetup_time, but it's so tedious and bloated. Finally, I decide to combine all this features together, just in one URL, one API.
5. What will happen if the server get all user's response?  The server would response:
```
Response on fail match:{
        'status': 'fail',
        'message': '(user1) was too late, or (user2) was too early' 
      }

Response on successful match:responseObject = {
        'status': 'success',
        'time': "Mon, 10 Apr 2017 09:00:00 GMT",
        'location': "room-100"
      }
```
6. What else? OK, there is a attribute in every board object called meetup_status, it has three different values, 0 represents no meetup in the board, 1 represents the meetup is undering negotiation, 2 represents the meetup has been decided.
7. Get your hands dirty, explore more by yourself.

#### Delete meetup within a board

```
URL:http://166.62.32.120:5000/meetup/
Method: DELETE
POST Format: {"board_id":"1"}
Response:{
  "message": "Meetup has been removed from (컴퓨터과학)",
  "status": "success",
  "token": "eyJpYXQiOjE0OTMzNTAxMzQsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDkzOTU2OTA4fQ.eyJ1c2VyX2VtYWlsIjoic29tZTFAZ29vZCIsInVzZXJfaWQiOm51bGwsInVzZXJfbmFtZSI6InVzZXIxIn0.QKQpLAQZ6nS7fTpWZCluej5--L4tUzSO-NIT5fYzkYY"
}
```

### Get all the information for a user

```
URL:http://166.62.32.120:5000/user/
Method: GET
Response:{
  "boards": [
    {
      "board_id": 1,
      "board_name": "board1",
      "members": [
        {
          "member_id": 2,
          "member_name": "lochuan",
          "member_thanks_received": 2,
          "member_todos_created_num": 8,
          "member_todos_done_num": 3
        }
      ],
      "memos": [
        {
          "holder_id": 2,
          "holder_name": "lochuan",
          "memo_content": "new content",
          "memo_id": 1,
          "memo_last_changed_time": "Thu, 27 Apr 2017 11:05:16 GMT",
          "memo_title": "new title"
        }
      ],
      "todos": [
        {
          "creator": "lochuan",
          "todo_id": 3,
          "todo_item": "Task3",
          "todo_last_changed_time": "Thu, 27 Apr 2017 10:12:09 GMT"
        },
        {
          "creator": "lochuan",
          "todo_id": 8,
          "todo_item": "This is task 6",
          "todo_last_changed_time": "Thu, 27 Apr 2017 11:11:53 GMT"
        }
      ],
      "todos_done": [
        {
          "done_by": "lochuan",
          "thanks_from": [],
          "todo_done_id": 2,
          "todo_done_item": "New todo item"
        }
      ],
      "todos_ongoing": [
        {
          "holder": "lochuan",
          "holder_id": 2,
          "todo_ongoing_id": 4,
          "todo_ongoing_item": "This is task 4"
        }
      ]
    },
    {
      "board_id": 2,
      "board_name": "board2",
      "members": [
        {
          "member_id": 2,
          "member_name": "lochuan",
          "member_thanks_received": 2,
          "member_todos_created_num": 8,
          "member_todos_done_num": 3
        }
      ],
      "memos": [],
      "todos": [
        {
          "creator": "lochuan",
          "todo_id": 6,
          "todo_item": "Task5",
          "todo_last_changed_time": "Thu, 27 Apr 2017 10:13:20 GMT"
        }
      ],
      "todos_done": [
        {
          "done_by": "lochuan",
          "thanks_from": [
            {
              "user_id": 1,
              "user_name": "이창섭"
            },
            {
              "user_id": 2,
              "user_name": "lochuan"
            }
          ],
          "todo_done_id": 1,
          "todo_done_item": "Task4"
        },
        {
          "done_by": "lochuan",
          "thanks_from": [],
          "todo_done_id": 3,
          "todo_done_item": "Task3"
        }
      ],
      "todos_ongoing": []
    }
  ],
  "confirmed": 0,
  "thanks_received": 2,
  "thanks_to": [
    {
      "item": "Task4",
      "user": "lochuan"
    }
  ],
  "todos_created_num": 8,
  "todos_done_num": 3,
  "token": "eyJpYXQiOjE0OTMyOTE1NzUsImV4cCI6MTQ5Mzg5NDQ3NCwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX25hbWUiOiJsb2NodWFuIiwidXNlcl9lbWFpbCI6InNvbWUxQGdvb2QuY29tIiwidXNlcl9pZCI6bnVsbH0.lYolEjDun6ahP0NWJE10GnYdnfWzbWcYFzAnGZPcNfA",
  "user_id": 2,
  "user_name": "lochuan"
}
```
This API offers all of the information related to a user. The boards which the user involved, and all of the information within the board, like todo, todo_ongoing, todo_done, memos, members. Here is a pure-new user's information looks like:
```
{
  "boards": [],
  "confirmed": 0,
  "thanks_received": 0,
  "thanks_to": [],
  "todos_created_num": 0,
  "todos_done_num": 0,
  "token": "eyJpYXQiOjE0OTMyOTE5MjQsImV4cCI6MTQ5MzkwMDMwNywiYWxnIjoiSFMyNTYifQ.eyJ1c2VyX25hbWUiOiJuZXciLCJ1c2VyX2VtYWlsIjoic29tZTJAZ29vZC5jb20iLCJ1c2VyX2lkIjpudWxsfQ.yojrmWD1xGhbhyi1m2lBg0QkNTHvot5fqoqd5C-4e2E",
  "user_id": 3,
  "user_name": "new"
}
```


