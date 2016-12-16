# Demeter

This project is part of the 3rd semester of the IT4BI Master's program at Universitat Politècnica de Catalunya. The expected outcome of the project is a recipe recommendation system.

Our API documentation can be found in: https://app.swaggerhub.com/api/larissaleite/Demeter/1.0.1

Our API base endpoint is being hosted in heroku under the following URL: https://guarded-mesa-45511.herokuapp.com/

### Examples

`curl -H "Content-Type: application/json" -X GET -d '{"ingredient_name":"onion"}' https://guarded-mesa-45511.herokuapp.com/recommendations/recommend_ingredient`

`curl -X GET https://guarded-mesa-45511.herokuapp.com/users/58508b3366b3f645bf9fd94f`

`curl -X GET https://guarded-mesa-45511.herokuapp.com/recipes/58508a0566b3f645bf9fbaff`

`curl -H "Content-Type: application/json" -X GET -d '{"recipe_id":"58508a2a66b3f645bf9fc5c4"}' https://guarded-mesa-45511.herokuapp.com/recommendations/recommend_recipes`

`curl -H "Content-Type: application/json" -X GET -d '{"user_id":"58508b3366b3f645bf9fd94f"}' https://guarded-mesa-45511.herokuapp.com/ratings`
