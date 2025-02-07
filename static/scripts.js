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

    // ADD MULTIPLE INGREDIENTS DYNAMICALLY
    const addIngredientBtn = document.getElementById("add-ingredient");
    const ingredientContainer = document.getElementById("ingredient-container");

    addIngredientBtn.addEventListener("click", function () {
        // Create a new ingredient row
        const newIngredientGroup = document.createElement("div");
        newIngredientGroup.classList.add("ingredient-group", "d-flex", "gap-2", "align-items-center", "mb-2");

        newIngredientGroup.innerHTML = `
            <input type="text" name="ingredient_name[]" class="form-control" placeholder="Ingredient Name">
            <input type="number" name="ingredient_quantity[]" class="form-control" placeholder="Quantity">
            <input type="text" name="ingredient_unit[]" class="form-control" placeholder="Unit">
            <i class="fa-solid fa-circle-xmark text-danger remove-ingredient" style="cursor: pointer; font-size: 1.3rem; margin-left: 10px;"></i>
        `;

        // Append the new ingredient row to the container
        ingredientContainer.appendChild(newIngredientGroup);
    });

    // EVENT DELEGATION: Remove ingredient when clicking on "X"
    ingredientContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-ingredient")) {
            event.target.closest(".ingredient-group").remove();
        }
    });

    // MAKE CATEGORY INPUT WRITABLE
    const categoryField = document.getElementById("category");
    if (categoryField) {
        categoryField.removeAttribute("readonly");
    }

    // CAPTURE INGREDIENTS ON FORM SUBMISSION
    document.querySelector("form").addEventListener("submit", function (event) {
        let ingredients = [];
        document.querySelectorAll(".ingredient-group").forEach(group => {
            const name = group.querySelector("input[name='ingredient_name[]']").value;
            const quantity = group.querySelector("input[name='ingredient_quantity[]']").value;
            const unit = group.querySelector("input[name='ingredient_unit[]']").value;

            if (name && quantity && unit) {
                ingredients.push({ name, quantity, unit });
            }
        });

        // Attach ingredients as a hidden input to the form
        let ingredientInput = document.createElement("input");
        ingredientInput.type = "hidden";
        ingredientInput.name = "ingredients_json";
        ingredientInput.value = JSON.stringify(ingredients);
        this.appendChild(ingredientInput);
    });

});