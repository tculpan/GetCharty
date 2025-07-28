# GetCharty - Intelligent CSV Chart Generator

GetCharty is a web-based application that automatically creates professional charts from CSV files with intelligent server-side processing and formatting.

## 🚀 Quick Start (Local Deployment)

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Option 1: Automated Setup (Recommended)

#### On Windows:
```bash
start-local.bat
```

#### On macOS/Linux:
```bash
chmod +x start-local.sh
./start-local.sh
```

### Option 2: Manual Setup

1. **Install Python dependencies:**
   ```bash
   cd server
   pip install -r requirements.txt
   cd ..
   ```

2. **Start the Flask server:**
   ```bash
   cd server
   python app.py
   ```
   The server will start on `http://localhost:5000`

3. **Start the client server (in a new terminal):**
   ```bash
   cd client
   python -m http.server 8000
   ```
   The client will be available at `http://localhost:8000`

## 📊 How to Use

1. **Open your browser** and go to `http://localhost:8000`
2. **Upload a CSV file** using the file upload button
3. **Watch the magic happen!** The server will:
   - Clean and standardize your data
   - Generate intelligent chart titles and labels
   - Create professional-looking visualizations
   - Auto-detect data types (currency, percentages, etc.)

## 🎯 Features

### Intelligent Data Processing
- **Smart Column Cleaning**: Converts technical column names to professional display names
- **Data Type Detection**: Automatically detects currency, percentages, and large numbers
- **Missing Data Handling**: Gracefully handles empty cells and invalid data

### Professional Chart Generation
- **Auto Title Generation**: Creates context-aware chart titles
- **Smart Axis Labels**: Adds appropriate units and context
- **Professional Styling**: Clean, modern chart design
- **Responsive Design**: Charts adapt to different screen sizes

### Supported Chart Types
- **Bar Charts**: Default visualization
- **Line Charts**: For trend analysis
- **Pie Charts**: For distribution analysis
- **Scatter Plots**: For correlation analysis

## 🏗️ Architecture

### Frontend (`client/`)
- **HTML/CSS/JavaScript**: Modern, responsive interface
- **Plotly.js**: Interactive chart rendering
- **PapaParse**: CSV file parsing

### Backend (`server/`)
- **Flask**: Python web framework
- **Pandas**: Data processing and analysis
- **NumPy**: Numerical computing
- **CORS**: Cross-origin resource sharing

### Key Functions
- `/process-file`: Main endpoint for CSV processing
- `/format-chart`: Chart formatting endpoint

## 📁 Project Structure

```
GetCharty/
├── client/
│   └── index.html          # Frontend application
├── server/
│   ├── app.py              # Flask server
│   ├── requirements.txt    # Python dependencies
│   └── lambda/            # Original AWS Lambda functions
├── start-local.sh         # Linux/macOS startup script
├── start-local.bat        # Windows startup script
└── README.md              # This file
```

## 🔧 Development

### Running in Development Mode
The Flask server runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger

### API Endpoints

#### POST `/process-file`
Processes CSV files and returns formatted data.

**Request Body:**
```json
{
  "filename": "data.csv",
  "content": "csv,content,here",
  "chart_config": {
    "chart_type": "bar"
  }
}
```

**Response:**
```json
{
  "data": [...],
  "chart_elements": {
    "title": "Revenue by Product",
    "x_label": "Product",
    "y_label": "Revenue (USD)"
  },
  "processing_info": {
    "duration": 45.2,
    "rows_processed": 100,
    "columns_processed": 3
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `server/app.py` (line 257)
   - Update the API endpoint in `client/index.html` (line 95)

2. **Python dependencies not found**
   - Run `pip install -r server/requirements.txt`

3. **CORS errors**
   - Ensure the Flask server is running on `http://localhost:5000`
   - Check that CORS is enabled in `server/app.py`

4. **File upload not working**
   - Check browser console for errors
   - Ensure file is under 5MB
   - Verify file is in CSV format

### Debug Mode
The Flask server runs in debug mode by default. Check the terminal for detailed error messages.

## 📈 Sample Data

Create a CSV file with this structure to test:
```csv
Product,Revenue,Quantity
Widget A,15000,45
Widget B,22000,67
Widget C,18000,52
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

This project is for demonstration purposes.

---

**Happy Charting! 📊✨** 