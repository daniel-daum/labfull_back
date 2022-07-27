# from src.database import schemas, models


# def test_JWT_added_to_blacklist(authorized_client, session):

#     #Create User Data
#     user = {"first_name": "anakin",
#                       "last_name": "skywalker", "email": "anakin@wustl.edu", "password": "password"}

#     #Create user and add to database
#     res = authorized_client.post("/api/users/", json= user)
#     user_data = res.json()

    
#     #Login to system, generating a JWT
#     authorized_client.post("/api/auth/login", data={"username":user["email"], "password":user["password"]})


#     jwt = session.query(models.Token_list).filter(models.Token_list.users_id == user_data['id'] ).first()


#     assert type(jwt.token) == str
    
