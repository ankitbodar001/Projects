# YouTube Video Scraper

This project is a web application built with Flask that allows users to search for YouTube videos and retrieve their details such as URL, thumbnail URL, title, views, and upload time. The application uses Selenium and BeautifulSoup for web scraping and stores the scraped data in a MongoDB database.

## Installation

1. Clone the repository:

   git clone https://github.com/your-username/your-repo.git

1. Install the required dependencies:

   pip install -r requirements.txt

2. Download and install the Chrome WebDriver suitable for your Chrome version: https://sites.google.com/a/chromium.org/chromedriver/downloads.

3. Update the 'executable_path' in the script (app.py) with the path to the Chrome WebDriver executable on your machine:

   service = Service(executable_path='/path/to/chromedriver')

4. Make sure you have MongoDB installed and running on your system. If not, follow the instructions at https://docs.mongodb.com/manual/installation/ to install and configure MongoDB.

5. Start the Flask application:

   python app.py

6. Access the application in your web browser at http://localhost:8000.

## Usage
1. Enter the search query in the input field on the home page.
2. Click the "Search" button.
3. The application will scrape the YouTube video data based on the search query and display the results with video details.
4. The scraped data will be stored in a MongoDB database.

## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the https://chat.openai.com/c/LICENSE.
You can modify this template according to your specific project requirements. Don't forget to include a `LICENSE` file if you decide to use a different license for your project.
