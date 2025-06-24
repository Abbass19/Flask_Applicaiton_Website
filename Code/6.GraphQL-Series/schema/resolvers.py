from ariadne import QueryType, MutationType, ObjectType
from fake_data import UserList, MovieList

query = QueryType()
mutation = MutationType()
user_object = ObjectType("User")

@query.field("users")
def resolve_users(_, info):
    return UserList

@query.field("user")
def resolve_user(_, info, id):
    return next((user for user in UserList if user["id"] == int(id)), None)

@query.field("movies")
def resolve_movies(_, info):
    return MovieList

@query.field("movie")
def resolve_movie(_, info, name):
    return next((movie for movie in MovieList if movie["name"] == name), None)

@user_object.field("Favorite_Movies")
def resolve_favorite_movies(user, info):
    return [movie for movie in MovieList if 2010 <= movie["year"] < 2023]

@mutation.field("createUser")
def resolve_create_user(_, info, input):
    user = input.copy()
    last_id = UserList[-1]["id"] if UserList else 0
    user["id"] = last_id + 1
    UserList.append(user)
    return user

@mutation.field("updateUserName")
def resolve_update_username(_, info, input):
    print("We entered the mutation function")
    id_ = int(input["id"])
    new_username = input["new_username"]

    for user in UserList:
        if user["id"] == id_:
            user["username"] = new_username
            return user
    return None

@mutation.field("deleteUser")
def delete_user(_, info, id):
    print("Entered deleteUser with id:", id)
    id_ = int(id)
    user_to_delete = None
    for user in UserList:
        if user["id"] == id_:
            user_to_delete = user
            break
    if user_to_delete:
        UserList.remove(user_to_delete)
        print("Deleted user:", user_to_delete)

    return user_to_delete
