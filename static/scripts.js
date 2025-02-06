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

                recipeList.innerHTML = "";

                if (recipes.length === 0) {
                    recipeList.innerHTML = "<p class='text-center'>No recipes found. Add some!</p>";
                } else {
                    recipes.forEach(recipe => {
                        const imageUrl = recipe.image && recipe.image !== "" ? recipe.image : "/static/images/default_recipe.jpg";
                        const recipeCard = `
                            <div class="col-md-4">
                                <div class="card shadow-sm">
                                    <img src="${imageUrl}" class="card-img-top" alt="${recipe.title}">
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

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/auth/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
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

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/auth/registration/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password1: password, password2: password })
            });

            if (response.ok) {
                alert("Signup successful! Redirecting to login...");
                window.location.href = "/login/";
            } else {
                alert("Error: " + (await response.text()));
            }
        });
    }
});