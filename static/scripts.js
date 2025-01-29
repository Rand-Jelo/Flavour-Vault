document.addEventListener("DOMContentLoaded", function () {

    // FETCH RECIPES FOR HOME PAGE 
    async function fetchRecipes() {
        try {
            const response = await fetch('/api/recipes/');
            console.log("Response status:", response.status);

            const textResponse = await response.text();
            console.log("Raw response:", textResponse);  

            try {
                const recipes = JSON.parse(textResponse);
                console.log("Fetched recipes:", recipes);

                const recipeList = document.getElementById('recipeList');
                if (!recipeList) {
                    console.error("Error: recipeList element not found.");
                    return;
                }

                recipeList.innerHTML = "";  // Clear existing content

                if (recipes.length === 0) {
                    recipeList.innerHTML = "<p class='text-center'>No recipes found. Add some!</p>";
                } else {
                    recipes.forEach(recipe => {
                        const recipeCard = `
                            <div class="col-md-4">
                                <div class="card shadow-sm">
                                    <img src="${recipe.image || 'https://via.placeholder.com/150'}" class="card-img-top" alt="${recipe.title}">
                                    <div class="card-body">
                                        <h5 class="card-title">${recipe.title}</h5>
                                        <p class="card-text">${recipe.description}</p>
                                        <a href="/recipes/${recipe.id}/" class="btn btn-primary">View Recipe</a>
                                    </div>
                                </div>
                            </div>
                        `;
                        recipeList.innerHTML += recipeCard;
                    });
                }
            } catch (jsonError) {
                console.error("Failed to parse JSON response:", jsonError);
            }
        } catch (error) {
            console.error("Error fetching recipes:", error);
        }
    }

    fetchRecipes();

    // LOGIN FUNCTIONALITY
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function(event) {
            event.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/api/auth/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            if (response.ok) {
                localStorage.setItem("access_token", data.access);
                alert("Login successful! Redirecting to recipes...");
                window.location.href = "/recipes/"; 
            } else {
                alert("Error: " + (data.error || "Login failed"));
            }
        });
    }

    // SIGNUP FUNCTIONALITY 
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", async function(event) {
            event.preventDefault();

            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/api/auth/signup/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();
            if (response.ok) {
                alert("Signup successful! Redirecting to login...");
                window.location.href = "/login/";
            } else {
                alert("Error: " + (data.error || "Signup failed"));
            }
        });
    }

    // FETCH SINGLE RECIPE DETAILS
    async function fetchRecipe() {
        const recipeId = window.location.pathname.split('/')[2];
        console.log("Extracted recipe ID:", recipeId); 

        try {
            const response = await fetch(`/api/recipes/${recipeId}/`);
            console.log("Recipe response status:", response.status);

            const textResponse = await response.text();
            console.log("Raw recipe response:", textResponse); 

            const recipe = JSON.parse(textResponse);
            console.log("Fetched recipe:", recipe);

            document.getElementById('recipeTitle').innerText = recipe.title;
            document.getElementById('recipeDescription').innerText = recipe.description;
            document.getElementById('recipeInstructions').innerText = recipe.instructions;

            // Populate Ingredients List
            const ingredientList = document.getElementById('ingredientList');
            ingredientList.innerHTML = "";
            recipe.ingredients.forEach(ingredient => {
                const li = document.createElement('li');
                li.innerText = `${ingredient.quantity} of ${ingredient.ingredient.name}`;
                ingredientList.appendChild(li);
            });

            // Fetch and Display Reviews
            fetchReviews(recipeId);
        } catch (error) {
            console.error("Error fetching recipe:", error);
        }
    }

    if (window.location.pathname.includes('/recipes/')) {
        fetchRecipe();
    }

    // FETCH REVIEWS 
    async function fetchReviews(recipeId) {
        console.log("Fetching reviews for recipe ID:", recipeId);

        try {
            const response = await fetch(`/api/recipes/${recipeId}/get_reviews/`);
            console.log("Reviews response status:", response.status);

            const textResponse = await response.text();
            console.log("Raw reviews response:", textResponse); 

            const reviews = JSON.parse(textResponse);
            console.log("Fetched reviews:", reviews);

            const reviewList = document.getElementById('reviewList');
            reviewList.innerHTML = "";

            if (reviews.length === 0) {
                reviewList.innerHTML = "<p>No reviews yet. Be the first to review this recipe!</p>";
                return;
            }

            reviews.forEach(review => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${review.user}</strong> - ${review.rating}⭐ <br> ${review.content}`;
                reviewList.appendChild(li);
            });
        } catch (error) {
            console.error("Error fetching reviews:", error);
        }
    }

    // HANDLE REVIEW SUBMISSION
    const reviewForm = document.getElementById("reviewForm");
    if (reviewForm) {
        reviewForm.addEventListener("submit", async function(event) {
            event.preventDefault();

            const token = localStorage.getItem("access_token");
            if (!token) {
                alert("You must be logged in to submit a review.");
                return;
            }

            const recipeId = window.location.pathname.split('/')[2];
            const rating = document.getElementById("rating").value;
            const content = document.getElementById("comment").value;

            const response = await fetch(`/api/recipes/${recipeId}/add_review/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify({ rating, content })
            });

            if (response.ok) {
                location.reload();
            } else {
                const errorData = await response.json();
                alert("Failed to submit review: " + JSON.stringify(errorData));
            }
        });
    }
});
