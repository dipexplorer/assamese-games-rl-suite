# Visualization & Web GUI Interface

Flask-based interactive web server and rendering template for visualising Kori Khel game state transitions and agent decisions in real time.

## Directory Structure

```
visualization/
├── gui_server.py     # Flask backend server & WebSocket interface
├── static/           # Asset images (board, cowrie shells)
└── templates/        # HTML templates for 2D board UI
```

## Running the Web GUI

```bash
python -m visualization.gui_server
```

Open `http://127.0.0.1:5000` in a web browser.
