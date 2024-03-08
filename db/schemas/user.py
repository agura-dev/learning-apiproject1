
#Una funcion que devuelve un diccionario, lo garantizamos al tiparlo
def user_schema(user) -> dict:
    return {"id": str (user["_id"]),
           "username": user["username"],
           "email": user["email"]
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
         