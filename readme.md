# Pygame Proyect

## Installation

- First of all, clone the repository in your computer

- Next step, install pygame. You can create a Virtual Environment or you can install in your Python Path:

  - For create a VE:

    - First of all we need to check if we have `virtualenv` module installed in our computer. Use `pip freeze` or `pip list`
    to check if you have installed it.

      - If you don't have it, use `pip install virtualenv` for install

    - Open your terminal and execute `python -m venv <name_VE>` and now you have a VE folder in your VSC explorer

- Then, for install pygame use `pip install pygame`.

  - Installing on VE:

    - When we have our VE created, we need to activate it:

      - (WINDOWS) In your terminal execute `<name_VE>\Scripts\activate` and you can see if your VE is activated like this:

      ```cmd
      (<name_VE>) C:/...
      ```

      - (LINUX/MAC) In your terminal execute `<name_VE>/bin/activate` and you can see if your VE is activated like this:

      ```bash
      (<name_VE>) $<user_name>:/...
      ```

      - Then, use `pip install pygame` for install the module

  - Installing on Python Path:

    - Open your terminal, and directly, use `pip install pygame`

- Next step. We need to create a **data** folder to store the database records. Create a new folder called **data** in main folder

- Final step, run the file **screen.py** for play the game, and enjoy it!
