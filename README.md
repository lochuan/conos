# Mission Tracking

### Enviroment Configuration and Initialization

- [x] Python3 
- [x] Virtualenv
- [x] Flask
- [x] Mysql
- [ ] Redis
- [ ] Gnicorn
- [ ] Nginx
- [ ] Docker

### Database Implementation

- [x] user table
- [x] board table
- [x] todo table
- [x] todo-ongoing table
- [x] todo-done table
- [ ] memo table
- [ ] meetup table
- [ ] file sharing table
- [x] user-board relation
- [ ] user-todo relation
- [ ] user-memo relation
- [ ] user-file-sharing relation
- [ ] user-meetup-board relation

### Module develepment

- User Management
  - [x] Register
  - [x] Token dispatch
  - [x] User confirmation by mail
  - [x] Send confimation mail
  - [x] Forget password
  - [ ] Personal Profile
  - [ ] SNS-similar feature

- Board Management
  - [x] Add board
  - [x] Delete board
  - [x] Add a member to a board
  - [x] Remove a member from board
  - [ ] Board status
  - [ ] Board sharing
  
- Todo Management
  - [ ] Add todo
  - [ ] Delete toto
  - [ ] Move toto to ongoing
  - [ ] Move ongoing to done
  - [ ] Thanks someone who done a good job
  - [ ] Status tracking
  - [ ] Statistical Report

- Memo Management
  - [ ] Add memo
  - [ ] Delete memo
  - [ ] Edit memo
  - [ ] Memo sharing


- Attachment Management
  - [ ] Add attah
  - [ ] Delete attach

- Notification
  - [ ] Get user's device key
  - [ ] Firebase connect
  - [ ] Individual Push
  - [ ] Group Push

### Testing

- Register
- Token dispatch
- User confirmation by mail
- Send confimation mail
- Forget password
- Add board
- Delete board
- Add a member to a board
- Remove a member from board


### Deployment

- [ ] Change run level from test to production
- [ ] Gnicorn and Nginx configuration
- [ ] Packing project and config file to Docker image
- [ ] Multi-WSGI if needed
- [ ] QoS load balancing if needed




# Conos API Spec

### Authorization and Authentication

#### Register:

```
URL: http://166.62.32.120:5000/user/register/
Method: POST
POST Format: {"username":"foo", "email":"bar@foo.com", "password":"bar"}
Response: {
  "message": "Successfully registered. Confirm mail sent",
  "status": "success",
  "token": "eyJleHAiOjE0OTIzOTY1OTAsImFsZyI6IkhTMjU2IiwiaWF0IjoxNDkyMzkyOTkwfQ.eyJ1c2VyX25hbWUiOiJMb2NodWFuIiwidXNlcl9pZCI6bnVsbCwidXNlcl9lbWFpbCI6ImxvY2h1YW5AbmF2ZXIuY29tIn0.RmOjU--MtwYQYleYEFTto6jz97mdhf16njxhTL1nSIc"
}
```
After register, a token will be send back.

#### Get Token:

```
URL: http://166.62.32.120:5000/user/get_token/
Method: POST
POST Format: {"email":"bar@foo.com", "password":"foo"}
Response: {
  "message": "Successfully generate the token",
  "status": "success",
  "token": "eyJleHAiOjE0OTIzOTY3MDQsImFsZyI6IkhTMjU2IiwiaWF0IjoxNDkyMzkzMTA0fQ.eyJ1c2VyX25hbWUiOiJMb2NodWFuIiwidXNlcl9pZCI6NCwidXNlcl9lbWFpbCI6ImxvY2h1YW5AbmF2ZXIuY29tIn0.Xy9IAsZLUqUMfKm842GyZ7mnuNiz7Lbm8MrbUWR5KUE"
}
```
If the token somehow losted, get a new token from this API.

#### Get confirmation mail:
```
URL: http://166.62.32.120:5000/user/get_confirm_mail/
Method: POST
POST Format: {"email":"foo@bar.com"}
Response: {
  "message": "Confirmation mail has been sent to lochuan@naver.com",
  "status": "success"
}
```
To verify the user give us a email belongs to him/her. the correct email address used for reset password. The confirmation mail send to user after finishing the register. But if the users are forget to verify their email in an hour, the confirmation email will be expired. So, This why we need this API, the confirmation email was expired, get another for users by post the email to this API.

#### Forget password:
```
URL: http://166.62.32.120:5000/user/forget_password/
Method: POST
POST Format: {"email":"bar@foo.com"}
Response: {
  "message": "New password has been sent to lochuan@naver.com",
  "status": "success"
}
```
The client post the user's email to here, then the server will regenerate a random 6 digits new password and send it to user's email address.


### Board and member
#### Add a board

```
URL:http://166.62.32.120:5000/board/
Method: POST
POST Format: {"board_name":"foo"}
```

#### Delete a board
```
URL:http://166.62.32.120:5000/board/
Method: DELETE
POST Format: {"board_id":"integer"}
Response: {
  "message": "Capstone has been added",
  "status": "success"
}
```

#### Get board list of an user
```
URL:http://166.62.32.120:5000/board/
Method: GET
Response: {
  "boards": [
    {
      "created_time": "Mon, 17 Apr 2017 01:42:52 GMT",
      "id": 4,
      "name": "자바"
    },
    {
      "created_time": "Mon, 17 Apr 2017 01:43:37 GMT",
      "id": 5,
      "name": "Capstone"
    },
    {
      "created_time": "Mon, 17 Apr 2017 01:44:03 GMT",
      "id": 6,
      "name": "中国语"
    },
    {
      "created_time": "Mon, 17 Apr 2017 01:44:24 GMT",
      "id": 7,
      "name": "컴퓨저구조"
    }
  ]
}
```

#### Change name of the board
```
URL:http://166.62.32.120:5000/board/
Method: PUT
PUT Format: {"board_id":"integer", "board_name":"new name"}
Response: {
  "message": "The board name have changed from Capstone to A new name",
  "status": "success"
}
```

#### Get the members from a board
```
URL:http://166.62.32.120:5000/board/member/<int: board_id>
Method: GET
Response: {
  "members": [
    {
      "id": 4,
      "name": "Lochuan",
      "thanks": 0
    }
  ]
}
```
Example: if you request http://166.62.32.120:5000/board/member/1, the members in the board (board_id == 1) will return

#### Add member to a board
```
URL:http://166.62.32.120:5000/board/member/
Method: POST
POST Format: {"user_email":"foo@bar.com", "board_id":"1"}
Response: {
  "message": "AnotherUser added in the 中国语",
  "status": "success"
}
```
Above POST will add foo@bar.com to board with its id == 1

#### Delete member from a board
```
URL:http://166.62.32.120:5000/board/member/
Method: DELETE
POST Format: {"user_email":"foo@bar.com", "board_id":"1"}
Response: {
  "message": "AnotherUser deleted from the 中国语",
  "status": "success"
}
```
Above DELETE operation will remove user foo@bar.com from board with its id == 1, if you want to leave a board, you can POST like this: {"user_email":"your@email.com","board_id":"1"}
