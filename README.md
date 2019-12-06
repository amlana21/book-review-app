# Book Search and Review

This is a flask application which lets users search for a book and submit reviews on the book. Below are technical details for the project:

<strong>Backend:</strong>  
 * Flask
 * Postgres DB

<strong>FrontEnd:</strong>  
 * HTML  
 * Javascript  
 * Bootstrap  
 * JQuery  

The application is also deployed to Heroku and can be accessed here:  
https://book-store-ac.herokuapp.com/  

## <strong>Steps to Run the App</strong>  
 * Install the dependencies:  
  `` pip install requirements.txt ``  
 * Set the environment variable for the app name  
  `` export FLASK_APP="application" ``
 * Run the app:  
  `` flask run ``  
  If it is to be accessed publicly:  
  `` flask run --host 0.0.0.0 ``

## <strong>Application Functional Details</strong>  
Below is a high level functional flow for the application:  
 * Login page opens when navigated to the application  
 * Enter credentials to login to the application  
 * User is directed to the search page  
 * The search can be performed in multiple ways  
  * Search with the exact Title, Author or ISBN  
  * Search with a keyword and it will show results if that is found as a match in any of the Titles, Author or ISBN columns  
  * Search results will show a list of book names along with an image of the book. The image is pulled from the Book reads API  
  * Since the images are pulled from a different API, the search results may take few seconds to load based on the number of results  
 * Click on any book name to view details for the book  
 * Once in the details page, you can view multiple details about the book along with a larger image(if available in Book Reads API)  
 * The details page will also show a table with list of reviews left for the book on the application. You will have to scroll down a bit to get the review list  
 * To submit a review of your own, select a rating(1-5) and provide a brief review. Click Submit to save the review  
  * If there are any errors, a pop up will show the error  
 * To navigate back to the Search page, click on the 'Home' link at the top Navigation bar or hit back button  
 * At any point, to log out of the application, hit the Logout link at the top  

## <strong>Application Technical Details</strong>  
Below is a description of the scripts and files involved in the application. The application is separated in two portions and the description is split accordingly:  

  ### Frontend  
  The client side consist of HTML file for the UI and Javascript/Jquery for transactions with the server. Below are the folders which contribute toward the client UI and functionality:  

  * <em>static: </em>Contains the Javascript files and the css files used by the HTML client side. There are separate css and js files named after the corresponding html pages. The css files define the style for the UI components at the client side. The JS files perform the API calls to the server to facilitate the logic of the application. This includes handling the login, performing the search, fetching Book details and committing the reviews to the database.   

  * <em>templates: </em> Contains the HTML files which form the UI of the application that is presented on the client side.These templates are rendered by the Flask app which is server side. The frontend UI also uses the Bootstrap framework to beautify the look and feel of the components. There are different templates for each of the pages:  
    * <em>details.html: </em>Book details page  
    * <em>index.html: </em>Search page  
    * <em>login.html: </em>Login page 
    * <em>logout.html: </em>Logout page. Redirects to the login page  

  ### Backend  
  The server side consist of a Flask app and various python scripts to support the functionalities in the app. The modules used in the app are in the requirements file to be installed if running on a different machine.Belo are the files which contribute towards the server side functionality:  
    
  * <em>application. py: </em>This is the server side Flask app. This performs all the application operations and sends the responses to client side. Some of the functionalities implemented in the app are as follows:  
    * Performs a keyword search for the books from the database
    * Connects to a postgres DB to perform Query and CRUD operations(except the delete part)  
    * User passwords are stored as a hash in the database. <em>bcrypt</em> module used for the hashing.  
    * User ID is stored in the session once a login is successful and this is used to validate each of the page access  
    * Sends back response to client API calls, in json  
    * All the endpoints are also available as separate callable REST API endpoints  

  * <em>import .py: </em>This is the python script to load the initial books data from the csv to the Postgres database. If there are any exceptions in the load, those are written to the exceptions .csv file.  

  * <em>requirements .txt: </em>Contains all the packages to be installed for the app to run.  

  * <em>sqls .sql: </em>All the sql queries used to prepare the database and the data in the database.  

  * <em>xmlparse .py: </em>Python script that parses the XML output from the Book reads API and gets the image URL for each book.  



