// Home Page 
async function fetchRecipes() {
    try {
        const response = await fetch('/api/recipes/');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const recipes = await response.json();
        console.log("Fetched recipes:", recipes);

        const recipeList = document.getElementById('recipeList');
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
    } catch (error) {
        console.error("Error fetching recipes:", error);
        document.getElementById('recipeList').innerHTML = `<p class='text-danger text-center'>Error loading recipes. ${error.message}</p>`;
    }
}

fetchRecipes();



// Login Page
document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/auth/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("access_token", data.access);
        alert("Login successful! Redirecting to recipes...");
        window.location.href = "/recipes/"; // Redirect after login
    } else {
        alert("Error: " + (data.error || "Login failed"));
    }
});


// Sign up page
document.getElementById("signupForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/auth/signup/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();
    if (response.ok) {
        alert("Signup successful! Redirecting to login...");
        window.location.href = "login.html";
    } else {
        alert("Error: " + (data.error || "Signup failed"));
    }
});


// Recipe page
async function fetchRecipes() {
    const response = await fetch('/api/recipes/');
    const recipes = await response.json();
    const recipeList = document.getElementById('recipeList');

    if (recipes.length === 0) {
        recipeList.innerHTML = "<p>No recipes found. Add some!</p>";
    } else {
        recipes.forEach(recipe => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="/recipes/${recipe.id}/"><strong>${recipe.title}</strong></a> - ${recipe.description}`;
            recipeList.appendChild(li);
        });
    }
}

fetchRecipes();


// Recipe page detail
async function fetchRecipe() {
    const recipeId = window.location.pathname.split('/')[2]; // Extract recipe ID from URL
    const response = await fetch(`/api/recipes/${recipeId}/`);
    const recipe = await response.json();

    document.getElementById('recipeTitle').innerText = recipe.title;
    document.getElementById('recipeDescription').innerText = recipe.description;
    document.getElementById('recipeInstructions').innerText = recipe.instructions;

    const ingredientList = document.getElementById('ingredientList');
    recipe.ingredients.forEach(ingredient => {
        const li = document.createElement('li');
        li.innerText = `${ingredient.quantity} of ${ingredient.ingredient.name}`;
        ingredientList.appendChild(li);
    });
}

fetchRecipe();