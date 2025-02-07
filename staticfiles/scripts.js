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
        loginForm.addEventListener("submit", async function (event) {
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
        signupForm.addEventListener("submit", async function (event) {
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

    // ADD & REMOVE INGREDIENTS DYNAMICALLY
    const addIngredientBtn = document.getElementById("add-ingredient");
    const ingredientContainer = document.getElementById("ingredient-container");
    const ingredientsJsonInput = document.getElementById("ingredients_json");

    // Function to add a new ingredient row
    function addIngredientRow(name = "", quantity = "", unit = "") {
        const newIngredientGroup = document.createElement("div");
        newIngredientGroup.classList.add("ingredient-group", "d-flex", "gap-2", "align-items-center", "mb-2");

        newIngredientGroup.innerHTML = `
            <input type="text" name="ingredient_name[]" class="form-control" value="${name}" placeholder="Ingredient Name">
            <input type="number" name="ingredient_quantity[]" class="form-control" value="${quantity}" placeholder="Quantity">
            <input type="text" name="ingredient_unit[]" class="form-control" value="${unit}" placeholder="Unit">
            <button type="button" class="btn btn-danger remove-ingredient">
                <i class="fa-solid fa-xmark"></i>
            </button>
        `;

        ingredientContainer.appendChild(newIngredientGroup);
    }

    // Add click event to the "Add Ingredient" button
    if (addIngredientBtn && ingredientContainer) {
        addIngredientBtn.addEventListener("click", function () {
            addIngredientRow();
        });

        // Event delegation for removing ingredients
        ingredientContainer.addEventListener("click", function (event) {
            if (event.target.classList.contains("remove-ingredient")) {
                event.target.closest(".ingredient-group").remove();
                updateIngredientJSON();  // Update the hidden ingredients JSON field
            }
        });
    }

    // LOAD EXISTING INGREDIENTS INTO EDIT FORM
    const existingIngredientsElement = document.getElementById("existing-ingredients");
    if (existingIngredientsElement && existingIngredientsElement.textContent.trim() !== "") {
        try {
            const existingIngredients = JSON.parse(existingIngredientsElement.textContent);
            existingIngredients.forEach(ingredient => {
                addIngredientRow(ingredient.name, ingredient.quantity, ingredient.unit);
            });
        } catch (error) {
            console.error("Error parsing existing ingredients JSON:", error);
        }
    } else {
        // For new recipes, start with one empty ingredient row
        addIngredientRow();
    }

    // UPDATE INGREDIENTS JSON FIELD
    function updateIngredientJSON() {
        let ingredients = [];
        document.querySelectorAll(".ingredient-group").forEach(group => {
            const name = group.querySelector("input[name='ingredient_name[]']").value.trim();
            const quantity = group.querySelector("input[name='ingredient_quantity[]']").value.trim();
            const unit = group.querySelector("input[name='ingredient_unit[]']").value.trim();

            if (name !== "" && quantity !== "" && unit !== "") {
                ingredients.push({ name, quantity, unit });
            }
        });

        ingredientsJsonInput.value = JSON.stringify(ingredients);
    }

    // CAPTURE INGREDIENTS ON FORM SUBMISSION
    document.querySelector("form").addEventListener("submit", function (event) {
        updateIngredientJSON();
    });

    // ADD REVIEW AND REFRESH PAGE AFTER SUBMISSION
    const reviewForm = document.querySelector("#reviewForm");

    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const form = event.target;
            const rating = form.querySelector("input[name='rating']").value;
            const content = form.querySelector("textarea[name='content']").value;
            const recipeId = form.querySelector("input[name='recipe_id']").value;

            // Create a payload with the rating and content
            const payload = {
                rating: rating,
                content: content,
            };

            // Perform AJAX call to the backend API
            fetch(`/recipes/${recipeId}/add_review/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value
                },
                body: JSON.stringify(payload) // Send the review data in JSON format
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Successfully added the review
                        alert('Review added successfully!');
                        // Refresh the page to show the newly added review
                        window.location.reload(); 
                    } else {
                        // Display the error message from the backend
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('There was an error submitting your review.');
                });
        });
    }
});