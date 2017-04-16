## Conos API Spec

### Authorization and Authentication

#### Register:

```
URL: http://166.62.32.120:5000/user/register
Method: POST
POST Format: {"username":"foo", "email":"bar@foo.com", "password":"bar"}
```

#### Get Token:

```
URL: http://166.62.32.120:5000/user/get_token
Method: POST
POST Format: {"email":"bar@foo.com", "password":"foo"}
```

#### Get confirmation mail:
```
URL: http://166.62.32.120:5000/user/get_confirm_mail
Method: POST
POST Format: {"email":"foo@bar.com"}
```

#### Forget password:
```
URL: http://166.62.32.120:5000/user/forget_password
Method: POST
POST Format: {"email":"bar@foo.com"}
```
The client post the user's email to here, then the server will regenerate a random 6 digits new password and send it to user's email address.

