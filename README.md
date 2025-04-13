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

