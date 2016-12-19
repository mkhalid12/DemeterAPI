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

`curl -H "Content-Type: application/json" -X POST -d '{"user_id":"58508b3366b3f645bf9fd94f", "recipe_id" : "58508a0566b3f645bf9fbaff", "rating" : 3 }' https://guarded-mesa-45511.herokuapp.com/ratings`
Should give an example of non-authorized request

Example of POST and DELETE requests (removed @login_required for demonstration)
`curl -H "Content-Type: application/json" -X POST -d '{"user_id":"58508b3066b3f645bf9fd902", "recipe_id" : "58508a0566b3f645bf9fbaff" }' https://guarded-mesa-45511.herokuapp.com/favorite_recipes/add`

`curl -H "Content-Type: application/json" -X DELETE -d '{"user_id":"58508b3066b3f645bf9fd902", "recipe_id" : "585089b666b3f645bf9f9be4" }' https://guarded-mesa-45511.herokuapp.com/favorite_recipes/delete`
