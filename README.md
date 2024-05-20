# Mask of Many Faces
DnD Fantasy Character Generator Telegram Bot

## Overview

This project is a Telegram bot that allows users to create custom fantasy Dungeons & Dragons characters. Users can select parameters for their character through a menu and upload their face to be placed on the generated character image.

## Features

- Menu-driven character creation
- Customizable parameters: race, class, hair, beard, gender, background
- Face swapping: upload your face to be placed on the generated character
- Generated images in a photorealistic, fantasy art style

## Installation

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management
- SQL db
- Insightface models 
- Telegram Bot API token

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Dimildizio/mask_of_many_faces.git
    cd mask_of_many_faces
    ```

2. **Install dependencies:**

    ```bash
    poetry install
    ```

3. **Set up a config:**

    Create a config `.yaml` file in the project `src/utilities` and add your variables:

    ```config
      swapper: your fastapi face swapper address
      
      gen_url: your image generation model url
      gen_model: type of the model
      gen_width: widths
      gen_height: heights
      gen_steps: steps of generation from 1 to 100
      gen_api: api for generation model
      gen_folder: where to save generations
      
      tg_token: telemgram token 
      face_folder: where to save downloaded images
      
      
      db_name: database name
      db_type: type of database
    ```

4. **Run the bot:**

    ```bash
    poetry run python main.py
    ```

## Usage

### Commands

- **/start**: Initialize the bot and create user data in the database.
- **/help**: Display help message.
- **/contacts**: Get contact information.
- **/menu**: Display the character creation menu.
- **/character**: Show current character details.
- **/generate**: Generate a character image based on selected parameters.
- **Photo upload**: Upload a photo to use your face on the generated character.

### Menu Navigation

1. **Main Menu**: Select from the following categories:
    - Race
    - Class
    - Hair
    - Beard
    - Gender
    - Background

2. **Subcategories**: Choose specific options within each category.

3. **Back Button**: Navigate back to the main menu from any subcategory.

## Example

1. **Genration Process:**
   
   Here is an example of generation and swap with given parameters:
     - Race: dwarf
     - Class: artificer
     - Hair: blonde
     - Beard: yes
     - Background: ship


   ![docs/img_examples/one example.png](https://github.com/Dimildizio/mask_of_many_faces/blob/main/docs/img_examples/one_example.png?raw=true)

       
2. **More examples:**
   
       prompt -> generated image -> source face -> result
   
   ![docs/img_examples/one example.png](https://github.com/Dimildizio/mask_of_many_faces/blob/main/docs/img_examples/many_example.png?raw=true)


## Project Structure
- `src`: folder for project python files
  - `main.py`: Entry point for the bot.
  - `tg_bot/`: Telegram bot related handlers and logic.
  - `database/`: Database models and operations.
  - `generation/`: Logic for generating character images.
  - `swapper/`: Logic for face swapping in images.
  - `utilities/`: Constants and helper functions.
- `tests`: folder for tests
- `docs`: folder for docs

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License.
