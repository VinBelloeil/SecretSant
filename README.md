# SecretSanta 🎁

**SecretSanta** is a coding exercise project designed to develop a web application that facilitates organizing Secret Santa 
gift exchanges among friends or colleagues. Users can add participants, define gift-giving rules, 
and perform the draw to assign who gives a gift to whom.

---

## 🚀 Features

- ✅ **CRUD operations** for managing participants
- 🎯 **Draw mechanism** for assigning Secret Santa pairs
- 🚫 **Custom rules** to exclude certain people from giving to others (e.g., no gift between couples or coworkers)
- 🧩 Modular backend design

---

## 🛠️ Technologies Used

- **Python**
- **Flask**

---

## 📦 Installation

To run the app locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VinBelloeil/SecretSant.git
   cd SecretSant
   ```

2. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch DB**:
   Before running the app, initialize the database:

    ```bash
    flask shell
    >>> db.create_all()
    >>> exit()
    ```

4. **Run the Flask app**:
   ```bash
   flask run
   ```

5. Open your browser and go to:  
   `http://127.0.0.1:5000/`

---

## 💻 Usage

Once the app is running:

1. Add participants (names and optional details)
2. Define exclusion rules (for example, Alice can't give to Bob)
3. Launch the Secret Santa draw
4. View the result (who gives a gift to whom)

## 🔧 Possible Improvements

While the current version of the Secret Santa app is functional, here are some ideas to enhance it further:

- 🎨 **Improve the UI**  
  Add a more responsive front-end design for a better user experience.

- 🧠 **Optimize the Draw Algorithm**  
  Replace the current brute-force shuffle with a recursive algorithm.

- 🔀 **Better Route Separation**  
  Organize participant-related routes into their own Blueprint.

- ⚙️ **Shared Test Configuration**  
  Introduce a common configuration file or fixture setup for all tests.

- 📄 **Better Commit Split**  
  Structure commits to reflect precise changes.

- 🚫 **Restrict Invalid Operations**  
  Add checks to prevent scenarios like having two participants with the same name.

