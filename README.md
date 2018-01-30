# toothpick sharing service
Start service as module `python -m toothpick_sharing` after installing it or being in project root project folder.
Swagger UI is available at http://localhost:5000/. To run tests execute `python -m unittest discover tests`

## API

### Resources

#### GET /api/users
Retreives collection of all users.

#### POST /api/users
Creates new user. Expects JSON-encoded user passed within body.

#### GET /api/users/{user_id}
Retrieves user by ID.

#### GET /api/toothpicks
Retreives collection of all users.

#### POST /api/toothpicks
Creates new toothpick. Does not require any input.

#### GET /api/toothpicks/{toothpick_id}
Retrieves toothpick by ID.

#### POST /api/toothpicks/{toothpick_id}/owners/{user_id}
Updates toothpick ownership.

### Models

#### User
```json
{
  "id": 42,
  "name": "Jack Daniels"
}
```

### Toothpick
```json
{
  "id": 42,
  "owners": [
    {
      "user": {
        "id": 42,
        "name": "Jack Daniels"
      },
      "since": "2018-01-29T19:52:06.700Z"
    }
  ]
}


```