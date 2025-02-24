# **Flavour Vault**

FlavourVault is a platform where users can share and discover recipes. This application is built using Python, Django, Cloudinary for image storage, PostgreSQL for the database, and is deployed on Heroku.


[**__link to deployed site here__**](https://flavour-vault-6970ed23d7f4.herokuapp.com/)
<br><br>

<img src="static/readme-img/am-i-responsive.png">
<br><br>

# Contents

* [User Experience](#user-experience)
    * [Owner Goals](#owner-goals)
    * [Visitor Goals](#visitor-goals)
* [Design](#design)
    * [Wireframes](#wireframes)
    * [Database Schema](#database-schema)
    * [Images](#images)
* [Features](#features)
    * [Multi-page Features](#multi-page-features)
    * [All User Features](#all-user-features)
    * [Logged-In Features](#logged-in-features)
    * [CRUD Functionality](#crud-functionality)
* [Technologies](#technologies)
    * [Languages](#languages)
    * [Tools](#tools)
* [Testing](#testing)
* [Deployment](#deployment)
    * [Deployment to Heroku](#deployment-to-heroku)
    * [Forking Repository](#forking-the-github-repository)
    * [Making a Local Clone](#making-a-local-clone)
    * [Version Control](#version-control)
* [Credits](#credits)

<br><br>

# User Experience

FlavourVault is designed to allow users to share their recipes and browse others. It also gives users the ability to search for recipes based on tags, categories, and specific ingredients.

## Owner Goals
- Provide a platform for users to easily share and browse recipes.
- Allow users to upload photos of their dishes.


## Visitor Goals
As a visitor:
- I want to view a variety of recipes from other users.
- I want to be able to create an account and submit my own recipes.
- I want to be able to search for recipes based on tags or categories.

<br><br>

# Design

## Wireframes

Wireframes created using miro.

<details>
<summary>Home Desktop</summary>
<br>
<img src="static/readme-img/home-desktop.png">
</details>
<details>
<summary>Home Mobile</summary>
<br>
<img src="static/readme-img/home-mobile.png">
</details>
<details>
<summary>Signup Desktop</summary>
<br>
<img src="static/readme-img/signup-desktop.png">
</details>
<details>
<summary>Singup Mobile</summary>
<br>
<img src="static/readme-img/signup-mobile.png">
</details>
<details>
<summary>Login Desktop</summary>
<br>
<img src="static/readme-img/login-desktop.png">
</details>
<details>
<summary>Login Mobile</summary>
<br>
<img src="static/readme-img/login-mobile.png">
</details>
<details>
<summary>Account Desktop</summary>
<br>
<img src="static/readme-img/account-desktop.png">
</details>
<details>
<summary>Account Mobile</summary>
<br>
<img src="static/readme-img/account-mobile.png">
</details>
<details>
<summary>Recipes Desktop</summary>
<br>
<img src="static/readme-img/recipes-desktop.png">
</details>
<details>
<summary>Recipes Mobile</summary>
<br>
<img src="static/readme-img/recipes-mobile.png">
</details>
<details>
<summary>Recipe detail Desktop</summary>
<br>
<img src="static/readme-img/recipe-detail-desktop.png">
</details>
<details>
<summary>Recipe detail Mobile</summary>
<br>
<img src="static/readme-img/recipe-detail-mobile.png">
</details>
<details>
<summary>Create recipe Desktop</summary>
<br>
<img src="static/readme-img/create-recipe-desktop.png">
</details>
<details>
<summary>Create recipe Mobile</summary>
<br>
<img src="static/readme-img/create-recipe-mobile.png">
</details>
<details>
<summary>Edit recipe Desktop</summary>
<br>
<img src="static/readme-img/edit-recipe-desktop.png">
</details>
<details>
<summary>Edit recipe Mobile</summary>
<br>
<img src="static/readme-img/edit-recipe-mobile.png">
</details>
<details>
<summary>Logout Desktop</summary>
<br>
<img src="static/readme-img/logout-desktop.png">
</details>
<details>
<summary>Logout Mobile</summary>
<br>
<img src="static/readme-img/logout-mobile.png">
</details>
<br><br>

## Database Schema

Schema for PostgreSQL database was created on [Draw.io](https://app.diagrams.net/)
<details>
<summary>DB Schema</summary>
<br>
<img src="static/readme-img/db-schema.png">
</details>
<br><br>

# Features

## Multi-page Features

### Navbar

The navbar is displayed on all pages except for login, signup, and create recipe. On mobile devices, it collapses into a hamburger icon that opens as a side navigation menu. The visible links depend on whether the user is logged in or not.

<details>
<summary>Navbar home Logged Out</summary>
<br>
<img src="static/readme-img/navbar-home-loggedout.png">
</details>
<details>
<summary>Navbar home Logged In</summary>
<br>
<img src="static/readme-img/navbar-home-loggedin.png">
</details>
<details>
<summary>Navbar recipes Logged out</summary>
<br>
<img src="static/readme-img/navbar-recipes-loggedout.png">
</details>
<details>
<summary>Navbar recipes Logged In</summary>
<br>
<img src="static/readme-img/navbar-recipes-loggedin.png">
</details>
<details>
<summary>Navbar recipe detail Logged Out</summary>
<br>
<img src="static/readme-img/navbar-recipe-detail-loggedout.png">
</details><details>
<summary>Navbar recipe detail Logged In</summary>
<br>
<img src="static/readme-img/navbar-recipe-detail-loggedin.png">
</details>
<details>
<summary>Navbar Account</summary>
<br>
<img src="static/readme-img/navbar-account.png">
</details><details>
<summary>Navbar Create Recipe</summary>
<br>
<img src="static/readme-img/navbar-create-recipe.png">
</details>
<details>
<summary>Navbar Edit Recipe</summary>
<br>
<img src="static/readme-img/navbar-edit-recipe.png">
</details><details>
<summary>Navbar Logout</summary>
<br>
<img src="static/readme-img/navbar-logout.png">
</details>

### Footer

Footer is present in all pages, with a disclaimer and links to GitHub profile, Instagram and facebook.

<details>
<summary>Footer</summary></summary>
<br>
<img src="static/readme-img/footer.png">
</details>
<br><br>

## All User Features

## Home Page

The home page is available to all users here users can view the top 6 best recipes.

<details>
<summary>Home Page</summary></summary>
<br>
<img src="static/readme-img/home-page.png">
</details>
<br><br>

### Log In Page

The login page is rendered, verifying the user’s existence in the database and validating the password. If the user is not registered, a prompt at the bottom provides a link to the singup page.

<details>
<summary>Log In</summary></summary>
<br>
<img src="static/readme-img/login-page.png">
</details>
<br><br>

### Sign Up Page

The signup page is rendered to register the user for the site, checks if user is already in database, if not adds them to database. If the user is registered, a prompt at the bottom provides a link to the login page.

<details>
<summary>Sign Up</summary></summary>
<br>
<img src="static/readme-img/signup-page.png">
</details>
<br><br>

### Recipe Detail Page

The recipe detail page is where users can the individual recipes. In the page the users can see the author, ingredients, desctription, instructions, image and reviews.

<details>
<summary>Recipe detal page</summary></summary>
<br>
<img src="static/readme-img/recipe-detail-page.png">
</details>
<br><br>

### Recipe Page

The recipe page is where users can see all the avaliable recipes and who created them, they can also see the date that the recipe was created on.

<details>
<summary>Recipe page</summary></summary>
<br>
<img src="static/readme-img/recipe-page.png">
</details>
<br><br>

## Logged In Features

These features/pages available to users who are logged in 

### Account Page

This is the page that the user can see, edit, create and delete recipes. They can also view their reviews.

<details>
<summary>Account page</summary></summary>
<br>
<img src="static/readme-img/account-page.png">
</details>
<br><br>

### Create Recipe Page

This is the page that the user can create a new recipe. Users can add title, description, instructions, catagory, image and multiple ingredients

<details>
<summary>Create recipe page</summary></summary>
<br>
<img src="static/readme-img/create-recipe-page.png">
</details>
<br><br>

### Edit Recipe Page

This is the page that the user edit their posted recipe, users can edit everything that is avalible in the create recipe page

<details>
<summary>Edit recipe page</summary></summary>
<br>
<img src="static/readme-img/edit-recipe-page.png">
</details>
<br><br>

### Add review

In the recipe detail page users can add a review and a comment on other recipes. Users can ad 1-5 stars

<details>
<summary>Recipe Detail Page</summary></summary>
<br>
<img src="static/readme-img/add-review.png">
</details>
<br><br>

### Log Out Page

When users click on the logut button in the navbar they get redirected to the log out page

<details>
<summary>Log out Page</summary></summary>
<br>
<img src="static/readme-img/logout-page.png">
</details>
<br><br>

## CRUD Functionality

| Page            | Create                                                       | Read                                                           | Update                                                  | Delete                                                       |
|-----------------|--------------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------|-------------------------------------------------------------|
| **Login**       |                                                              | Read username and password for authentication                 |                                                              |                                                             |
| **Register**    | Create a new user account                                    | Read username to check if the user already exists               |                                                            |                                                             |
| **Home Page**   |                                                              | View featured recipes and display details                      |                                                         |                                                             |
| **Recipe Page** | Create a new recipe with ingredients and images               | Read individual recipe details, including ingredients and instructions | Edit recipe details, including ingredients and image      | Delete recipe from the database                             |
| **Recipe Detail** |                                                              | View full details of the recipe, including ingredients and reviews | Edit recipe details                                     |                                                             |
| **Account Page** | Create and view user’s personal recipes                     | View all recipes posted by the user                            | Edit recipe details and ingredients                      | Delete personal recipes                                     |
| **Create Recipe Page** | Create a new recipe with ingredients, image, and details | View the form to input recipe information                       | Update recipe details and ingredients                     |                                                             |
| **Edit Recipe Page** | Update existing recipe with new ingredients and details   | View the current recipe to edit its details                    | Modify the recipe's ingredients, instructions, and image  |     

# Technologies

## Languages

* HTML5 - Used for structuring and organizing content.
* Bootstrap - Utilized for styling and responsive design.
* JavaScript - Handles frontend interactivity, initializes Bootstrap components, and processes functions that interact with the backend data.
* Python - Manages the backend functionality.
    * asgiref==3.8.1
    * certifi==2025.1.31
    * cffi==1.17.1
    * charset-normalizer==3.4.1
    * cloudinary==1.36.0
    * crispy-bootstrap5==2024.10
    * cryptography==44.0.0
    * dj-database-url==2.3.0
    * dj-rest-auth==7.0.1
    * dj3-cloudinary-storage==0.0.6
    * Django==5.1.5
    * django-allauth==65.4.0
    * django-cloudinary-storage==0.3.0
    * django-crispy-forms==2.3
    * djangorestframework==3.15.2
    * djangorestframework_simplejwt==5.4.0
    * gunicorn==20.1.0
    * idna==3.10
    * pillow==11.1.0
    * psycopg2-binary==2.9.10
    * pycparser==2.22
    * PyJWT==2.10.1
    * python-decouple==3.8
    * requests==2.32.3
    * setuptools==75.8.0
    * six==1.17.0
    * sqlparse==0.5.3
    * typing_extensions==4.12.2
    * urllib3==1.26.20
    * whitenoise==6.8.2
<br><br>

## Tools

* **Cloudinary** - Used for image and media storage and management.
* **Heroku** - Used for deployment of the application.
* **PostgreSQL** - Used for the database management.
* **Git/GitHub** - Used for version control and storage.
* **Django** - The web framework used for building the backend of the application.
* **Django REST Framework** - Used for building the API and handling requests.
* **FontAwesome** - Used for icons in the application, including buttons and navigation.
* **Cloudinary Storage** - Integrated to handle media uploads and static file storage.
* **Whitenoise** - Used for serving static files in production (with Heroku).
* **Google Dev Tools** - Used for troubleshooting during development.
* **Draw.io** - Used for designing the database schema.
* **miro** - Used for wireframe designs.
* **Requests Library** - Used for making HTTP requests in the backend.
* **Pillow** - Used for image processing in Django.
* **Am I Responsive** - Used to create responsive mockup for readme.

# Testing

For testing please the [Testing](/TESTING.md) documentation.
<br><br>

## Deployment

### Deployment to Heroku

To deploy to Heroku:
1. In GitPod CLI, the root directory of the project, run:
    pip3 freeze --local > requirements.txt
    to create a requirements.txt file containing project dependencies.
2. In the Gitpod project workspace root directory, create a new file called Procfile, with capital 'P'.
    Open the Procfile. Inside the file, check that web: python3 app.py has been added when creating the file
    Save the file.
3. Push the 2 new files to the GitHub repository
4. Login to Heroku, select Create new app, add the name for your app and choose your closest region.
5. Navigate to the Deploy tab on Heroku dashboard and select Github, search for your repository and click 'connect'.
6. Navigate to the settings tab, click reveal config vars and input the following:

| Key               | Value                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| **DATABASE_URL**   | Your PostgreSQL database URL                         
| **SECRET_KEY**     | Your Secret key                                                                                   |
| **CLOUDINARY_URL** | Your Cloudinary URL                                                                              |

7. Deploy the app by selecting **Deploy Branch** under the **Deploy** tab.

### Forking the GitHub Repository
<br>

By forking the **FlavourVault** GitHub repository, you make a personal copy of the repository to explore and make changes without affecting the original repository. To fork the repository:

1. Log in to GitHub and go to the [FlavourVault Repository](https://github.com/rand-Jelo/Flavour-Vault).
2. At the top of the repository page, just above the "Settings" button, click the **Fork** button.
3. You should now have your own copy of the repository in your GitHub account.
<br><br>

### Making a Local Clone
<br>

To clone the repository locally, follow these steps:

1. Log in to GitHub and go to the [FlavourVault Repository](https://github.com/rand-Jelo/Flavour-Vault).
2. Under the repository name, click the **Clone or download** button.
3. To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
4. Open Git Bash
5. Change the current working directory to the location where you want the cloned directory to be made.
6. Type `git clone`, and then paste the URL you copied in Step 3.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```
7. Press Enter. Your local clone will be created.
<br><br>

### Version Control

We use **Git** and **GitHub** for version control. Git helps us track the history of the project and collaborate with others. It enables us to manage different versions of the code and helps us to roll back changes when necessary.

- **git add**: Stage the changes for commit.
- **git commit**: Commit the staged changes with a message describing them.
- **git push**: Push the changes to the remote GitHub repository.

Once your changes are committed, you can push them to GitHub to make them available to collaborators and for deployment.
<br><br>

# **Credits**

## **Code**
- Recipe submission, editing, and CRUD functionality implemented using [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/).
- Image upload and storage handled via [Cloudinary](https://cloudinary.com/) integration.
- Authentication and user management built using [Django Allauth](https://django-allauth.readthedocs.io/en/latest/) and [Django Rest Auth](https://dj-rest-auth.readthedocs.io/en/latest/).
- PostgreSQL database schema designed with [Draw.io](https://app.diagrams.net/).
- Database interactions optimized using [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/queries/).
- Search and filtering logic adapted from [Django documentation](https://docs.djangoproject.com/en/stable/topics/db/search/).

## **Media**
- Icons sourced from [Font Awesome](https://fontawesome.com/).
- Responsive mockups created using [Am I Responsive](https://ui.dev/amiresponsive).
- UI wireframes designed using [Miro](https://miro.com/).
- Images sourced from [Freepik](https://www.freepik.com/).

## **Tutorials and Resources**
- Django authentication setup guidance from [Django Allauth official documentation](https://django-allauth.readthedocs.io/en/latest/installation.html).
- API request handling in Django REST Framework based on [DRF official documentation](https://www.django-rest-framework.org/tutorial/quickstart/).
- PostgreSQL integration and environment setup references from [Heroku documentation](https://devcenter.heroku.com/categories/heroku-postgres).
- Frontend styling approaches adapted from [Bootstrap documentation](https://getbootstrap.com/docs/).

## **Acknowledgements**
- A big thank you to my mentor, **Mitko Bachvarov**, for his continuous guidance and feedback throughout the project.
- Special thanks to the [Stack Overflow](https://stackoverflow.com/) community for providing solutions to technical challenges.
- Appreciation to the **Open Source contributors** behind Django, DRF, and PostgreSQL for their valuable frameworks.
