# CodeSnap <img src="https://github.com/Nestor162/CodeSnap/assets/113930607/658c24db-dbed-4f35-bbc8-47ae0526c34e" alt="App icon" width="60" height="60" align="left">

CodeSnap is a simple code image generator. Paste or type your code, click a button, and get a downloadable image for easy sharing. You can also tweak the style to your liking. No complications, just a quick way to present and share your code.

## Screenshots
<div style="display: flex; gap: 20px;">

<img src="https://github.com/Nestor162/CodeSnap/assets/113930607/c413a92b-21c7-4c78-b78b-a779899f961d" width="400px">

<img src="https://github.com/Nestor162/CodeSnap/assets/113930607/e1f9d44f-db43-4808-be26-809d6d61d181" width="400px">

<img src="https://github.com/Nestor162/CodeSnap/assets/113930607/40d2706d-61d5-4887-89db-76c1a981caf0" width="400px">

<img src="https://github.com/Nestor162/CodeSnap/assets/113930607/17919196-13fa-461c-b583-d2587a472e84" width="400px">

</div>

## Getting Started

### Installation

1.  Clone the repository to your local machine:
    ```bash:
    git clone https://github.com/Nestor162/CodeSnap
    cd CodeSnap
    ```
2.  Set up a virtual environment and install the required dependencies using `requirements.txt`:
    ```bash:
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    ```

### Running the App

3. Generate random secret key and save to an .env file
   ```bash:
   echo "FLASK_SECRET_KEY=$(openssl rand -hex 24)" > .env
   ```
4. Run the Flask application server:

   ```bash:
   python -m flask run
   ```

   This will start the CodeSnap server in development mode. Visit http://127.0.0.1:5000 in your browser to use CodeSnap.

## Features

- **Extensive Language Support**: Choose from a vast selection of over 500 programming languages + automatic language detection.
- **Theme Customization**: Customize the style from a collection of more than 45 themes (color palettes).
- **High-Quality Image Generation**: Generate high-quality code images for easy downloading.

## What I Learned

In the process of developing CodeSnap, I acquired valuable skills and knowledge, including:

- **Flask Project Setup**: Successfully set up and ran a Flask project, laying the foundation for a robust web application.
- **Jinja Templates Usage**: Used Jinja templates to dynamically render content, incorporating logic within the HTML, and reusing code through templates..
- **CSS Styling with Vanilla CSS**: Employed vanilla CSS to establish a visually appealing, minmal and responsive user interface, ensuring a seamless user experience.
- **Playwright for Image Generation**: Implemented Playwright to dynamically create and capture code images, offering users a straightforward method for visually representing their code.
- **Pygments for Syntax Highlighting**: Enhanced the visual appeal of code snippets by implementing Pygments for syntax highlighting, making code readability a priority.
- **Session Management for Improved UX**: Leveraged browser sessions to efficiently save and manage states, contributing to an enhanced and more user-friendly experience.
- **JavaScript for Interactivity**: Implemented JavaScript to boost interactivity and responsiveness within the application, creating a more engaging user environment.

## Potential Future Additions

CodeSnap aims to continuously improve, and potential future features may include:

- Image customization options such as changing size and format.
- Implementing a progress bar to provide visual feedback during image generation, thereby enhancing the overall user experience.
- Exploring a theme gallery and a saved code snippet gallery for user convenience.

## Acknowledgments
This project was inspired by and developed with the guidance of the tutorial provided by [RealPython](https://realpython.com/python-code-image-generator/). Thanks to RealPython for providing valuable resources and guidance.
