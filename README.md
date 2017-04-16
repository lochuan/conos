## Conos API Spec

### Authorization and Authentication

#### Register:

```
URL: http://166.62.32.120:5000/user/register/
Method: POST
POST Format: {"username":"foo", "email":"bar@foo.com", "password":"bar"}
```
After register, a token will be send back.

#### Get Token:

```
URL: http://166.62.32.120:5000/user/get_token/
Method: POST
POST Format: {"email":"bar@foo.com", "password":"foo"}
```
If the token somehow losted, get a new token from this API.

#### Get confirmation mail:
```
URL: http://166.62.32.120:5000/user/get_confirm_mail/
Method: POST
POST Format: {"email":"foo@bar.com"}
```
To verify the user give us a email belongs to him/her. the correct email address used for reset password. The confirmation mail send to user after finishing the register. But if the users are forget to verify their email in an hour, the confirmation email will be expired. So, This why we need this API, the confirmation email was expired, get another for users by post the email to this API.

#### Forget password:
```
URL: http://166.62.32.120:5000/user/forget_password/
Method: POST
POST Format: {"email":"bar@foo.com"}
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
```

#### Get board list of an user
```
URL:http://166.62.32.120:5000/board/
Method: GET
```

#### Change name of the board
```
URL:http://166.62.32.120:5000/board/
Method: PUT
PUT Format: {"board_id":"integer", "board_name":"new name"}
```

#### Get the members from a board
```
URL:http://166.62.32.120:5000/board/member/<int: board_id>
Method: GET
```
Example: if you request http://166.62.32.120:5000/board/member/1, the members in the board (board_id == 1) will return

#### Add member to a board
```
URL:http://166.62.32.120:5000/board/member/
Method: POST
POST Format: {"user_email":"foo@bar.com", "board_id":"1"}
```
Above POST will add foo@bar.com to board with its id == 1

#### Delete member from a board
```
URL:http://166.62.32.120:5000/board/member/
Method: Delete
POST Format: {"user_email":"foo@bar.com", "board_id":"1"}
```
Above DELETE operation will remove user foo@bar.com from board with its id == 1, if you want to leave a board, you can POST like this: {"user_email":"your@email.com","board_id":"1"}
